# Content-type icons

| Category | Shape | Markdown asset |
|---|---|---|
| Explanation | Fleet's official six-dot mark | `explanation-light.svg` |
| How-to | Checklist | `howto-light.svg` |
| Reference | Reference book | `reference-light.svg` |
| Troubleshooting | Magnifying glass | `troubleshooting-light.svg` |

Each has a matching `-dark.svg`. Use a relative Markdown image with the category
as alt text, for example `![Reference](../_assets/icons/reference-light.svg)`.
Docusaurus's `website/src/theme/MDXComponents/Img/index.js` selects the variant
using the reader's site theme. Other images keep the standard renderer.

The Explanation mark's six paths and colors come unchanged from Fleet's
[official press-kit SVG at fleet-v4.90.0](https://github.com/fleetdm/fleet/blob/fleet-v4.90.0/website/assets/images/press-kit/fleet-logo-mark.svg).
The source SVG is identical in Fleet 4.90.0 and 4.91.0. Its viewBox here crops
excess canvas whitespace while preserving the dot geometry.
The mark is the same color in both themes. Fleet retains ownership of its logo.

The three companion icons were drawn for this manual. Their structural strokes
are `#192147` in light mode and `#F9FAFC` in dark mode, with round caps and joins.
Their colored dots use the logo palette: blue `#5CABDF`, lavender `#C98DEF`, mint
`#3AEFC4`, apricot `#FAA669`, and rose `#D66C7B`. The logo also uses green `#63C740`.
Dots support the visual family; shape and alt text carry the category meaning.

All eight SVGs have transparent backgrounds and a 28 px intrinsic size. Keep
them below the site's 10 KB inline-image limit and synchronize the copies under
`website/versioned_docs/version-4.90/_assets/icons/` when updating the set. The
theme renderer matches the asset URLs, so identical edition copies are required.
Browser printing renders the marks in black for legibility on white paper.

Edit these SVGs directly. Do not regenerate the Fleet logo or turn the icons into
raster images. Placement guidance lives in the root `STYLE.md`.
