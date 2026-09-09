#!/usr/bin/env python3
"""Part VII editable technical diagrams, using the approved collection primitives."""
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location('base',Path(__file__).resolve().parents[1]/'part-0-1/render-diagrams.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b);b.OUT=Path(__file__).resolve().parent/'assets'
D=b.Diagram
NAVY,SLATE,MUTED,BORDER,BG,PALE,BLUE,PINK,APRICOT=b.NAVY,b.SLATE,b.MUTED,b.BORDER,b.BG,b.PALE,b.BLUE,b.PINK,b.APRICOT
MINT='#D8FBEF'
def text(d,x,y,t,size=30):d.text(x,y,t,size,500,SLATE,anchor='start')
def title(d,t):text(d,48,80,t,40)
def bracket(d,x1,x2,y,label,color=MUTED):
 d.path([(x1,y-16),(x1,y),(x2,y),(x2,y-16)],color,arrow=False,width=3);d.text((x1+x2)/2,y+48,label,30)
def outcomes():
 d=D('7.1-outcomes-and-what-can-be-measured',1744,'Five independent service outcomes have different measurement costs; the database and Redis health check does not measure them.')
 title(d,'Match service objectives to available evidence')
 d.node(888,144,464,144,'Fleet health check\nDatabase + Redis',fill=MINT,size=34)
 text(d,48,196,['Five independent outcomes','Measurement cost varies by question'],32)
 rows=[('Administrative access',[('Cheap / direct','Request success and latency',MINT)]),
 ('Agent reporting',[('Cheap / partial','Oldest check-in in a filterable population',BLUE)]),
 ('Device-management delivery',[('Cheap / partial','Queue age from one host’s own view',BLUE),('Expensive','Estate-wide queue age requires enumeration',APRICOT)]),
 ('Scheduled processing',[('Not available','Supported current schedule-status surface',PINK)]),
 ('Data freshness',[('Cheap / partial','Maximum staleness: one ordered read in a filterable population',BLUE),('Expensive','Share past an arbitrary age: enumerate the population',APRICOT)])]
 y=364
 for name,items in rows:
  h=164 if len(items)==1 else 292
  d.rect(48,y,1304,h,BG,BORDER);text(d,80,y+54,name,34)
  for i,(cost,note,fill) in enumerate(items):
   yy=y+82+i*124;d.node(80,yy,312,64,cost,fill=fill,size=28)
   text(d,424,yy+42,note,28)
  y+=h+32
 d.text(700,1644,['Maximum age needs one ordered read; a share needs enumeration.','There is no staleness-threshold filter.'],30)
 d.save()
def recovery():
 d=D('7.1-recovery-objective-windows',1000,'Potential data loss and recovery duration are distinct windows with separately recorded targets and rehearsal results.')
 title(d,'Measure data loss and recovery duration separately')
 text(d,48,156,'Schematic time · intervals are not to scale',30)
 for x,lines in [(176,'Latest recoverable\ndata'),(700,'Incident\nonset'),(1224,'Service verified\nrestored')]:
  d.path([(x,316),(x,432)],NAVY,arrow=False);d.text(x,242,lines,32)
 d.path([(176,376),(416,376)],NAVY,arrow=False);d.path([(448,376),(936,376)],NAVY,arrow=False);d.path([(968,376),(1224,376)])
 for x in [432,952]:d.path([(x-10,364),(x+2,388)],NAVY,arrow=False,width=3)
 bracket(d,176,700,480,'Potential data-loss window','#FAA669');bracket(d,700,1224,480,'Recovery duration','#5CABDF')
 for x,heading in [(48,'Data-loss objective'),(736,'Recovery-time objective')]:
  d.rect(x,624,616,236,PALE,BORDER);text(d,x+32,680,heading,34)
  for y,label in [(740,'Target'),(808,'Rehearsed result')]:text(d,x+32,y,label,30);d.path([(x+320,y),(x+568,y)],MUTED,arrow=False,width=2)
 d.rect(48,904,36,36,APRICOT,'#FAA669',r=4);text(d,108,932,'Record a gap when the measured result exceeds its target',30)
 d.save()
def escrow():
 d=D('7.2-three-escrow-chains',1168,'Linux and macOS escrow depend on the Fleet server private key; Windows escrow requires separately preserved Windows enrollment certificate and key.')
 title(d,'Preserve each escrow chain’s recovery material')
 for x,label in [(48,'Linux LUKS'),(504,'macOS FileVault'),(960,'Windows BitLocker')]:d.text(x+196,176,label,34,600,NAVY)
 text(d,48,250,'Configuration material · outside the database',30)
 d.node(48,292,848,128,'Fleet server private key',anchor=True,size=36)
 d.node(960,292,392,128,'Windows enrolment\ncertificate + key',fill=APRICOT,size=32)
 d.rect(48,520,1304,496,PALE,NAVY);text(d,80,580,['MySQL','backup'],32)
 for x in [472,928]:d.path([(x,632),(x,984)],BORDER,arrow=False,width=2)
 d.node(528,656,368,144,'Apple CA material\nEncrypted',fill=BLUE,size=32)
 for x,lab in [(80,'Linux escrow'),(528,'FileVault escrow'),(976,'BitLocker escrow')]:d.node(x,872,344 if x==976 else 368,112,lab,size=32)
 d.path([(264,872),(264,420)])
 d.path([(712,872),(712,800)]);d.path([(712,656),(712,420)])
 d.path([(1148,872),(1148,420)])
 d.text(700,1088,['Database backup + Fleet server private key: Linux and macOS','Windows also needs its enrolment certificate and key'],30)
 d.save()
def cross_store():
 d=D('7.2-backup-cross-store-gap',1320,'Independent database and object captures can leave missing bytes or unreferenced objects that cleanup may delete.')
 title(d,'Separate captures leave two possible consistency gaps')
 for x,label in [(48,'Database capture'),(760,'Storage capture')]:
  d.text(x+292,174,label,34,600,NAVY);d.path([(x+56,224),(x+528,224)],MUTED,arrow=False,width=2)
 d.path([(224,208),(224,240)],NAVY,arrow=False);d.path([(1104,208),(1104,240)],NAVY,arrow=False)
 d.text(700,294,'Independent moments · no atomic snapshot or capture order implied',28)
 text(d,48,398,'Case A · referenced bytes are absent',36)
 d.node(48,448,472,128,'Row references installer X',size=32)
 d.node(760,448,592,128,'Storage lacks X',fill=PINK,size=36)
 d.path([(520,512),(760,512)]);d.cross(648,512)
 d.text(1056,638,'Missing bytes',32)
 text(d,48,768,'Case B · storage is newer than the restored database',34)
 d.node(48,820,472,128,'Older database\nNo row for Y',size=32)
 d.node(760,820,592,128,'Object Y exists\nUnreferenced',fill=APRICOT,size=34)
 d.path([(520,884),(760,884)],MUTED,dash='7 7',arrow=False);d.cross(648,884)
 d.path([(1056,948),(1056,1036)],MUTED,dash='7 7');text(d,1112,1004,'Cleanup',28)
 d.node(760,1036,592,112,'Deletion candidate',fill=PINK,size=36)
 d.text(700,1244,'Storage versioning may permit recovery; it is not guaranteed',30)
 d.save()
def restart():
 d=D('7.3-restart-activated-queue',1312,'An activated activity survives a Fleet restart and blocks later work on that host until a result or cancellation arrives; there is no age-based reaper.')
 title(d,'An activated item can keep a host’s queue blocked')
 text(d,48,160,'One host · queued activities',32)
 for x,label in [(48,'A · Activated'),(504,'B · Waiting'),(960,'C · Waiting')]:d.node(x,216,392,120,label,anchor=x==48,size=34)
 for a,z in [(440,504),(896,960)]:d.path([(a,276),(z,276)],MUTED,arrow=False,width=2)
 d.path([(48,424),(1352,424)],MUTED,dash='8 8',arrow=False);d.text(1080,404,'Fleet restart',30)
 d.path([(244,336),(244,536)])
 d.node(48,536,520,152,'A remains activated\nCan be fetched again',fill=BLUE,size=36)
 d.path([(568,612),(712,612)])
 d.node(712,520,640,184,'Result or cancellation\nreceived?',size=38)
 d.path([(928,704),(928,856),(700,856)]);d.text(824,820,'Yes',30)
 d.node(48,796,652,120,'Advance to B',fill=MINT,size=38)
 d.path([(1200,704),(1200,996),(700,996)]);d.text(1236,864,'No',30)
 d.node(48,948,652,152,'B and C keep waiting\nNo age-based reaper',fill=PINK,size=36)
 d.text(700,1224,'The active item’s result or cancellation releases this host’s later work',30)
 d.save()
def health():
 d=D('7.4-green-while-failing',2000,'A database and Redis check can stay green while five service outcomes fail; the metrics endpoint, export pipeline and operational reads provide distinct evidence.')
 title(d,'Observe each service outcome independently')
 d.node(48,152,424,136,'Fleet health check\nDatabase + Redis',fill=MINT,size=34)
 d.text(256,356,['Green can persist','through every failure below'],28)
 text(d,568,216,['A failed health response does not','identify which check failed.'],30)
 text(d,48,444,'Independent failure lanes · illustrative, not a timing chart',30)
 rows=[('Administrative access','Request success / latency','Metrics endpoint + export pipeline',160),('Agent reporting','Host check-in freshness','Read Fleet state',288),('Device-management delivery','Per-host queue age','Read the host’s own view',208),('Scheduled processing','Freshness of expected output','Maintained / purchased apps: not established',336),('Data freshness','Per-host update times','Read Fleet state',256)]
 for i,(name,signal,source,offset) in enumerate(rows):
  y=492+i*176;d.text(48,y+38,name,32,500,NAVY,anchor='start')
  d.path([(48,y+90),(448,y+90)],MUTED,arrow=False,width=3);d.cross(48+offset,y+90)
  text(d,560,y+40,signal,32);text(d,560,y+90,source,28)
 text(d,48,1420,'Separate evidence sources',36)
 cards=[(48,'Metrics endpoint',['Request-level metrics','No business metrics']), (504,'Export pipeline',['Traces + metrics','Pool statistics, errors','and cache counters','Export pipeline only']), (960,'Operational reads',['Check-in freshness','Per-host queue age','Per-host update times'])]
 for x,head,lines in cards:
  d.rect(x,1460,392,328,PALE,BORDER);d.text(x+196,1524,head,32,600,NAVY);d.text(x+196,1596,lines,28,leading=44)
 d.text(700,1852,'Metrics and export coverage overlap; neither contains the other',30)
 d.node(48,1896,1304,72,'Object storage · no Fleet-side signal · monitor the storage provider',fill=APRICOT,size=30)
 d.save()
def units():
 d=D('7.4-latency-metric-unit-check',1016,'The service latency family is named for microseconds but emits seconds in Fleet 4.90.0; thresholds need explicit unit checking.')
 title(d,'Check the latency metric’s emitted unit')
 d.rect(48,168,1304,168,PALE,BORDER)
 d.text(700,232,'api_service_request_latency_microseconds',31,500,NAVY,mono=True)
 d.text(700,298,'Emitted in seconds at this release',34)
 for x,w,label in [(48,312,'Raw seconds'),(480,456,'Unit conversion /\nthreshold check'),(1056,296,'Alert\ncomparison')]:d.node(x,456,w,144,label,anchor=x==480,size=34)
 for a,z in [(360,480),(936,1056)]:d.path([(a,528),(z,528)])
 d.text(700,700,'Illustrative value: 0.25 s = 250 ms = 250,000 microseconds',32)
 d.path([(204,600),(204,864),(400,864)],MUTED,dash='7 7');d.cross(316,864)
 d.node(400,800,488,128,'Treat raw as microseconds',fill=PINK,size=30)
 d.path([(888,864),(1016,864)],'#D66C7B');d.node(1016,800,336,128,'Threshold\nmismatch',fill=PINK,size=34)
 d.save()
def capacity():
 d=D('7.5-capacity-decision-path',1656,'Investigate stalled work first, then sustained pressure and the constrained component; reclaim headroom before expanding capacity.')
 title(d,'Find the constrained component before scaling')
 for y,lab in [(176,'Slow progress'),(380,'Stalled work?'),(624,'Sustained pressure?'),(868,'Identify constrained component')]:d.node(48,y,632,128,lab,anchor=y==176,size=36)
 d.path([(364,304),(364,380)])
 for yy,end in [(508,624),(752,868)]:d.path([(364,yy),(364,end)])
 d.text(410,578,'No',30);d.text(410,822,'Yes',30)
 for y,lab,branch in [(380,'Investigate queue,\nschedule and replica state','Yes'),(624,'Observe spike\nagainst baseline','No')]:
  d.path([(680,y+64),(936,y+64)]);d.text(808,y+28,branch,30);d.node(936,y,416,128,lab,fill=APRICOT,size=30)
 d.rect(48,1100,1304,492,PALE,BORDER);text(d,80,1160,'Component-specific remedy',36)
 d.path([(364,996),(364,1040),(700,1040),(700,1100)],MUTED,width=3)
 d.path([(212,1192),(1196,1192)],MUTED,arrow=False,width=3)
 for x,lab in [(80,'Application'),(408,'MySQL'),(736,'Redis'),(1064,'Storage')]:
  d.path([(x+132,1192),(x+132,1220)],MUTED,width=3);d.node(x,1220,264,96,lab,size=32)
 d.text(700,1400,'Tune / reclaim headroom',36,600,NAVY)
 d.path([(700,1424),(700,1480)]);d.node(320,1480,760,80,'Expand the constrained component as needed',fill=BLUE,size=32)
 d.save()
def pools():
 d=D('7.5-connection-budget-multiplies',1664,'Each Fleet instance has independent writer and replica connection ceilings; configured replica loss can remove every instance from a health-check-based load balancer.')
 title(d,'Connection budgets multiply independently')
 d.node(48,168,336,112,'Load balancer',size=36)
 for x in [528,824,1120]:d.node(x,168,232,112,'Fleet instance',size=30)
 d.path([(384,224),(432,224),(432,136),(1236,136)],MUTED,arrow=False,width=3)
 for x in [644,940,1236]:d.path([(x,136),(x,168)],MUTED,width=3)
 d.text(940,344,'N instances',32)
 d.path([(644,280),(644,392)],MUTED,dash='7 7',arrow=False,width=2)
 d.rect(48,392,680,568,PALE,BORDER);text(d,80,452,'One representative Fleet instance',34)
 for y,lab,letter,col,dest in [(520,'Writer pool','W','#009A7D','Writable primary\nExactly one'),(784,'Replica pool','R','#5CABDF','Read replica')]:
  d.node(80,y,584,136,lab+'\nMaximum '+letter+' concurrent connections',size=30)
  d.path([(664,y+68),(1016,y+68)],col)
  d.node(1016,y,336,136,dest,anchor=y==520,size=34)
 d.cross(1312,804,10)
 for y,left,right,col in [(1056,'At primary: N × W maximum concurrent connections','Primary’s own\nconnection limit','#009A7D'),(1184,'At replica: N × R maximum concurrent connections','Replica’s own\nconnection limit','#5CABDF')]:
  text(d,48,y,left,30);d.path([(48,y+28),(920,y+28)],col,arrow=False,width=4);d.path([(920,y+8),(920,y+48)],'#FAA669',arrow=False,width=6);text(d,968,y+12,right,28)
 d.text(700,1320,'Ceilings on concurrent connections; not connections held at rest',30)
 for x,lab in [(48,'Configured read\nreplica unavailable'),(504,'Health check fails\non every instance'),(960,'Load balancer removes\nevery instance')]:d.node(x,1436,392,128,lab,fill=PINK,size=30)
 for a,z in [(440,504),(896,960)]:d.path([(a,1500),(z,1500)],'#D66C7B')
 d.text(700,1620,'Health-check-based removal · no fallback to the writer',30)
 d.save()
def ca():
 d=D('7.6-private-ca-cutover',1432,'A private trust-root cutover waits for verified distribution to representative agents before the server presents the new chain; retain hostname continuity.')
 title(d,'Verify private-root distribution before cutover')
 d.node(48,144,1304,80,'Same hostname throughout · a hostname change is a migration',fill=BLUE,size=32)
 for x,lab in [(48,'Operator / Fleet server'),(776,'Representative agents')]:
  text(d,x,318,lab,36);d.path([(x+284,360),(x+284,1120)],MUTED,dash='7 7',arrow=False,width=2)
 d.node(48,408,568,128,'Distribute new private root',size=34)
 d.path([(616,472),(776,472)]);d.node(776,408,576,128,'Receive new root',size=34)
 d.node(776,652,576,168,'Verify trust\non representative platforms',anchor=True,size=34)
 d.path([(1064,536),(1064,652)])
 d.path([(776,736),(332,736),(332,940)]);text(d,400,870,'Trust verified',30)
 d.node(48,940,568,128,'Switch served chain',size=36)
 d.path([(616,1004),(776,1004)]);d.node(776,940,576,128,'Confirm agent check-ins',fill=MINT,size=34)
 d.text(1064,1160,['Browser-only check:','insufficient evidence'],30)
 d.text(700,1352,'Keep old-root overlap until the transition is tested',30)
 d.save()
def renewal():
 d=D('7.6-renewal-versus-replacement',1656,'Existing escrow retrieval depends on different keys and certificates by platform; only macOS supports certificate rollover with its authority key retained.')
 title(d,'Certificate renewal has different escrow consequences')
 text(d,48,150,'Existing escrow retrieved through a working Fleet configuration',30)
 for x,lab in [(48,'macOS FileVault'),(504,'Windows BitLocker'),(960,'Linux LUKS')]:
  d.rect(x,204,392,856,BG,BORDER);d.text(x+196,270,lab,32,600,NAVY)
 d.node(80,328,328,112,'Fleet server\nprivate key',fill=BLUE,size=32)
 d.path([(112,552),(112,440)]);text(d,152,490,['Protects authority','material'],28)
 d.node(80,552,328,144,'Apple authority key',size=30)
 d.node(80,744,328,80,'Current certificate',size=28);d.node(80,844,328,80,'Historical certificates',size=28)
 d.node(536,552,328,168,'Current enrolment\ncertificate + key\nOnly',size=32)
 d.text(700,812,['No historical fallback','Certificate participates','in retrieval'],28)
 d.node(992,552,328,144,'Fleet server\nprivate key',size=32);d.text(1156,808,'No certificate in this path',28)
 for x,lab in [(80,'FileVault escrow'),(536,'BitLocker escrow'),(992,'LUKS escrow')]:d.node(x,952,328,80,lab,fill=PALE,size=30)
 # Dependencies rise within their own platform columns; certificate chips support only Apple material.
 d.path([(112,952),(112,924),(56,924),(56,624),(80,624)],MUTED,width=3)
 d.path([(700,952),(700,924),(888,924),(888,636),(864,636)],MUTED,width=3)
 d.path([(1156,952),(1156,900),(1336,900),(1336,624),(1320,624)],MUTED,width=3)
 text(d,48,1136,'Renew certificate',36)
 for x,lab,fill in [(48,'Survivable if the\nauthority key is retained',MINT),(504,'Not survivable, even\nwith the same key pair',PINK),(960,'Not applicable\nNo certificate',PALE)]:d.node(x,1176,392,128,lab,fill=fill,size=30)
 text(d,48,1380,'Replace the decrypting key',36)
 for x in [48,504,960]:d.node(x,1416,392,80,'Not survivable',fill=PINK,size=32)
 d.rect(48,1544,1304,80,APRICOT,BORDER);d.text(700,1595,'Windows: Fleet still reports credentials available after the certificate changes',30)
 d.save()
def handover():
 d=D('7.7-what-is-handed-over',1088,'A Fleet handover carries ongoing storage, credential, trust, upgrade and scheduled-work obligations beyond the URL and administrative login.')
 title(d,'Hand over the ongoing operating responsibilities')
 d.node(48,444,328,144,'Fleet URL +\nadmin login',anchor=True,size=34)
 d.path([(376,516),(496,516)])
 d.rect(528,168,824,824,PALE,BORDER);text(d,568,238,'Standing obligations',38)
 rows=[['Three stores','More than one can lose unrecoverable data'],['Expiring credentials','Renewal schedules belong to other organizations'],['Certificate rotation','Order preserves agent connectivity'],['Upgrades','The documented procedure stops service'],['Periodic jobs','Can stop without reporting an error']]
 for i,(heading,note) in enumerate(rows):
  y=320+i*136;d.rect(568,y-24,12,12,'#5CABDF','#5CABDF',r=6);text(d,616,y,heading,34);text(d,616,y+48,note,28)
 d.path([(520,168),(496,168),(496,992),(520,992)],MUTED,arrow=False,width=3)
 d.save()
def evidence():
 d=D('7.7-handoff-evidence-gate',1328,'An organization reviews restore, upgrade and ownership evidence with named owners and results before accepting ongoing handoff responsibility.')
 title(d,'Make handoff acceptance depend on recorded evidence')
 text(d,48,150,'Your organization’s review process',30)
 for x,lab in [(48,'Restore rehearsal'),(504,'Upgrade rehearsal'),(960,'Dependency / credential\nownership record')]:
  d.rect(x,216,392,264,PALE,BORDER);d.text(x+196,278,lab,32,500,NAVY)
  for y,t in [(372,'Owner'),(438,'Recorded result')]:d.node(x+24,y-40,344,56,t,size=28)
  d.path([(x+196,480),(x+196,556)],MUTED,arrow=False,width=3)
 d.path([(244,556),(1156,556)],MUTED,arrow=False,width=3);d.path([(700,556),(700,644)])
 d.node(456,644,488,128,'Handoff review\nEvidence complete?',anchor=True,size=36)
 d.path([(456,708),(260,708),(260,888)]);d.text(340,674,'No',30)
 d.node(48,888,424,112,'Resolve the gap',fill=APRICOT,size=36)
 d.path([(260,1000),(260,1040),(568,1040),(568,772)],MUTED,dash='7 7');text(d,600,1016,'Re-review',30)
 d.path([(944,708),(1156,708),(1156,888)]);d.text(1040,674,'Yes',30)
 d.node(960,888,392,112,'Accept handoff',fill=MINT,size=36)
 d.path([(1156,1000),(1156,1104),(700,1104),(700,1152)])
 d.node(376,1152,648,112,'Named primary + backup\nContinuing responsibility',fill=BLUE,size=34)
 d.save()
def retirement():
 d=D('7.8-deployment-retirement-order',1592,'Release devices and external dependencies, revoke credentials and preserve a final keyed backup before shutting down; deletion follows retention policy.')
 title(d,'Release dependencies before decommissioning Fleet')
 stages=['Export required records','Release or migrate devices','Release external assignments','Revoke credentials','Final backup with key material','Decommission']
 for i,lab in enumerate(stages):
  y=176+i*204;d.node(48,y,136,112,str(i+1),anchor=i==5,size=42);d.node(304,y,744,112,lab,fill=BLUE if i==5 else PALE,size=36)
  d.path([(184,y+56),(304,y+56)],MUTED,arrow=False,width=2)
  if i<5:d.path([(676,y+112),(676,y+204)],MUTED if i==4 else NAVY,dash='7 7' if i==4 else None)
 d.path([(1112,176),(1144,176),(1144,1104),(1112,1104)],MUTED,arrow=False,width=3)
 d.text(1232,520,['Fleet still','available','where','required'],28)
 d.path([(48,1144),(1352,1144)],MUTED,dash='8 8',arrow=False,width=3);d.text(1104,1132,'Shutdown boundary',28)
 d.path([(676,1308),(676,1384)],MUTED,dash='7 7')
 d.node(304,1384,744,112,'Retention-based deletion',fill=APRICOT,size=34)
 d.save()
if __name__=='__main__':
 b.OUT.mkdir(parents=True,exist_ok=True)
 for f in [outcomes,recovery,escrow,cross_store,restart,health,units,capacity,pools,ca,renewal,handover,evidence,retirement]:f()
