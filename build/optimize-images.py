#!/usr/bin/env python3
"""Convert generated PNG artwork to WebP and repoint the markdown that references it.

Generated diagrams arrive as ~1MB PNGs. They carry gradients, so a PNG palette barely
helps, but WebP at q88 lands around 5% of the original with no visible loss and no
resizing. Run after dropping new artwork in:  python3 build/optimize-images.py apply
"""
import io, os, re, sys, glob
from PIL import Image

QUALITY = 88

def main(apply):
    pngs = sorted(glob.glob("manual/*/assets/*.png"))
    if not pngs:
        print("no PNGs found"); return
    before = after = 0
    renames = {}
    for p in pngs:
        w = p[:-4] + ".webp"
        b = os.path.getsize(p); before += b
        if apply:
            Image.open(p).convert("RGB").save(w, "WEBP", quality=QUALITY, method=6)
            a = os.path.getsize(w); os.remove(p)
        else:
            im = Image.open(p).convert("RGB")
            im.save("/tmp/_probe.webp", "WEBP", quality=QUALITY, method=6)
            a = os.path.getsize("/tmp/_probe.webp")
        after += a
        renames[os.path.basename(p)] = os.path.basename(w)
        print("  %-46s %5dKB -> %4dKB" % (os.path.basename(p), b//1024, a//1024))

    touched = 0
    for md in glob.glob("manual/*/*.md"):
        t = io.open(md, encoding="utf-8").read(); orig = t
        for old, new in renames.items():
            t = t.replace(old, new)
        if t != orig:
            touched += 1
            if apply:
                io.open(md, "w", encoding="utf-8").write(t)
    print("%s: %d images, %.1fMB -> %.1fMB (%.0f%% smaller), %d markdown files repointed"
          % ("APPLIED" if apply else "DRY RUN", len(pngs), before/1e6, after/1e6,
             100*(1-after/before), touched))

if __name__ == "__main__":
    main(len(sys.argv) > 1 and sys.argv[1] == "apply")
