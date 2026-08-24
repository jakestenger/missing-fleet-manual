#!/usr/bin/env python3
"""Verify every cross-reference in the manual resolves.

Three classes of breakage have actually happened in this repo, so all three are checked:
  1. A link to a section file that does not exist.
  2. A #anchor into a heading that was later renamed. Silent: the page still loads.
  3. An image reference with no file behind it. This is a hard webpack failure at build.

Exit code 1 on any failure, so CI blocks the merge.
"""
import io, os, re, sys, glob

def slug(h):
    s = re.sub(r'`', '', h.strip().lower())
    s = re.sub(r'[^\w\s-]', '', s)
    return re.sub(r'\s+', '-', s).strip('-')

def strip_comments(t):
    return re.sub(r'<!--.*?-->', '', t, flags=re.S)

def main():
    files = sorted(glob.glob('manual/*/*.md'))
    if not files:
        print("no markdown found under manual/*/*.md"); return 1

    heads = {}
    for f in files:
        heads[f] = {slug(l.lstrip('#')) for l in io.open(f, encoding='utf-8') if l.startswith('#')}

    fails = []
    for f in files:
        raw = io.open(f, encoding='utf-8').read()
        body = strip_comments(raw)          # parked refs in comments are not live
        d = os.path.dirname(f)

        for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', body):
            u = m.group(1)
            if u.startswith(('http://', 'https://', 'data:')):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(d, u))):
                fails.append("missing image   %s -> %s" % (f, u))

        for m in re.finditer(r'(?<!!)\[[^\]]*\]\(([^)#]*\.md)(?:#([a-z0-9-]+))?\)', body):
            target, anc = m.group(1), m.group(2)
            tf = os.path.normpath(os.path.join(d, target))
            if not os.path.exists(tf):
                fails.append("missing file    %s -> %s" % (f, target)); continue
            if anc and tf in heads and anc not in heads[tf]:
                fails.append("missing anchor  %s -> %s#%s" % (f, target, anc))

        for m in re.finditer(r'(?<!!)\[[^\]]*\]\(#([a-z0-9-]+)\)', body):
            if m.group(1) not in heads[f]:
                fails.append("missing anchor  %s -> #%s" % (f, m.group(1)))

    for x in fails:
        print("  FAIL " + x)
    print("checked %d files: %d problems" % (len(files), len(fails)))
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
