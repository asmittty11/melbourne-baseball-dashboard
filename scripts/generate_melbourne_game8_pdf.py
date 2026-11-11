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
out=os.path.join(root,'reports','Melbourne_Season_Stats_Through_Game8_Sandringham_Updated.pdf')
txt=os.path.join(root,'text_reports','Melbourne_Season_Stats_Through_Game8_Sandringham_Updated.txt')
os.makedirs(os.path.dirname(out),exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportTitle',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=17,leading=21,textColor=colors.HexColor('#15384e'),spaceAfter=9))
styles.add(ParagraphStyle(name='ReportSub',parent=styles['Normal'],fontSize=9,leading=13,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallNote',parent=styles['Normal'],fontSize=8,leading=11,spaceAfter=7))
styles.add(ParagraphStyle(name='Sect',parent=styles['Heading2'],fontSize=12,textColor=colors.HexColor('#15384e'),spaceBefore=9,spaceAfter=7))
doc=SimpleDocTemplate(out,pagesize=landscape(A4),rightMargin=12*mm,leftMargin=12*mm,topMargin=12*mm,bottomMargin=12*mm)
story=[]
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PLAYER TENDENCIES',styles['ReportTitle']))
story.append(Paragraph('2026–27 season | Eight games | Official ladder: 8th, 4–4–0 | RF 52 | RA 57 | RD −5 | Last game: 5–1 win vs Sandringham',styles['ReportSub']))
story.append(Paragraph('BATTING | EIGHT-GAME CUMULATIVE',styles['Sect']))
batcols=['Player','Bats','PA','AB','H','2B','3B','HR','BB','SO','AVG','OBP','SLG','OPS','ISO','BB%','SB']
def addtable(rows,cols,widths):
    data=[cols]+[[str(r.get(k,'') or '') for k in cols] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#15384e')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#dcebed')),('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor('#f2f6f8')]),('FONTSIZE',(0,0),(-1,-1),7.3),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),0.5,colors.HexColor('#95aebc'))]))
    story.append(t)
addtable(d['melbourne']['batting'],batcols,[112,29]+[35]*8+[38]*7)
story.append(Spacer(1,9))
story.append(Paragraph('* AVG indicates fewer than 16 plate appearances (2 PA per team game). Only AVG carries a qualification asterisk. OBP/OPS are estimates from H, BB and AB because historical HBP/SF/CI are incomplete. Unknown handedness is blank. Stolen bases carry forward only when verified; a dot means unverified, not zero. RBI omitted by design.',styles['SmallNote']))
story.append(Paragraph('Game 8 player statistics were supplied without column headings. PA, AB, H and extra-base hits were mapped from the row structure; BB and SO remain provisional pending a headed box score.',styles['SmallNote']))
story.append(PageBreak())
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PITCHING & COACHING',styles['ReportTitle']))
story.append(Paragraph('PITCHING | EIGHT-GAME CUMULATIVE | Innings displayed as full innings plus outs',styles['Sect']))
pitcols=['Player','IP','H','BB','SO','ER','ERA','WHIP','K/9','BB/9','K/BB']
addtable(d['melbourne']['pitching'],pitcols,[155]+[60]*10)
story.append(Spacer(1,10))
story.append(Paragraph('* ERA indicates fewer than 2.2 IP (one recorded out per team game). Only ERA carries the qualification asterisk. Game 8 Perrett line provisionally interpreted as 6.0 IP, 4 H, 1 BB, 7 SO, 0 ER; confirm against the headed box score. Prior Game 7 pitcher-run discrepancy remains unresolved.',styles['SmallNote']))
story.append(Paragraph('LINEUP & COACHING USAGE',styles['Sect']))
notes=[
'Joshua Hendricks remains the primary power source (4 HR); maintain opportunities with runners on base. Oscar Hargreaves supplied two hits against Sandringham and retains a strong walk profile.',
'William Kent continues to provide contact consistency; Blake Mitchell remains a baserunning asset with six previously confirmed steals. New stolen-base events are not assumed from the unheaded columns.',
'Brennan, Pietersz, Mcconnon and Chinn contributed hits in the 5–1 win, supporting lineup depth. Avoid treating one game as a stable batting-order trend.',
'Taylor Perrett handled six innings in the latest supplied game. The provisional pitching line points to strong strikeout and walk control; confirm details before changing role recommendations.',
'Continue emphasizing free-base prevention and first-pitch strikes across the pitching staff. Historical player ER/H/BB figures and the Game 7 run discrepancy warrant verification.'
]
for n in notes:story.append(Paragraph('• '+n,styles['SmallNote']))
story.append(Paragraph('SOURCE & LIMITATIONS',styles['Sect']))
story.append(Paragraph('Official eight-game ladder snapshot provided by the user; seven-game cumulative player totals from archived Melbourne report; Sandringham GameDay player rows provided without headings. This is an independent analytical report, not an official VSBL statistical certification.',styles['SmallNote']))
doc.build(story)
lines=['MELBOURNE BASEBALL CLUB | EIGHT-GAME PLAYER & TEAM STATS','8th | 4-4-0 | RF 52 | RA 57 | RD -5 | Sandringham W 5-1','','BATTING',' | '.join(batcols)]
for r in d['melbourne']['batting']:lines.append(' | '.join(str(r.get(k,'') or '') for k in batcols))
lines+=['','PITCHING',' | '.join(pitcols)]
for r in d['melbourne']['pitching']:lines.append(' | '.join(str(r.get(k,'') or '') for k in pitcols))
lines+=['','NOTES']+notes+['','Game 8 columns unheaded: BB/SO and Perrett pitching components provisional. OBP/OPS estimated. Previous game pitching run discrepancy unresolved.']
with open(txt,'w',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
print(out)
