import React from 'react';
import OriginalImg from '@theme-original/MDXComponents/Img';
import ThemedImage from '@theme/ThemedImage';

import explanationLight from '!!url-loader?limit=10000!@site/../manual/_assets/icons/explanation-light.svg';
import explanationDark from '!!url-loader?limit=10000!@site/../manual/_assets/icons/explanation-dark.svg';
import howtoLight from '!!url-loader?limit=10000!@site/../manual/_assets/icons/howto-light.svg';
import howtoDark from '!!url-loader?limit=10000!@site/../manual/_assets/icons/howto-dark.svg';
import referenceLight from '!!url-loader?limit=10000!@site/../manual/_assets/icons/reference-light.svg';
import referenceDark from '!!url-loader?limit=10000!@site/../manual/_assets/icons/reference-dark.svg';
import troubleshootingLight from '!!url-loader?limit=10000!@site/../manual/_assets/icons/troubleshooting-light.svg';
import troubleshootingDark from '!!url-loader?limit=10000!@site/../manual/_assets/icons/troubleshooting-dark.svg';

// Load URLs explicitly: the site’s SVGR plugin otherwise imports React components.
// Match the same inlined SVG data URLs that the Markdown image loader produces. Identical
// frozen-edition assets resolve to the same URL. Ordinary images use Docusaurus's
// original renderer, and Markdown outside the site retains the light fallback.
const icons = new Map([
  [explanationLight, {light: explanationLight, dark: explanationDark}],
  [howtoLight, {light: howtoLight, dark: howtoDark}],
  [referenceLight, {light: referenceLight, dark: referenceDark}],
  [troubleshootingLight, {light: troubleshootingLight, dark: troubleshootingDark}],
]);

export default function Img({src, alt, className, ...props}) {
  const sources = icons.get(src);
  if (!sources) {
    return <OriginalImg src={src} alt={alt} className={className} {...props} />;
  }

  return (
    <ThemedImage
      {...props}
      sources={sources}
      alt={alt}
      title={alt || undefined}
      width={28}
      height={28}
      className={['content-kind-icon', className].filter(Boolean).join(' ')}
    />
  );
}
