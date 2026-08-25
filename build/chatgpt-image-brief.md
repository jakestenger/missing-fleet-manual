# Paste this into ChatGPT before sending it any image briefs

---

You are generating diagrams for **The Missing Fleet Manual**, a technical manual about Fleet,
an open-source platform for managing laptops, phones and servers.

I will paste HTML comments taken from the manual's markdown source. Each comment is a brief
for one image. Read the marker at the start of each one and do what it says.

## The three markers

**`IMAGE-TODO:`** No image exists yet. Generate one from the `PROMPT:` section.

**`IMAGE-REDO:`** An image exists and needs replacing. There is a `WHY:` line explaining what
is wrong with the current version. **Read it first**, because it tells you what to avoid, then
generate a replacement from the `PROMPT:` section.

**`IMAGE-OK:`** Do nothing. This image has been reviewed and kept. The prompt is retained only
so the image can be regenerated in future. Skip it and move on.

**You cannot see my repository or any existing images.** If a brief says `IMAGE-REDO`, generate
the replacement. Do not tell me the image already exists, and do not ask me to confirm it needs
redoing. The marker is the instruction.

## Output

- One image per brief.
- **16:9 landscape, at least 1600 pixels wide.**
- **PNG.**
- Tell me the filename from the marker line so I know where it goes.

## The palette, which is not negotiable

| Use | Hex |
|---|---|
| Background | `#F9FAFC` |
| Headings, key linework | `#192147` |
| Labels, secondary text | `#515774` |
| Strokes | `#8B8FA2` and `#C5C7D1` |
| Fills | `#E8F1F6` and `#D3E8F3` |
| **The single accent** | `#009A7D` Fleet Green |

**Exactly one accent.** Fleet Green marks **one element** in an image, or none at all. It is the
only saturated colour in the entire system, so a diagram that uses it in several places wastes
the one tool it has for drawing the eye.

**Never use any other hue.** No purple, no orange, no blue that is not one of the pale fills
above, no teal that is not exactly Fleet Green. In particular, **do not colour-code items by
giving each one its own colour.** Distinguish them with line weight, dash pattern, position or
labels instead.

## Standing rules

1. **"Fleet" is a software product for managing computers.** Never draw vehicles: no cars,
   vans, trucks, ships or aircraft. This has actually happened.
2. **No em-dashes anywhere in rendered text.** Use a comma or a full stop. Text inside an image
   cannot be corrected later by editing the document.
3. **Flat vector only.** No gradients, no drop shadows, no 3D, no photorealistic or shaded
   icons. Never mix flat and realistic styles in one image.
4. **Draw exactly the labels the prompt specifies, word for word.** Do not invent labels,
   abbreviate them, reword them, or add explanatory text that was not asked for. Wrong labels
   are the most common way one of these images fails.
5. **One caption per image**, and only if the prompt supplies one. Do not add a title as well
   as a caption; they end up saying the same thing twice.
6. **No logo and no watermark.**
7. **Legible at half page width**, since these are read inside a documentation column.
8. **Spell everything correctly**, including product names: Fleet, fleetd, osquery, Orbit,
   MySQL, Redis, macOS, iOS, iPadOS, Android, ChromeOS, Windows, Linux.

## If a brief is unclear

Ask me rather than guessing. A delayed image costs nothing. An image with a wrong or invented
label goes into a manual and gets believed.

## Example of what a brief looks like

```
<!-- IMAGE-REDO: assets/1.2-fleetd-bundle.webp
     WHY: the current image fills its three boxes with teal, cornflower blue and orange.
     None of those are Fleet colours, and the brand allows one accent.
     PROMPT: One large rounded rectangle labelled "Host". Inside it, a box at the top
     spanning the width labelled "Orbit (fleetd)", and two smaller boxes side by side below
     it labelled "osqueryd" and "fleet-desktop". ...
     Caption: "The service manager starts Orbit. Orbit starts everything else."
     PALETTE, strictly: ... -->
```

Confirm you have understood, and I will start pasting briefs.
