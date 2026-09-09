#!/usr/bin/env python3
"""Package a rendered, inspected part for owner review; never accept or install its images.

Usage: python3 research/visual-reviews/package-review.py part-2 02 'Part II'
Run only after inspecting every candidate. Preserves visible chapter content.
"""
from pathlib import Path
import re,json,sys,shutil,html
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
OUTPUT=Path('/Users/jake/Documents/Codex/2026-09-08/ca/outputs/manual-visuals')
folder,prefix,part_title=sys.argv[1:4]
part=ROOT/folder
inventory=json.loads((ROOT/'remaining-briefs.json').read_text())
jobs=[j for j in inventory if j['part'].startswith(prefix+'-')]
assert jobs,'No matching briefs'
blocker_file=part/'capture-blockers.json'
blockers=json.loads(blocker_file.read_text()) if blocker_file.exists() else []
blocked={j['asset']:j for j in blockers}
assert len(blocked)==len(blockers)
assert set(blocked)<=set(j['asset'] for j in jobs)
for j in jobs:
    if j['asset'] in blocked:
        assert 'SCREENSHOT:' in j['brief'], 'Only documented authentic-capture blockers may be excluded'
        assert blocked[j['asset']]['reason']
        assert not (part/'assets'/Path(j['asset']).name).exists()
        j.update(status='awaiting authentic demo capture',blocker=blocked[j['asset']]['reason'])
jobs=[j for j in jobs if j['asset'] not in blocked]
def order(j):
    s=Path(j['chapter']).name.split('-')[0].split('.')
    return (int(s[-1]),j['asset'])
jobs.sort(key=order)
# Check every candidate before making any chapter edits.
for j in jobs:assert (part/'assets'/Path(j['asset']).name).is_file(),j['asset']
records=[]
term='     TERMINOLOGY: Fleet is the company, product, or server. Host groups are lowercase\n     fleet/fleets, including headings and labels. Do not call these groups teams. Preserve\n     exact code/API identifiers. These instructions are not text to render.\n'
for j in jobs:
    f=REPO/j['chapter'];text=f.read_text();name=Path(j['asset']).stem
    pat=re.compile(r'<!-- IMAGE-(TODO|REDO): '+re.escape(j['asset'])+r'\n[\s\S]*?-->')
    m=pat.search(text);assert m,j['asset']
    comment=m.group()
    for old,new in [('Fleet-scoped','fleet-scoped'),('Fleet A','fleet A'),('Fleet B','fleet B'),('Fleet: Workstations','fleet: Workstations'),('Fleet: Kiosks','fleet: Kiosks')]:comment=comment.replace(old,new)
    if '     TERMINOLOGY:' not in comment:
        if '     DESIGN:' in comment:comment=comment.replace('     DESIGN:',term+'     DESIGN:',1)
        else:comment=comment.replace('-->',term+'-->')
    if '     CANDIDATE:' not in comment:comment=comment.replace('-->',f'     CANDIDATE: ../../research/visual-reviews/{folder}/assets/{name}.webp\n     Rendered and inspected for the overnight batch; awaiting final joint review.\n-->')
    updated=text[:m.start()]+comment+text[m.end():]
    visible=lambda s:re.sub(r'<!--[\s\S]*?-->','',s)
    assert visible(updated)==visible(text)
    f.write_text(updated)
    q=re.search(r'QUESTION: ([\s\S]*?)(?=\n     [A-Z]+:)',comment)
    q=' '.join(q.group(1).split()) if q else name.split('-',1)[-1].replace('-',' ').capitalize()
    note=re.search(r'NOTE: ([\s\S]*?)(?=\n     CANDIDATE:|-->)',comment)
    note=' '.join(note.group(1).split()) if note else 'Replacement candidate; compare with the current image before acceptance.'
    method='Editable SVG' if (part/'assets'/(name+'.svg')).exists() else 'Built-in image generation'
    source='assets/'+name+('.svg' if method=='Editable SVG' else '.png')
    if j['state']=='REDO':
        old=f.parent/j['asset'];assert old.exists()
        shutil.copy2(old,part/'assets'/(name+'-before.webp'))
    j['brief']=comment.split('\n',1)[1].removesuffix('-->')
    records.append({**j,'status':'candidate ready; pending final joint review','question':q,'method':method,'candidate':'assets/'+name+'.webp','source':source,'editor_note':note,'chapter_comment':comment})
    j.update(status='candidate ready; pending final joint review',candidate=f'{folder}/assets/{name}.webp')
(part/'briefs.json').write_text(json.dumps(records,indent=2)+'\n')
(ROOT/'remaining-briefs.json').write_text(json.dumps(inventory,indent=2)+'\n')
css=re.search(r'<style>([\s\S]*?)</style>',(ROOT/'part-0-1/index.html').read_text()).group(1)
esc=html.escape
cards=[]
for blocker in blockers:
    cards.append(f'<article><header><p class="eyebrow">Capture outstanding</p><h2>{esc(Path(blocker["asset"]).stem)}</h2></header><p>{esc(blocker["reason"])}</p><p><a href="capture-blockers.json">Capture requirements and observed blockers</a></p></article>')
for i,j in enumerate(records):
    name=Path(j['asset']).stem;before=''
    if j['state']=='REDO':before=f'<details><summary>Compare the current book image</summary><img class="art" src="assets/{esc(name)}-before.webp" alt="Previous book artwork for comparison."></details>'
    cards.append(f'<article id="figure-{i+1}"><header><p class="eyebrow">{esc(name.split("-")[0])} · {esc(j["method"])} · Pending review</p><h2>{esc(j["question"])}</h2></header><figure><img class="art" src="{esc(j["candidate"])}" alt="{esc(j["question"])}"><figcaption>{esc(j["editor_note"])}</figcaption></figure><div class="links"><a href="{esc(j["candidate"])}">Full-size WebP</a><a href="{esc(j["source"])}">{esc(j["method"])} source</a></div>{before}</article>')
page=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(part_title)} · Fleet manual visual review</title><style>{css}</style><main><p class="eyebrow">The Missing Fleet Manual · Overnight visual production</p><h1>{esc(part_title)}: visual review</h1><p class="intro">{len(records)} candidates, prepared for the final manual-wide review. Fleet is the product, company, or server; host groups are lowercase fleet/fleets. Published chapter prose and artwork remain in place.</p><p><a href="../index.html">All parts</a> · <a href="briefs.json">Full chapter briefs</a></p><div class="controls"><label><input id="gray" type="checkbox"> Grayscale</label><label><input id="wide" type="checkbox"> Expand artwork</label><span>Default: 720 px</span></div>'+''.join(cards)+'</main><script>for(const name of ["gray","wide"])document.getElementById(name).addEventListener("change",e=>document.body.classList.toggle(name,e.target.checked));</script></html>'
(part/'index.html').write_text(page)
# Build the collection index from packaged galleries; unresolved captures remain explicit.
batches=[]
for child in ROOT.iterdir():
    if child.is_dir() and (child/'index.html').exists() and (child/'briefs.json').exists():
        count=len(json.loads((child/'briefs.json').read_text()))
        batches.append((child.name,count))
batches.sort(key=lambda x:(x[0]=='appendices',x[0]))
links=''.join(f'<article><h2><a href="{esc(name)}/index.html">{esc(name.replace("part-","Part "))}</a></h2><p>{count} candidates'+(' · Capture outstanding' if (ROOT/name/'capture-blockers.json').exists() and json.loads((ROOT/name/'capture-blockers.json').read_text()) else '')+'</p></article>' for name,count in batches)
(ROOT/'index.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fleet manual · Complete visual review</title><style>{css}</style><main><p class="eyebrow">The Missing Fleet Manual</p><h1>Visual review collection</h1><p class="intro">{sum(c for _,c in batches)} candidates across {len(batches)} batches. Outstanding captures are listed with their batch. More batches will appear as overnight production finishes. All artwork remains pending final installation.</p>{links}<p><a href="overnight-progress.md">Production progress</a></p></main></html>')
OUTPUT.mkdir(parents=True,exist_ok=True)
shutil.copytree(ROOT,OUTPUT,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
print(f'Packaged {len(records)} candidates; collection now has {sum(c for _,c in batches)}.')
