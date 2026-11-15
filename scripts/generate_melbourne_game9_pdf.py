#!/usr/bin/env python3
import json, os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm

root=os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(root,'data','league_stats.json'),encoding='utf-8') as f: d=json.load(f)
out=os.path.join(root,'reports','Melbourne_Season_Stats_Through_Game9_Waverley_Updated.pdf')
txt=os.path.join(root,'text_reports','Melbourne_Season_Stats_Through_Game9_Waverley_Updated.txt')
os.makedirs(os.path.dirname(out),exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportTitle',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=17,leading=21,textColor=colors.HexColor('#15384e'),spaceAfter=9))
styles.add(ParagraphStyle(name='ReportSub',parent=styles['Normal'],fontSize=9,leading=13,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallNote',parent=styles['Normal'],fontSize=8,leading=11,spaceAfter=7))
styles.add(ParagraphStyle(name='Sect',parent=styles['Heading2'],fontSize=12,textColor=colors.HexColor('#15384e'),spaceBefore=9,spaceAfter=7))
doc=SimpleDocTemplate(out,pagesize=landscape(A4),rightMargin=12*mm,leftMargin=12*mm,topMargin=12*mm,bottomMargin=12*mm)
story=[]
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PLAYER TENDENCIES',styles['ReportTitle']))
story.append(Paragraph('2026–27 season | Nine games | Official ladder: 9th, 4–5–0 | RF 53 | RA 63 | RD −10 | Last game: 6–1 loss vs Waverley (Nov 14)',styles['ReportSub']))
story.append(Paragraph('BATTING | NINE-GAME CUMULATIVE',styles['Sect']))
batcols=['Player','Bats','PA','AB','H','2B','3B','HR','BB','SO','AVG','OBP','SLG','OPS','ISO','BB%','SB']
def addtable(rows,cols,widths):
    data=[cols]+[[('' if ((k=='SB' and str(r.get(k,'')) in ['·','.','—','-']) or (k=='K/BB' and str(r.get(k,'')) in ['—','-'])) else str(r.get(k,'') or '')) for k in cols] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#15384e')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#dcebed')),('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor('#f2f6f8')]),('FONTSIZE',(0,0),(-1,-1),7.3),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),0.5,colors.HexColor('#95aebc'))]))
    story.append(t)
addtable(d['melbourne']['batting'],batcols,[112,29]+[35]*8+[38]*7)
story.append(Spacer(1,9))
story.append(Paragraph('* AVG is qualified at 18 PA (2 PA per 9 team games); only AVG has the qualification asterisk. OBP/OPS are estimates from H, BB, AB because historical HBP/SF/CI is incomplete. Unverified handedness and stolen bases display blank. RBI omitted by design.',styles['SmallNote']))
story.append(Paragraph('November 14 game 9 is supported by the supplied 38-column headers, and adds 10 hits (all singles), 1 BB, 1 HBP, 8 SO and 1 run. Earlier Sandringham game 8 remains provisional pending the headed box score.',styles['SmallNote']))
story.append(PageBreak())
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PITCHING & COACHING',styles['ReportTitle']))
story.append(Paragraph('PITCHING | NINE-GAME CUMULATIVE | Innings displayed as full innings plus outs',styles['Sect']))
pitcols=['Player','IP','H','BB','SO','ER','ERA','WHIP','K/9','BB/9','K/BB']
addtable(d['melbourne']['pitching'],pitcols,[155]+[60]*10)
story.append(Spacer(1,10))
story.append(Paragraph('* ERA qualifies at 3.0 IP (one recorded out per team game, 9 total outs). Only ERA carries the qualification asterisk. Waverley game pitching reconciles to 8.0 IP and 6 R (6 ER). Prior game 8 Perrett metrics remain provisional.',styles['SmallNote']))
story.append(Paragraph('LINEUP & COACHING USAGE',styles['Sect']))
notes=[
'November 14 vs Waverley: Melbourne collected 10 singles but scored once, with 8 strikeouts and just 1 walk. Emphasize productive contact, runner advancement and controlling two-strike approaches.',
'Oscar Hargreaves, Lochlann O\'Connor and Wade Mcconnon recorded two hits each. Ben Aslett reached on a single, walk and hit-by-pitch. A single outing is not an established lineup tendency.',
'Angus Saggers allowed 1 ER in 3.0 IP without a walk. Relievers allowed 5 ER over 5.0 IP; Simon Fitzmaurice conceded 4 ER in 2.2 IP. Recheck bullpen options and workload before the next game.',
'Joshua Hendricks remains the leading power source with 4 HR in the nine-game sample. Seek on-base opportunities ahead of him; against Moorabbin prioritize strike throwing and extra-base prevention.',
'Qualification standards are 18 PA (AVG) and 3.0 IP (ERA). Historical HBP/SF/CI gaps and previous provisional box-score entries remain documented.'
]
for n in notes:story.append(Paragraph('• '+n,styles['SmallNote']))
story.append(Paragraph('SOURCE & LIMITATIONS',styles['Sect']))
story.append(Paragraph('Official nine-game ladder and November 14 Waverley box score supplied by user. The earlier cumulative dataset was preserved as an archive. OBP/OPS estimates and Game 8 provisional data remain identified. Independent analysis, not official VSBL certification.',styles['SmallNote']))
doc.build(story)
lines=['MELBOURNE BASEBALL CLUB | NINE-GAME PLAYER & TEAM STATS','9th | 4-5-0 | RF 53 | RA 63 | RD -10 | Waverley L 1-6 (Nov 14)','','BATTING',' | '.join(batcols)]
for r in d['melbourne']['batting']:lines.append(' | '.join(str(r.get(k,'') or '') for k in batcols))
lines+=['','PITCHING',' | '.join(pitcols)]
for r in d['melbourne']['pitching']:lines.append(' | '.join(str(r.get(k,'') or '') for k in pitcols))
lines+=['','NOTES']+notes+['','Game 9 Waverley box score verified against supplied headers and final score; earlier Game 8 components provisional; OBP/OPS estimated.']
with open(txt,'w',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
print(out)
