#!/usr/bin/env bash
# Stand up hosting for the manual: private S3 bucket, CloudFront in front of it,
# and a GitHub OIDC role so CI deploys without long-lived AWS keys.
#
# Idempotent: safe to re-run. Prints the GitHub variables and secret to set at the end.
#
#   aws configure          # personal account, once
#   ./build/aws-setup.sh
set -euo pipefail

BUCKET="${BUCKET:-missing-fleet-manual-site}"
REGION="${REGION:-us-east-1}"
REPO="${REPO:-jakestenger/missing-fleet-manual}"
ROLE="${ROLE:-missing-fleet-manual-deploy}"

ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
echo "account $ACCOUNT, region $REGION, repo $REPO"

# --- S3: private. CloudFront reads it through an origin access control. -------
if ! aws s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
  if [ "$REGION" = "us-east-1" ]; then
    aws s3api create-bucket --bucket "$BUCKET" --region "$REGION" >/dev/null
  else
    aws s3api create-bucket --bucket "$BUCKET" --region "$REGION" \
      --create-bucket-configuration LocationConstraint="$REGION" >/dev/null
  fi
  echo "created bucket $BUCKET"
fi
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# --- CloudFront function: map /path/ to /path/index.html ----------------------
# Docusaurus emits directory/index.html. The S3 REST origin that OAC requires does
# not serve index documents for subdirectories the way website hosting does, so
# without this every page below the root 404s.
FN_NAME="${ROLE}-rewrite"
FN_CODE='function handler(event) {
  var req = event.request;
  var uri = req.uri;
  if (uri.endsWith("/")) { req.uri = uri + "index.html"; return req; }
  // Section slugs contain dots (1.1-what-fleet-is, 8.14-degradation, a.6-glossary),
  // so "contains a dot" cannot mean "is a file". Test the last segment for a real
  // extension instead, or every section 403s while the homepage works.
  var last = uri.substring(uri.lastIndexOf("/") + 1);
  if (!/\.[A-Za-z0-9]{2,5}$/.test(last)) { req.uri = uri + "/index.html"; }
  return req;
}'
if ! aws cloudfront describe-function --name "$FN_NAME" >/dev/null 2>&1; then
  printf '%s' "$FN_CODE" > /tmp/rewrite.js
  aws cloudfront create-function --name "$FN_NAME" \
    --function-config "Comment=append index.html,Runtime=cloudfront-js-2.0" \
    --function-code fileb:///tmp/rewrite.js >/dev/null
  ETAG=$(aws cloudfront describe-function --name "$FN_NAME" --query ETag --output text)
  aws cloudfront publish-function --name "$FN_NAME" --if-match "$ETAG" >/dev/null
  echo "created and published CloudFront function $FN_NAME"
fi
FN_ARN=$(aws cloudfront describe-function --name "$FN_NAME" \
  --query 'FunctionSummary.FunctionMetadata.FunctionARN' --output text)

# --- Origin access control ----------------------------------------------------
OAC_ID=$(aws cloudfront list-origin-access-controls \
  --query "OriginAccessControlList.Items[?Name=='$BUCKET'].Id | [0]" --output text 2>/dev/null || echo "None")
if [ "$OAC_ID" = "None" ] || [ -z "$OAC_ID" ]; then
  OAC_ID=$(aws cloudfront create-origin-access-control --origin-access-control-config \
    "Name=$BUCKET,Description=manual,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3" \
    --query 'OriginAccessControl.Id' --output text)
  echo "created origin access control $OAC_ID"
fi

# --- CloudFront distribution --------------------------------------------------
DIST_ID=$(aws cloudfront list-distributions \
  --query "DistributionList.Items[?Comment=='$BUCKET'].Id | [0]" --output text 2>/dev/null || echo "None")
if [ "$DIST_ID" = "None" ] || [ -z "$DIST_ID" ]; then
  cat > /tmp/dist.json <<JSON
{
  "CallerReference": "$BUCKET-$(date +%s)",
  "Comment": "$BUCKET",
  "Enabled": true,
  "DefaultRootObject": "index.html",
  "Origins": {"Quantity": 1, "Items": [{
    "Id": "s3origin",
    "DomainName": "$BUCKET.s3.$REGION.amazonaws.com",
    "OriginAccessControlId": "$OAC_ID",
    "S3OriginConfig": {"OriginAccessIdentity": ""}
  }]},
  "DefaultCacheBehavior": {
    "TargetOriginId": "s3origin",
    "ViewerProtocolPolicy": "redirect-to-https",
    "Compress": true,
    "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
    "FunctionAssociations": {"Quantity": 1, "Items": [
      {"EventType": "viewer-request", "FunctionARN": "$FN_ARN"}
    ]}
  },
  "CustomErrorResponses": {"Quantity": 1, "Items": [
    {"ErrorCode": 404, "ResponsePagePath": "/404.html", "ResponseCode": "404", "ErrorCachingMinTTL": 60}
  ]}
}
JSON
  DIST_ID=$(aws cloudfront create-distribution --distribution-config file:///tmp/dist.json \
    --query 'Distribution.Id' --output text)
  echo "created distribution $DIST_ID (takes a few minutes to deploy)"
fi
DIST_DOMAIN=$(aws cloudfront get-distribution --id "$DIST_ID" --query 'Distribution.DomainName' --output text)

# --- Bucket policy: only this distribution may read ---------------------------
cat > /tmp/policy.json <<JSON
{"Version":"2012-10-17","Statement":[{
  "Sid":"AllowCloudFrontRead","Effect":"Allow",
  "Principal":{"Service":"cloudfront.amazonaws.com"},
  "Action":"s3:GetObject","Resource":"arn:aws:s3:::$BUCKET/*",
  "Condition":{"StringEquals":{"AWS:SourceArn":"arn:aws:cloudfront::$ACCOUNT:distribution/$DIST_ID"}}
}]}
JSON
aws s3api put-bucket-policy --bucket "$BUCKET" --policy file:///tmp/policy.json

# --- GitHub OIDC provider and deploy role -------------------------------------
OIDC_ARN="arn:aws:iam::$ACCOUNT:oidc-provider/token.actions.githubusercontent.com"
if ! aws iam get-open-id-connect-provider --open-id-connect-provider-arn "$OIDC_ARN" >/dev/null 2>&1; then
  aws iam create-open-id-connect-provider \
    --url https://token.actions.githubusercontent.com \
    --client-id-list sts.amazonaws.com \
    --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1 >/dev/null
  echo "created GitHub OIDC provider"
fi

# GitHub issues an *immutable* subject claim that embeds numeric owner and repo ids:
#   repo:owner@1234/name@5678:ref:refs/heads/main
# Every trust-policy example published for AWS uses the plain repo:owner/name form,
# which silently fails to match. Derive the real one.
OWNER="${REPO%%/*}"; NAME="${REPO##*/}"
OWNER_ID=$(gh api "/users/$OWNER" --jq .id 2>/dev/null || echo "")
REPO_ID=$(gh api "/repos/$REPO" --jq .id 2>/dev/null || echo "")
if [ -n "$OWNER_ID" ] && [ -n "$REPO_ID" ]; then
  SUB="repo:$OWNER@$OWNER_ID/$NAME@$REPO_ID:ref:refs/heads/main"
else
  echo "warning: gh unavailable, falling back to the mutable sub form" >&2
  SUB="repo:$REPO:ref:refs/heads/main"
fi
echo "trusting sub $SUB"

cat > /tmp/trust.json <<JSON
{"Version":"2012-10-17","Statement":[{
  "Effect":"Allow","Principal":{"Federated":"$OIDC_ARN"},
  "Action":"sts:AssumeRoleWithWebIdentity",
  "Condition":{"StringEquals":{
    "token.actions.githubusercontent.com:aud":"sts.amazonaws.com",
    "token.actions.githubusercontent.com:sub":"$SUB"
  }}}]}
JSON
if ! aws iam get-role --role-name "$ROLE" >/dev/null 2>&1; then
  aws iam create-role --role-name "$ROLE" \
    --assume-role-policy-document file:///tmp/trust.json >/dev/null
  echo "created role $ROLE"
else
  aws iam update-assume-role-policy --role-name "$ROLE" \
    --policy-document file:///tmp/trust.json
fi

cat > /tmp/perm.json <<JSON
{"Version":"2012-10-17","Statement":[
 {"Effect":"Allow","Action":["s3:ListBucket"],"Resource":"arn:aws:s3:::$BUCKET"},
 {"Effect":"Allow","Action":["s3:PutObject","s3:DeleteObject"],"Resource":"arn:aws:s3:::$BUCKET/*"},
 {"Effect":"Allow","Action":["cloudfront:CreateInvalidation"],
  "Resource":"arn:aws:cloudfront::$ACCOUNT:distribution/$DIST_ID"}
]}
JSON
aws iam put-role-policy --role-name "$ROLE" --policy-name deploy --policy-document file:///tmp/perm.json

echo
echo "=============================================================="
echo "Set these on the repo (Settings > Secrets and variables > Actions)"
echo
echo "  Variables:"
echo "    AWS_REGION                 $REGION"
echo "    S3_BUCKET                  $BUCKET"
echo "    CLOUDFRONT_DISTRIBUTION_ID $DIST_ID"
echo "    SITE_URL                   https://$DIST_DOMAIN"
echo
echo "  Secret:"
echo "    AWS_DEPLOY_ROLE_ARN        arn:aws:iam::$ACCOUNT:role/$ROLE"
echo
echo "  Site will be at: https://$DIST_DOMAIN"
echo "=============================================================="
