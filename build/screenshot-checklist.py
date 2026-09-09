#!/usr/bin/env python3
"""Build the Parts 0–V screenshot checklist from chapter comments.

Run from any directory. Existing checked capture IDs and capture-record notes are preserved. --check checks
synchronization without writing. No screenshots or application actions are performed.
"""
from pathlib import Path
import argparse
import re
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'SCREENSHOTS.md'
EDITIONS = {'4.91': ROOT / 'manual', '4.90': ROOT / 'website/versioned_docs/version-4.90'}
FIELDS = ('purpose', 'prepare', 'capture', 'frame', 'edition', 'privacy', 'filename')
PARTS = ['0 — Introduction', 'I — Foundations', 'II — Administer and deploy Fleet',
         'III — Connect devices', 'IV — Know your devices', 'V — Manage devices']
ID = r'SS-\d+\.\d+-\d{2}'
COMMENT = re.compile(r'<!--.*?-->', re.S)


def slug(text):
    return re.sub(r'\s+', '-', re.sub(r'[^\w\s-]', '', text.lower().replace('`', ''))).strip('-')


def code_key(code):
    return tuple(map(int, code.split('.')))


def placement(path, text, offset, edition):
    prior = COMMENT.sub('', text[:offset])
    headings = re.findall(r'^#{1,6} (.+)$', prior, re.M)
    assert headings, path
    return {'path': path, 'heading': headings[-1], 'edition': edition}


def link(place):
    return f"[{place['edition']}]({place['path'].relative_to(ROOT).as_posix()}#{slug(place['heading'])})"


def read_briefs():
    briefs, chapters, reuses = {}, {}, defaultdict(list)
    for edition, root in EDITIONS.items():
        seen = set()
        for path in sorted(root.glob('0[0-5]*/*.md')):
            text = path.read_text()
            code = path.name.split('-')[0]
            title = re.search(r'^# (.+)$', COMMENT.sub('', text), re.M).group(1)
            chapters.setdefault(code, {'title': title, 'ids': [], 'reuse': []})
            for comment in COMMENT.finditer(text):
                content = comment.group()
                match = re.match(r'<!-- SCREENSHOT: (' + ID + r') \| (.+)\n', content)
                if match:
                    ident, title = match.groups()
                    assert ident not in seen, f'duplicate {edition} {ident}'
                    seen.add(ident)
                    fields = dict((k.lower(), v.strip()) for k, v in re.findall(
                        r'^\s+([A-Z]+): (.+)$', content, re.M))
                    assert all(fields.get(k) for k in FIELDS), f'incomplete {ident}'
                    data = {'id': ident, 'title': title, 'chapter': code, **fields}
                    if ident in briefs:
                        assert all(briefs[ident][k] == data[k] for k in data), f'edition brief drift: {ident}'
                    else:
                        assert edition == '4.91', f'brief only in frozen edition: {ident}'
                        briefs[ident] = {**data, 'places': []}
                        chapters[code]['ids'].append(ident)
                    briefs[ident]['places'].append(placement(path, text, comment.start(), edition))
                elif content.startswith('<!-- SCREENSHOT-REUSE:'):
                    note = content.removeprefix('<!-- SCREENSHOT-REUSE:').removesuffix('-->').strip()
                    # Only the first sentence identifies reused captures. Later notes may
                    # mention a distinct brief that is already located in this chapter.
                    ids = re.findall(ID, note.split('. ', 1)[0])
                    assert ids, f'no reuse ID in {path}'
                    for ident in ids:
                        reuses[ident].append({**placement(path, text, comment.start(), edition), 'note': note, 'chapter': code})
                        if edition == '4.91':
                            chapters[code]['reuse'].append(ident)
                elif 'SCREENSHOT' in content:
                    raise ValueError(f'Unnormalized screenshot brief in {path}: {content[:100]}')
    assert not (set(reuses) - set(briefs)), f'unresolved reuse: {set(reuses) - set(briefs)}'
    return briefs, chapters, reuses


def render(briefs, chapters, reuses, checked, capture_notes):
    reuse_count = sum(1 for ps in reuses.values() for p in ps if p['edition'] == '4.91')
    lines = ['# Screenshot capture checklist: Parts 0–V', '',
        f'{len(briefs)} capture briefs, plus {reuse_count} reuse placements in the living edition. Each brief describes a useful view; some call for two separate frames. The same captures can serve the frozen edition when its visible behavior and controls match.', '',
        'The chapter comments are the source of truth. This checklist covers the company and product introductions and every remaining chapter in Parts 0–V. The approved introduction prose is retained. Chapters without a new screenshot use text or existing diagrams where those explain the subject more clearly.', '',
        '## Capture conventions', '',
        '- Use a demo instance whenever practical. Dogfood is suitable for existing, non-sensitive views; stage enrollment, failures, configuration changes, and state-changing actions on disposable test devices.',
        '- Record the Fleet server version, fleetd version where relevant, device OS, date, and source instance with each capture. If Dogfood is newer than the book, compare the visible controls with the pinned edition before reusing the image. Capture 4.90 separately where it differs. The three briefs marked **4.91 only** do not belong in the frozen 4.90 edition.',
        '- Use the same Fleet theme, browser zoom, and approximate viewport for desktop captures. A 1440-pixel-wide viewport at 100% zoom with a 2× capture is a useful starting point. Keep native product fonts, colors, labels, and proportions. Device setup screens should retain their actual OS appearance.',
        '- Save clean PNGs. Crop around the useful content while retaining enough page, fleet, or host context to orient the reader. Check that essential labels remain readable at about 720 pixels wide; use a detail crop or second frame when needed.',
        '- Keep credentials, enrollment links, QR codes, My Device URLs, personal information, and private company data out of the frame. Use demo identities and non-sensitive output. Opaque redaction is acceptable when necessary; label a redaction rather than replacing a value with invented UI. Never photograph a revealed recovery key.',
        '- Capture each real state separately. Do not combine controls or statuses that never coexist, redraw product UI, or add fictional success messages. Keep explanations in the caption. Use at most a few numbered callouts if the accepted image needs them.',
        '- Use the proposed filename for one frame. For multiple frames add descriptive suffixes such as `-settings`, `-result`, or `-detail`; add `-4.90` for a distinct frozen-edition capture. Keep the SS ID in every filename so the artwork can be matched to its chapter comment.',
        '- Check off a brief when its requested primary frames are captured. Note omitted optional frames and record the saved paths/version in your working copy. Artwork still needs review, alt text, and insertion into the chapter; these comments do not create visible placeholders.', '',
        '## Chapter coverage', '',
        '| Chapter | Topic | New briefs | Reuse |', '|---|---|---|---|']
    for code in sorted(chapters, key=code_key):
        chapter = chapters[code]
        refs = lambda ids: ', '.join(f'[{ident}](#{slug(ident)})' for ident in sorted(ids)) or '—'
        lines.append(f"| {code} | {chapter['title']} | {refs(chapter['ids'])} | {refs(chapter['reuse'])} |")
    for part in range(6):
        lines += ['', f'## Part {PARTS[part]}', '']
        for ident, record in sorted(briefs.items(), key=lambda pair: (*code_key(pair[1]['chapter']), pair[0])):
            if code_key(record['chapter'])[0] != part:
                continue
            places = record['places']
            lines += [f'### {ident}', '', f"- [{'x' if ident in checked else ' '}] **{ident}: {record['title']}**", '',
                f"**Place:** Chapter {record['chapter']}, “{places[0]['heading']}” ({', '.join(link(p) for p in places)}).", '',
                f"**Purpose:** {record['purpose']}", '', f"**Prepare:** {record['prepare']}", '',
                f"**Capture:** {record['capture']}", '', f"**Frame:** {record['frame']}", '',
                f"**Edition:** {record['edition']}", '', f"**Privacy:** {record['privacy']}", '',
                f"**Filename:** `{record['filename']}`", '']
            grouped = defaultdict(list)
            for reuse in reuses.get(ident, []):
                grouped[(reuse['chapter'], reuse['heading'], reuse['note'])].append(reuse)
            for (code, heading, note), ps in sorted(grouped.items(), key=lambda item: code_key(item[0][0])):
                lines += [f"**Also place:** Chapter {code}, “{heading}” ({', '.join(link(p) for p in ps)}). {note}", '']
            lines += ['**Capture record:** ' + capture_notes.get(ident, 'Fleet version · fleetd/OS where relevant · date · saved file(s) · optional frames or differences.'), '']
    lines += ['## Maintaining this list', '',
        'Edit the structured `SCREENSHOT:` or `SCREENSHOT-REUSE:` comments in the relevant chapters, keeping the edition-specific content accurate. Then run `python3 build/screenshot-checklist.py` from the repository. It preserves checked SS IDs and the single-paragraph Capture record notes in this file. Use `--check` to verify that the list matches the comments without changing it.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    old = OUTPUT.read_text() if OUTPUT.exists() else ''
    checked = set(re.findall(r'^- \[[xX]\] \*\*(' + ID + r'):', old, re.M))
    capture_notes = {}
    for section in re.split(r'^### ', old, flags=re.M)[1:]:
        ident = section.splitlines()[0]
        note = re.search(r'^\*\*Capture record:\*\* (.+)$', section, re.M)
        if note:
            capture_notes[ident] = note.group(1)
    briefs, chapters, reuses = read_briefs()
    result = render(briefs, chapters, reuses, checked, capture_notes)
    if args.check:
        if old != result:
            raise SystemExit('SCREENSHOTS.md is out of sync; run build/screenshot-checklist.py')
        print(f'Checklist synchronized: {len(briefs)} briefs across {len(chapters)} chapters')
    else:
        OUTPUT.write_text(result)
        print(f'Wrote {OUTPUT.name}: {len(briefs)} briefs across {len(chapters)} chapters')


if __name__ == '__main__':
    main()
