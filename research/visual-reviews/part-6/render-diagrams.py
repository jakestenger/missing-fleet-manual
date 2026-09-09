#!/usr/bin/env python3
"""Part VI native candidates; shared Fleet visual primitives."""
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('base',Path(__file__).resolve().parents[1]/'part-0-1/render-diagrams.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.OUT=Path(__file__).resolve().parent/'assets'
D=b.Diagram
NAVY,SLATE,MUTED,BORDER,BG,PALE,BLUE,PINK,APRICOT=b.NAVY,b.SLATE,b.MUTED,b.BORDER,b.BG,b.PALE,b.BLUE,b.PINK,b.APRICOT
MINT='#D8FBEF'
def text(d,x,y,t,size=30):d.text(x,y,t,size,500,SLATE,anchor='start')
def title(d,t):text(d,48,80,t,40)
def paths():
 d=D('6.1-paths-to-one-control-plane',1064,'GitOps, fleetctl and custom clients converge on the REST API; events travel outward through webhooks.')
 title(d,'Clients reach one Fleet control plane')
 for y,label,client in [(180,'Configuration\nrepository','fleetctl gitops'),(412,'Operator or\npipeline','fleetctl')]:
  d.node(48,y,320,128,label,size=34);d.path([(368,y+64),(448,y+64)]);d.node(448,y,296,128,client,size=32)
 d.node(48,644,320,128,'Custom client',size=34)
 d.path([(744,244),(816,244),(816,360),(904,360)])
 d.path([(744,476),(816,476),(816,440),(904,440)])
 d.path([(368,708),(816,708),(816,520),(904,520)])
 d.node(904,300,448,264,'Fleet REST API\nOne control plane',anchor=True,size=38)
 d.text(632,820,['No field ownership','or stale-write check'],30)
 d.rect(904,644,448,160,PALE,BORDER);d.text(1128,704,['Fleet configuration','Queued device actions'],32)
 d.path([(1128,564),(1128,644)])
 for x,label in [(48,'Fleet events'),(504,'Outbound webhook'),(960,'External receiver\nor workflow')]:d.node(x,912,392,112,label,fill=BLUE,size=32)
 d.path([(440,968),(504,968)]);d.path([(896,968),(960,968)])
 d.save()
def ambiguous():
 d=D('6.1-ambiguous-write-reconcile',1392,'An ambiguous write is reconciled against current state before bounded retry or escalation; acceptance and device outcome are separate.')
 title(d,'Read current state after an ambiguous write')
 d.node(48,176,352,120,'Request sent',anchor=True,size=38)
 d.path([(400,236),(512,236)]);d.node(512,176,352,120,'Clear response',size=34)
 d.path([(224,296),(224,392)]);d.node(48,392,352,144,'Timeout /\nunknown outcome',fill=APRICOT,size=34)
 d.path([(400,464),(512,464)])
 d.node(512,376,840,176,'Read current state\nRetained identifier or documented scoped key',size=32)
 d.text(932,614,'Already pending: evidence to inspect',30)
 for y,label,dest,fill in [(708,'Intended result observed','Verify convergence',MINT),(916,'Definitely absent AND\nendpoint safe to repeat','Bounded retry policy',APRICOT),(1124,'Still ambiguous','Stop / escalate',PINK)]:
  d.node(416,y,512,120,label,size=32);d.node(1040,y,312,120,dest,fill=fill,size=30);d.path([(928,y+60),(1040,y+60)])
 d.path([(672,552),(672,660),(360,660),(360,1184)],MUTED,arrow=False)
 for y in [768,976,1184]:d.path([(360,y),(416,y)])
 d.text(700,1336,'Verify request acceptance and device outcome separately',30)
 d.save()
def execution():
 d=D('6.2-execution-model',2480,'fleetctl GitOps performs client-side preflight then ordered API phases; a failure preserves earlier changes and skips later work.')
 title(d,'A GitOps invocation commits through separate requests')
 d.rect(48,152,620,416,PALE,BORDER);text(d,80,210,'Configuration repository',36)
 for y,label in [(270,'default.yml'),(334,'fleets/workstations.yml'),(398,'fleets/servers.yml'),(462,'fleets/unassigned.yml')]:d.text(80,y,label,30,anchor='start',mono=True)
 text(d,80,506,['unassigned.yml may be absent;','that changes behavior'],28)
 d.path([(668,360),(764,360)])
 d.rect(764,152,588,416,NAVY,NAVY)
 d.text(1058,220,['fleetctl gitops','Client-side orchestrator'],36,600,BG)
 d.text(796,334,['Parse all supplied YAML','Resolve environment and files','Read current Fleet state','Compute operations'],30,400,BG,anchor='start',leading=54)
 d.path([(1058,568),(1058,600),(24,600),(24,780),(160,780)])
 text(d,48,650,'Fleet API · ordered phases',36)
 text(d,48,706,'Each API request commits independently; a file can require several requests',28)
 # A vertical phase rail describes order, not a transaction or per-file atomicity.
 specs=[(780,'1  Global configuration, forced first','Some unassigned.yml controls are folded into this phase',MINT),
 (976,'2  First named fleet file','Remaining supplied files follow invocation order',MINT),
 (1172,'Second named fleet file: failure','Earlier changes remain applied',PINK),
 (1368,'Explicit unassigned.yml, wherever supplied','Not reached in this example; never automatically moved last',PALE),
 (1564,'3  Restore ABM / App Store assignments','New fleet referenced; Premium multi-file run; deferred apps follow',PALE),
 (1760,'4  Delete absent fleets (optional)','Compare live fleets with files supplied in this invocation',PALE),
 (1956,'5  Synthesized empty Unassigned apply','Conditional alternative: global file, no explicit unassigned.yml',PALE),
 (2152,'6  Deferred label and certificate-authority deletions','Not reached in this failed invocation',PALE)]
 for y,heading,note,fill in specs:
  d.rect(272,y,1080,144,fill,BORDER);text(d,304,y+54,heading,32);text(d,304,y+110,note,28)
 d.path([(160,780),(160,1244)],NAVY,arrow=False)
 d.path([(160,1244),(160,2224)],MUTED,dash='7 7',arrow=False)
 for y in [852,1048]:d.path([(160,y),(272,y)]);d.rect(218,y-10,20,20,'#009A7D','#009A7D',r=0)
 d.path([(160,1244),(272,1244)]);d.cross(224,1244,12)
 for y in [1440,1636,1832,2028,2224]:d.path([(160,y),(272,y)],MUTED,dash='7 7',arrow=False)
 d.text(96,1450,'Not',28);d.text(96,1488,'reached',28)
 d.text(700,2372,['No transaction / no automatic rollback','No server-side GitOps run record'],30)
 d.save()
def assignment():
 d=D('6.2-gitops-assignment-loss-window',1240,'A Premium multi-file apply may clear token assignments before fleet creation, leaving them cleared after an intervening failure.')
 title(d,'The GitOps assignment-loss window')
 text(d,48,148,'Premium multi-file run references a fleet that does not yet exist',30)
 for y,label in [(224,'Existing assignments'),(428,'Temporarily clear\nassignment lists'),(684,'Create / configure fleets'),(940,'Restore assignments')]:d.node(48,y,568,144,label,anchor=y==224,size=36)
 for y,end in [(368,428),(572,684),(828,940)]:d.path([(332,y),(332,end)])
 d.rect(664,428,688,456,APRICOT,BORDER);text(d,696,490,'Assignment-loss window',36)
 d.path([(616,756),(760,756)]);d.text(1032,624,'Failure',30)
 d.node(760,660,544,176,'Live assignments\nremain cleared',fill=PINK,size=36)
 d.node(760,940,544,244,'Inspect live state\nFix first failure\nRerun same complete commit\nand full file set\nVerify routing and associations',size=28)
 d.path([(1032,836),(1032,940)])
 d.path([(648,428),(648,940)],MUTED,arrow=False,width=3)
 d.save()
def prefixes():
 d=D('6.3-version-prefixes-per-module',1224,'Module and route availability determine usable version prefixes; latest is a registered path, not a redirect or frozen schema.')
 title(d,'Version prefixes are registered per module')
 d.node(48,324,320,176,'One API client',anchor=True,size=38)
 for y,heading,fill in [(172,'Core module',BLUE),(500,'Activities module',PALE)]:
  d.rect(616,y,736,252,fill,BORDER);text(d,648,y+60,heading,36)
  for x,label in [(648,'v1'),(856,'2022-04'),(1112,'latest')]:
   if y==500 and label=='2022-04':continue
   w=176 if label!='2022-04' else 208
   d.rect(x,y+92,w,76,PALE,BORDER);d.text(x+w/2,y+142,label,30,500,NAVY,mono=True)
  text(d,648,y+216,'Example route: 2022-04 or latest' if y==172 else 'Example route: v1 or latest',30)
 d.path([(368,380),(480,380),(480,388),(616,388)]);text(d,384,278,['Needs the','core route'],28)
 d.path([(368,444),(480,444),(480,716),(616,716)]);text(d,240,584,['Needs the','activities route'],28)
 d.path([(960,424),(960,500)],'#FAA669',dash='7 7',arrow=False)
 d.text(960,818,'No single dated prefix serves both example routes',28)
 d.text(700,888,'Prefixes select route availability, not response schema',30)
 options=["Use each route’s\ndocumented prefix","Use mixed prefixes\nin one client","Use latest everywhere\nwith release-pinned tests"]
 for x,t in zip([48,504,960],options):d.node(x,1024,392,144,t,size=30)
 d.path([(208,500),(208,956),(1156,956)],MUTED,arrow=False,width=2)
 for x in [244,700,1156]:d.path([(x,956),(x,1024)],MUTED,width=2)
 d.save()
def cursor():
 d=D('6.3-host-list-cursor',1088,'The host list can be traversed by ascending ID with explicit page size; a top-level page error rejects the whole page and live changes still require reconciliation.')
 title(d,'Walk the host list by ascending identifier')
 text(d,48,150,'Illustrative error-free pages · page size 3 · host-list endpoint',30)
 for y,request,result in [(232,'Start','11, 18, 24'),(492,'After 24','31, 40, 57'),(752,'After 57','63 · short page: stop')]:
  d.node(48,y,416,128,request+'\nPage size 3 + ID ascending',size=30)
  d.path([(464,y+64),(608,y+64)]);d.node(608,y,520,128,result,fill=BLUE,size=36)
  d.path([(1128,y+64),(1168,y+64)],MUTED,dash='7 7',arrow=False)
 d.path([(868,360),(868,410),(256,410),(256,492)])
 d.path([(868,620),(868,670),(256,670),(256,752)])
 d.rect(1168,192,184,752,APRICOT,BORDER)
 d.text(1260,318,['Top-level','error?'],28,500,NAVY)
 d.text(1260,456,['Reject','the whole','page'],28,500,NAVY)
 d.path([(48,976),(1352,976)],BORDER,arrow=False,width=2)
 d.text(700,1032,'Live dataset changes → reconcile if exactness matters',32)
 d.save()
def race():
 d=D('6.4-fleetctl-config-write-race',1304,'Two jobs can read the same configuration snapshot and overwrite one another; separate files remove their shared write edge.')
 title(d,'Concurrent fleetctl configuration writes can lose changes')
 text(d,48,156,'Shared file · illustrative time runs downward',32)
 for x,label in [(208,'Job A'),(700,'Shared config'),(1192,'Job B')]:
  d.node(x-160,196,320,96,label,size=34);d.path([(x,292),(x,784)],MUTED,dash='7 7',arrow=False,width=2)
 for x in [208,1192]:d.path([(700,376),(x,376)])
 d.text(454,340,'Read revision 0',30);d.text(946,340,'Read revision 0',30)
 d.path([(208,500),(700,500)]);d.text(454,464,'Write A’s context change',28)
 d.path([(1192,636),(700,636)]);d.text(946,600,'Write B’s whole-file snapshot',28)
 d.node(524,712,352,112,'A’s change lost',fill=PINK,size=34)
 d.text(700,892,'Both commands may exit successfully',32)
 text(d,48,990,'Isolated files · one per job',36)
 for x,job,config in [(48,'Job A','Config A'),(768,'Job B','Config B')]:
  d.node(x,1052,216,112,job,size=34);d.node(x+304,1052,280,112,config,fill=BLUE,size=34);d.path([(x+216,1108),(x+304,1108)]);d.text(x+264,1080,'Write',28)
 d.text(700,1252,'Separate files do not correct credentials or server selection',30)
 d.save()
def exit_zero():
 d=D('6.4-what-exit-zero-hides',1696,'fleetctl maps the returned client-action error to zero or one; script outcome, ignored local work and queued work need different evidence.')
 title(d,'fleetctl exit status follows the client action')
 text(d,48,148,'Illustrative server-backed command path',32)
 boxes=[(48,192,352,112,'1  fleetctl invocation'),(48,376,352,112,'2  Request sent'),(48,560,352,112,'3  Fleet accepts it'),(48,744,352,144,'4  Work runs\nor is queued'),(512,744,352,144,'5  Result or accepted\nresponse returns'),(512,560,352,112,'6  Client renders\nthe result'),(512,296,352,176,'7  Did client action\nreturn an error?')]
 for x,y,w,h,label in boxes:d.node(x,y,w,h,label,anchor=label.startswith('6'),size=30)
 for start,end in [(304,376),(488,560),(672,744)]:d.path([(224,start),(224,end)])
 d.path([(400,816),(512,816)]);d.path([(688,744),(688,672)]);d.path([(688,560),(688,472)])
 d.path([(864,344),(1016,344)]);d.text(940,310,'No',28);d.node(1016,288,336,112,'Exit 0',fill=MINT,size=36)
 d.path([(864,428),(940,428),(940,508),(1016,508)]);text(d,884,478,'Yes',28);d.node(1016,452,336,112,'Exit 1',fill=PINK,size=36)
 d.text(1184,632,['Most exit 0 results','are ordinary success'],28)
 d.text(1128,764,['Wrapper timeout, signal,','or failure to start may','produce another status'],28)
 text(d,48,988,'Where the operational outcome appears',36)
 cards=[(48,'Printed output',['Script ran; script exit','code is non-zero','fleetctl exits 0: client','action completed'],BLUE),(504,'Nowhere',['Client-only exception:','accepted delete kind','is parsed and ignored','No message · No error','No effect · Exit 0'],APRICOT),(960,'Fleet later',['Asynchronous work queued','Final outcome is','not yet knowable'],APRICOT)]
 for x,heading,lines,fill in cards:
  d.rect(x,1040,392,424,fill,BORDER);d.text(x+196,1104,heading,36,600,NAVY);d.text(x+196,1170,lines,28,leading=46)
 d.text(244,1388,['--quiet removes the','script exit-code line'],28)
 d.path([(1156,1292),(1156,1332)],MUTED,width=2)
 d.node(984,1332,344,100,'Read Fleet state\nafterwards',size=28)
 # These are evidence examples, not successive execution stages.
 for y,label in [(1536,'Standard error'),(1620,'Standard output')]:
  text(d,48,y,label,30);d.path([(416,y-12),(1352,y-12)],MUTED,arrow=False,width=3)
 d.save()
def receiver():
 d=D('6.5-webhook-receive-and-act',1352,'Receiver-owned durable intake is separate from worker reconciliation and bounded, repeatable effects; event identity is modeled by the receiver.')
 title(d,'Receiver design: record receipt, then perform the work')
 d.rect(392,164,960,1080,PALE,BORDER);text(d,424,228,'Logic and storage you implement',34)
 d.node(48,316,256,144,'Webhook\nreceipt',size=36);d.path([(304,388),(440,388)])
 d.node(440,316,472,144,'Validate and durably\nrecord event',anchor=True,size=34)
 d.path([(676,460),(676,568)]);d.node(440,568,472,112,'Acknowledge promptly',size=32)
 d.text(176,566,['Repeated /','unordered delivery'],28)
 d.path([(176,632),(176,664),(344,664),(344,424),(440,424)],MUTED,dash='7 7')
 d.path([(912,388),(1040,388),(1040,756),(944,756)])
 d.text(1140,544,['Independent','worker path'],30)
 d.node(440,700,504,176,'Reconcile current state\nUse event / entity model\nSide effect needed?',size=32)
 d.path([(692,876),(692,952)]);text(d,736,920,'Yes',28)
 d.path([(944,820),(1168,820),(1168,952)]);text(d,1024,862,'No',28)
 d.node(440,952,504,128,'Apply bounded,\nrepeatable side effect',size=34)
 d.path([(944,1016),(1032,1016)]);d.node(1032,952,272,128,'Record\noutcome',size=34)
 d.text(700,1308,'No universal delivery ID or timestamp-only deduplication key',30)
 d.save()
def mcp():
 d=D('6.6-mcp-transport-boundaries',1480,'Local stdio is a launched subprocess; remote SSE crosses a TLS boundary with client access distinct from Fleet API credentials.')
 title(d,'Local stdio and remote SSE have different boundaries')
 d.rect(48,168,968,520,BG,NAVY);text(d,80,232,'Local machine',36)
 d.node(80,292,328,144,'Assistant client',size=34)
 d.node(552,292,400,144,'Fleet MCP\nsubprocess',anchor=True,size=36)
 d.path([(408,364),(552,364)]);d.text(480,320,'stdio',30);d.text(480,480,'Launches',28)
 d.node(1104,292,248,144,'Fleet',size=40);d.path([(952,364),(1104,364)])
 d.node(552,524,400,112,'Fleet API credential',fill=APRICOT,size=30);d.path([(752,524),(752,436)])
 d.text(80,548,'MCP_AUTH_TOKEN:',28,anchor='start',mono=True)
 d.text(80,584,['startup guard only;','not stdio authentication'],28,anchor='start')
 text(d,48,812,'Remote SSE',36)
 d.path([(336,900),(336,1308)],MUTED,dash='7 7',arrow=False,width=3);text(d,392,876,'Network / TLS boundary',30)
 for x,w,label in [(48,248,'Assistant\nclient'),(384,248,'TLS proxy'),(720,296,'Fleet MCP\nSSE listener'),(1104,248,'Fleet')]:d.node(x,956,w,144,label,anchor=x==720,size=32)
 for a,z in [(296,384),(632,720),(1016,1104)]:d.path([(a,1028),(z,1028)])
 d.node(48,1192,248,144,'Client access\ncredential',fill=BLUE,size=30);d.path([(172,1192),(172,1100)])
 d.node(720,1192,296,144,'Fleet API\ncredential',fill=APRICOT,size=30);d.path([(868,1192),(868,1100)])
 d.text(510,1170,['HTTPS / SSE','MCP checks bearer','on MCP requests'],28)
 d.text(700,1432,'Transport depends on client capability and topology, not brand',30)
 d.save()
if __name__=='__main__':
 b.OUT.mkdir(parents=True,exist_ok=True)
 for f in [paths,ambiguous,execution,assignment,prefixes,cursor,race,exit_zero,receiver,mcp]:f()
