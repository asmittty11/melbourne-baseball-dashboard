#!/usr/bin/env python3
import json, os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm

root=os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(root,'data','melbourne_game10_snapshot.json'),encoding='utf-8') as f: d=json.load(f)
out=os.path.join(root,'reports','Melbourne_Season_Stats_Through_Game10_Moorabbin_Updated.pdf')
txt=os.path.join(root,'text_reports','Melbourne_Season_Stats_Through_Game10_Moorabbin_Updated.txt')
os.makedirs(os.path.dirname(out),exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportTitle',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=17,leading=21,textColor=colors.HexColor('#15384e'),spaceAfter=9))
styles.add(ParagraphStyle(name='ReportSub',parent=styles['Normal'],fontSize=9,leading=13,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallNote',parent=styles['Normal'],fontSize=8,leading=11,spaceAfter=7))
styles.add(ParagraphStyle(name='Sect',parent=styles['Heading2'],fontSize=12,textColor=colors.HexColor('#15384e'),spaceBefore=9,spaceAfter=7))
doc=SimpleDocTemplate(out,pagesize=landscape(A4),rightMargin=12*mm,leftMargin=12*mm,topMargin=12*mm,bottomMargin=12*mm)
story=[]
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PLAYER TENDENCIES',styles['ReportTitle']))
story.append(Paragraph('2026–27 season | Ten games | Official ladder: 8th, 4–5–1 | RF 53 | RA 63 | RD −10 | Last game: 0–0 draw vs Moorabbin (Nov 17)',styles['ReportSub']))
story.append(Paragraph('BATTING | TEN-GAME CUMULATIVE',styles['Sect']))
batcols=['Player','Bats','PA','AB','H','2B','3B','HR','BB','SO','AVG','OBP','SLG','OPS','ISO','BB%','SB']
def addtable(rows,cols,widths):
    data=[cols]+[[('' if ((k=='SB' and str(r.get(k,'')) in ['·','.','—','-']) or (k=='K/BB' and str(r.get(k,'')) in ['—','-'])) else str(r.get(k,'') or '')) for k in cols] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#15384e')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#dcebed')),('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor('#f2f6f8')]),('FONTSIZE',(0,0),(-1,-1),7.3),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),0.5,colors.HexColor('#95aebc'))]))
    story.append(t)
addtable(d['melbourne']['batting'],batcols,[112,29]+[35]*8+[38]*7)
story.append(Spacer(1,9))
story.append(Paragraph('* AVG qualifies at 20 PA (2 per 10 games): only AVG has the asterisk. OBP/OPS are estimates because historic HBP, SF and CI are incomplete. Unverified handedness and stolen bases blank; Zak Skinner 1+ indicates at least one recorded stolen base. RBI omitted by design.',styles['SmallNote']))
story.append(Paragraph('November 17 game 10 adds four singles, two walks, five offensive strikeouts and one recorded stolen base. Zak Skinner sacrifice bunt conflicts with his supplied PA/AB/BB counts; source unchanged pending verification. Game 8 Perrett pitching provisional.',styles['SmallNote']))
story.append(PageBreak())
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PITCHING & COACHING',styles['ReportTitle']))
story.append(Paragraph('PITCHING | TEN-GAME CUMULATIVE | Innings displayed as full innings plus outs',styles['Sect']))
pitcols=['Player','IP','H','BB','SO','ER','ERA','WHIP','K/9','BB/9','K/BB']
addtable(d['melbourne']['pitching'],pitcols,[155]+[60]*10)
story.append(Spacer(1,10))
story.append(Paragraph('* ERA qualifies at 10 outs (3.1 IP), one out per ten team games. Only ERA carries *. New pitchers total 6.0 scoreless IP, 7 H, 9 SO and 0 BB. Earlier Sandringham Game 8 Perrett inputs remain provisional.',styles['SmallNote']))
story.append(Paragraph('LINEUP & COACHING USAGE',styles['Sect']))
notes=[
"November 17 0–0 draw vs Moorabbin: four singles and two walks, five offensive strikeouts, no runs. Wade Mcconnon collected two singles; Harvey Chinn and Oscar Hargreaves had one apiece.",
"Zak Skinner drew a walk and recorded one stolen base. A listed sacrifice bunt conflicts with 2 PA, 1 AB and 1 BB; verify before inferring bunting tactics.",
"Taylor Perrett: 5.0 IP, 6 H, 7 SO, 0 BB, 0 ER; Joey White: 1.0 IP, 1 H, 2 SO, 0 BB, 0 ER. Their combined 6.0 IP, 9 SO and no walks offer a positive command indicator, without inferring an additional inning.",
"Joshua Hendricks remains the leading documented power bat with four homers; Blake Mitchell (8 BB, 6 verified SB) and Oscar Hargreaves (9 H, 6 BB) offer on-base contributions, subject to current lineup and defense.",
"Sunshine official ladder: 5th, 6-3-0, +35. Malvern: 2nd, 8-1-0, +47. The existing opponent player samples exclude their latest unavailable individual box scores.",
"Qualification: AVG 20 PA, ERA 3.1 IP. Historical OBP/OPS estimates and provisional Game 8 Perrett pitching values remain labeled."
]
for n in notes:story.append(Paragraph('• '+n,styles['SmallNote']))
story.append(Paragraph('SOURCE & LIMITATIONS',styles['Sect']))
story.append(Paragraph('Official ten-game ladder and November 17 Moorabbin player rows supplied by user. Original nine-game archive remains frozen. Historical OBP/OPS estimated, sacrifice bunt PA conflict flagged, older Game 8 pitcher input provisional. Not official VSBL certification.',styles['SmallNote']))
doc.build(story)
lines=['MELBOURNE BASEBALL CLUB | TEN-GAME PLAYER & TEAM STATS','8th | 4-5-1 | RF 53 | RA 63 | RD -10 | Moorabbin D 0-0 (Nov 17)','','BATTING',' | '.join(batcols)]
for r in d['melbourne']['batting']:lines.append(' | '.join(str(r.get(k,'') or '') for k in batcols))
lines+=['','PITCHING',' | '.join(pitcols)]
for r in d['melbourne']['pitching']:lines.append(' | '.join(str(r.get(k,'') or '') for k in pitcols))
lines+=['','NOTES']+notes+['','Game 10 Moorabbin data verified against supplied GameDay rows; sacrifice bunt/PA discrepancy flagged; Game 8 provisional; OBP/OPS estimated.']
with open(txt,'w',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
print(out)
