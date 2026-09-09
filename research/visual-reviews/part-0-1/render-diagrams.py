#!/usr/bin/env python3
"""Author the review batch's diagrams as editable SVG and lossless WebP.

Requires Inter and Roboto Mono fonts, rsvg-convert, and cwebp.
This is artwork source; it does not alter chapter prose or approve images.
"""
from pathlib import Path
from html import escape
import subprocess

OUT = Path(__file__).resolve().parent / 'assets'
NAVY, SLATE, MUTED = '#192147', '#515774', '#8B8FA2'
BG, BLUE, PALE, BORDER = '#F9FAFC', '#D3E8F3', '#E8F1F6', '#C5C7D1'
ROSE, PINK, APRICOT = '#D66C7B', '#F6E4E8', '#FBEBDC'

class Diagram:
    def __init__(self, name, height, description):
        self.name, self.height = name, height
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="{height}" viewBox="0 0 1400 {height}" role="img">',
                      f'<title>{escape(description)}</title>',
                      '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="context-stroke"/></marker></defs>',
                      f'<rect width="1400" height="{height}" fill="{BG}"/>']
    def text(self, x, y, lines, size=36, weight=400, color=SLATE, anchor='middle', mono=False, leading=None):
        lines = lines.split('\n') if isinstance(lines, str) else lines
        step = leading or round(size*1.3)
        family = 'Roboto Mono' if mono else 'Inter'
        for n,line in enumerate(lines):
            self.parts.append(f'<text x="{x}" y="{y+n*step}" text-anchor="{anchor}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(line)}</text>')
    def rect(self,x,y,w,h,fill=PALE,stroke=BORDER,r=12,dash=None,width=2.5):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def node(self,x,y,w,h,label,fill=PALE,size=36,anchor=False,stroke=None):
        self.rect(x,y,w,h, NAVY if anchor else fill, stroke or (NAVY if anchor else BORDER))
        lines=label.split('\n');step=round(size*1.3)
        self.text(x+w/2,y+h/2-(len(lines)-1)*step/2+size*.35,lines,size,600 if anchor else 500,BG if anchor else NAVY)
    def path(self, points, color=NAVY, dash=None, arrow=True, width=4):
        d='M'+' L'.join(f'{x} {y}' for x,y in points)
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
    def cross(self,x,y,size=13):
        self.path([(x-size,y-size),(x+size,y+size)],ROSE,arrow=False,width=6)
        self.path([(x-size,y+size),(x+size,y-size)],ROSE,arrow=False,width=6)
    def laptop(self,x,y,w=144,h=90,fill=BG):
        self.rect(x,y,w,h,fill,NAVY,5,width=3)
        self.parts.append(f'<path d="M{x-12} {y+h+10} H{x+w+12} L{x+w} {y+h+24} H{x} Z" fill="{fill}" stroke="{NAVY}" stroke-width="3"/>')
    def diamond(self,x,y,w,h,label):
        self.parts.append(f'<path d="M{x+w/2} {y} L{x+w} {y+h/2} L{x+w/2} {y+h} L{x} {y+h/2} Z" fill="{PALE}" stroke="{NAVY}" stroke-width="2.5"/>')
        lines=label.split('\n');self.text(x+w/2,y+h/2-(len(lines)-1)*20+12,lines,32,500,NAVY,leading=40)
    def save(self):
        svg=OUT/(self.name+'.svg');svg.write_text('\n'.join(self.parts+['</svg>'])+'\n')
        png=OUT/(self.name+'.png');webp=OUT/(self.name+'.webp')
        subprocess.run(['rsvg-convert',str(svg),'-o',str(png)],check=True)
        subprocess.run(['cwebp','-quiet','-lossless',str(png),'-o',str(webp)],check=True)
        print(self.name)

def reading_route():
    d=Diagram('0.1-new-reader-route',868,'A deployment reading route with separate production handoff prerequisites.')
    # Branches are reading alternatives; the lower gate requires actual operating evidence.
    d.path([(268,126),(332,126)])
    d.path([(572,126),(868,126)])
    d.text(720,98,'Managed Fleet',30,500)
    d.path([(452,184),(452,292)])
    d.text(468,246,'Self-hosted',30,anchor='start')
    d.path([(572,352),(636,352)])
    d.path([(1036,352),(1070,352),(1070,202),(976,202),(976,184)])
    d.path([(1084,126),(1148,126)])
    d.path([(1250,184),(1250,478)])
    d.path([(1250,588),(1250,618),(684,618),(684,672)])
    d.path([(880,728),(1032,728)])
    d.path([(352,728),(410,728),(410,824),(1192,824),(1192,784)],MUTED,dash='8 8')
    d.node(48,64,220,120,'Part I\nFoundations',size=34)
    d.node(332,64,240,120,'2.1\nChoose hosting',size=30)
    d.node(868,64,216,120,'2.5 onward\nAdministration',size=30)
    d.node(1148,64,204,120,'Part III\nEnrollment',size=32)
    d.node(332,292,240,120,'2.2\nArchitecture',size=34)
    d.rect(636,270,400,164)
    d.text(836,316,'Choose a deployment path',28,500)
    d.text(836,362,'2.3  AWS / GCP',32,500,NAVY)
    d.text(836,407,'2.4  Containers / VMs',32,500,NAVY)
    d.node(1076,478,276,110,'Working\ndeployment',anchor=True,size=36)
    d.node(48,672,304,112,'Parts II + VII\nPrerequisite reading',size=30)
    d.node(488,672,392,112,'Operating +\nrehearsal evidence',size=34)
    d.node(1032,672,320,112,'7.7\nProduction handoff',fill='#EAE4F1',size=34)
    d.save()

def ecosystem():
    d=Diagram('1.1-fleet-environment-boundaries',746,'Fleet retains its accounts and roles alongside identity, configuration management and exported data.')
    d.path([(338,222),(564,222)]);d.text(452,167,['Sign-in','identity'],30)
    for y,label in [(164,'Results'),(240,'Status'),(316,'Audit')]:
        d.path([(884,y),(1052,y)]);d.text(968,y-18,label,30)
    d.path([(724,530),(724,376)]);d.text(752,452,'Observe',30,anchor='start')
    d.path([(438,608),(580,608)]);d.text(509,460,['System','configuration'],28)
    d.node(48,146,290,152,'Identity\nprovider',size=36)
    d.rect(564,64,320,312,PALE,NAVY)
    d.node(588,88,272,92,'Fleet',anchor=True,size=44)
    d.text(724,254,['Accounts and roles','Stored in Fleet'],30,500)
    d.node(1052,104,300,310,'SIEM /\ndata lake',size=40)
    d.text(1202,465,['Audit: Premium,','opt-in'],28)
    d.node(48,532,390,152,'Existing configuration\nmanagement',size=34)
    d.node(580,530,288,156,'Linux host',size=38)
    d.save()

def online():
    d=Diagram('1.2-online-evidence-boundary',810,'The Online indicator uses osquery freshness and a new-record fallback, independently of MDM results.')
    d.rect(48,48,288,704,BG,BORDER)
    d.rect(1048,48,304,704,BG,BORDER)
    d.text(192,112,'Host',44,600,NAVY);d.text(1200,112,'Fleet',44,600,NAVY)
    d.laptop(124,362,136,88,BLUE)
    d.path([(336,216),(1080,216)])
    d.text(700,174,'osquery check-in',36,500,NAVY)
    d.path([(420,280),(968,280)],MUTED,arrow=False,width=2.5)
    d.path([(420,268),(420,292)],MUTED,arrow=False,width=2.5)
    d.path([(968,268),(968,292)],MUTED,arrow=False,width=2.5)
    d.text(694,325,'Check-in window + 60 s grace',28)
    d.text(694,366,'Schematic timing',28,color=MUTED)
    d.node(1080,168,240,96,'Online',anchor=True,size=40)
    d.node(1080,386,240,112,'Host record\ncreated',size=30)
    d.path([(1100,386),(1100,264)],MUTED,dash='6 8')
    d.text(1218,315,['Before first','check-in'],28)
    d.path([(1048,578),(336,578)])
    d.text(692,544,'MDM command',36,500,NAVY)
    d.path([(336,696),(1080,696)])
    d.text(692,662,'MDM result',36,500,NAVY)
    d.node(1080,646,240,100,'Result\nreceived?',size=32)
    d.save()

def transfer():
    d=Diagram('1.3-host-transfer-state',944,'A fleet transfer keeps identity, discards old scope results, and has separate profile and escrow consequences.')
    d.rect(48,48,390,270,BG,BORDER);d.rect(962,48,390,270,BG,BORDER)
    d.text(243,110,'fleet A',44,600,NAVY);d.text(1157,110,'fleet B',44,600,NAVY)
    d.node(80,156,326,112,'Host 42',anchor=True,size=40)
    d.node(994,156,326,112,'Host 42',anchor=True,size=40)
    d.path([(406,212),(994,212)])
    d.text(700,141,['Same host ID','and inventory'],32,500)
    d.path([(243,318),(243,452)],ROSE)
    d.text(243,382,'Old scope',30,500)
    d.rect(48,452,390,222,PINK,ROSE)
    d.text(80,508,'Deleted',36,600,NAVY,anchor='start')
    d.text(80,560,['fleet policy/report results','fleet label memberships'],28,anchor='start',leading=46)
    d.path([(1094,318),(1094,368),(700,368),(700,544)])
    d.text(762,442,'Profiles',28,anchor='start')
    d.node(512,544,376,132,'Profile\nreconciliation',size=34)
    d.text(700,722,'Deferred',30,500)
    d.path([(1236,318),(1236,480)])
    d.text(1124,410,'Recovery',28,500)
    d.node(980,480,372,164,'Encryption enforced\nin destination?',size=30,stroke=NAVY)
    d.path([(1166,644),(1166,738)])
    d.text(1190,703,'No',30,500,anchor='start')
    d.node(980,738,372,112,'Active escrow\nkey deleted',fill=PINK,stroke=ROSE,size=34)
    d.text(1166,899,'Archived-key fallback is separate',28)
    d.save()

def accounts():
    d=Diagram('1.4-account-review-lifecycles',814,'SSO deprovisioning and owner-led account review follow separate paths.')
    d.text(48,60,'SSO authenticates · JIT creates',30,anchor='start')
    d.text(48,134,'Eligible SSO accounts',38,600,NAVY,anchor='start')
    d.path([(320,238),(384,238)]);d.path([(558,238),(640,238)])
    d.path([(870,238),(958,238),(958,190),(1066,190)])
    d.text(956,158,'No',30,500)
    d.path([(755,320),(755,362),(1066,362)])
    d.text(942,344,'Yes',30,500)
    d.node(48,182,272,112,'IdP deletion /\ndeactivation',size=30)
    d.node(384,182,174,112,'SCIM',anchor=True,size=36)
    d.node(640,158,230,162,'Last global\nadmin?',size=30,stroke=NAVY)
    d.node(1066,138,286,104,'Fleet account\nremoved',size=32)
    d.node(1066,316,286,92,'Protected',fill=APRICOT,size=34)
    d.text(471,352,['Premium at','server startup'],28)
    d.path([(48,454),(1352,454)],BORDER,arrow=False,width=2)
    d.text(48,512,'Password and API-only accounts',38,600,NAVY,anchor='start')
    d.path([(318,626),(384,626)])
    d.path([(754,626),(890,626),(890,579),(1020,579)])
    d.path([(890,626),(890,719),(1020,719)])
    d.node(48,574,270,104,'Named owner',size=34)
    d.node(384,574,370,104,'Scheduled\naccess review',size=34)
    d.node(1020,534,332,90,'Keep + review date',size=30)
    d.node(1020,674,332,90,'Revoke / remove',size=32)
    d.save()

def activities():
    d=Diagram('1.5-activity-actor-retention',894,'Device events may have no actor; account deletion preserves stored attribution but breaks the live-user lookup.')
    d.text(48,76,'A device event',38,600,NAVY,anchor='start')
    d.laptop(120,144,180,100,BLUE)
    d.text(210,312,'Apple device',32)
    d.path([(332,205),(672,205)]);d.text(500,173,'CheckOut',32,mono=True)
    d.rect(672,136,572,164,BG,NAVY)
    d.rect(672,136,572,72,NAVY,NAVY)
    d.text(958,184,'Activity',36,500,BG)
    d.text(958,266,'mdm_unenrolled',34,500,NAVY,mono=True)
    d.text(958,352,'No user actor',32)
    d.path([(48,402),(1352,402)],BORDER,arrow=False,width=2)
    d.text(48,468,'An account is deleted',38,600,NAVY,anchor='start')
    d.text(48,528,'Before',30,600,NAVY,anchor='start');d.text(756,528,'After',30,600,NAVY,anchor='start')
    d.node(48,614,202,112,'User\naccount',size=30)
    d.path([(250,670),(324,670)],MUTED,dash='6 7',arrow=False,width=3)
    d.rect(324,560,320,218,BG,NAVY)
    d.rect(324,560,320,62,BLUE,NAVY)
    d.text(484,603,'Activity',32,500,NAVY)
    d.text(348,667,'User link',28,anchor='start')
    d.path([(324,692),(644,692)],BORDER,arrow=False,width=2)
    d.text(348,744,'Stored name / email',28,anchor='start')
    d.path([(668,670),(732,670)])
    d.node(756,614,202,112,'Account\ndeleted',fill=APRICOT,size=30)
    d.path([(958,670),(1032,670)],MUTED,dash='6 7',arrow=False,width=3)
    d.cross(995,670,10)
    d.rect(1032,560,320,218,BG,NAVY)
    d.rect(1032,560,320,62,BLUE,NAVY)
    d.text(1192,603,'Activity',32,500,NAVY)
    d.text(1056,667,'User link: null',28,anchor='start')
    d.path([(1032,692),(1352,692)],BORDER,arrow=False,width=2)
    d.text(1056,744,'Stored name / email',28,anchor='start')
    d.text(48,838,'Dashed line: user lookup',28,anchor='start')
    d.text(1054,838,'Actor type no longer resolvable',28)
    d.save()

def stores():
    d=Diagram('1.6-datastore-outage-paths',970,'MySQL outage blocks authentication; Redis outage has separate feature and optional queue consequences.')
    d.rect(48,48,620,870,BG,BORDER);d.rect(732,48,620,870,BG,BORDER)
    d.text(80,112,'MySQL unavailable',38,600,NAVY,anchor='start')
    d.text(764,112,'Redis unavailable',38,600,NAVY,anchor='start')
    d.text(764,160,'MySQL remains available',30,anchor='start')
    d.path([(316,278),(430,278)]);d.cross(370,278)
    d.node(80,228,236,100,'Host\nauthentication',size=30)
    d.node(430,228,206,100,'MySQL',size=34)
    d.path([(198,328),(198,468)])
    d.node(80,468,556,122,'Check-ins and\nUI/API fail',fill=PINK,size=36)
    d.text(104,672,['Process stays running','New instance cannot start'],30,anchor='start',leading=54)
    d.path([(1016,278),(1112,278)],MUTED,dash='6 8')
    d.node(764,228,252,100,'Host\nauthentication',size=30)
    d.node(1112,228,208,100,'Redis\ncache',size=30)
    d.cross(1220,213,11)
    d.path([(890,328),(890,482),(1112,482)])
    d.text(922,374,['More database','load'],28,anchor='start')
    d.node(1112,438,208,88,'MySQL',anchor=True,size=34)
    d.node(764,566,252,96,'Live reports',fill=PINK,size=30)
    d.node(1068,566,252,96,'SSO in flight',fill=PINK,size=30)
    d.cross(780,553,10);d.cross(1084,553,10)
    d.rect(764,690,556,186,BG,MUTED,dash='7 7')
    d.text(1042,736,'If async processing is enabled',28,500)
    d.path([(944,811),(960,811)],MUTED,dash='5 6',width=3)
    d.path([(1084,811),(1100,811)],MUTED,dash='5 6',width=3)
    d.node(780,770,164,82,'Observed\nupdates',size=28)
    d.node(960,770,124,82,'Redis\nqueue',size=28)
    d.cross(1022,766,9)
    d.node(1100,770,204,82,'Stale\nobservations',size=28)
    d.save()

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    for make in [reading_route,ecosystem,online,transfer,accounts,activities,stores]:make()
