#!/usr/bin/env python3
import json, os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm

root=os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(root,'data','melbourne_game12_snapshot.json'),encoding='utf-8') as f: d=json.load(f)
out=os.path.join(root,'reports','Melbourne_Season_Stats_Through_Game12_Malvern_Updated.pdf')
txt=os.path.join(root,'text_reports','Melbourne_Season_Stats_Through_Game12_Malvern_Updated.txt')
os.makedirs(os.path.dirname(out),exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportTitle',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=17,leading=21,textColor=colors.HexColor('#15384e'),spaceAfter=9))
styles.add(ParagraphStyle(name='ReportSub',parent=styles['Normal'],fontSize=9,leading=13,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallNote',parent=styles['Normal'],fontSize=8,leading=11,spaceAfter=7))
styles.add(ParagraphStyle(name='Sect',parent=styles['Heading2'],fontSize=12,textColor=colors.HexColor('#15384e'),spaceBefore=9,spaceAfter=7))
doc=SimpleDocTemplate(out,pagesize=landscape(A4),rightMargin=12*mm,leftMargin=12*mm,topMargin=12*mm,bottomMargin=12*mm)
story=[]
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PLAYER TENDENCIES',styles['ReportTitle']))
story.append(Paragraph('2026–27 season | 12 supplied games | Official: 12 G, 9th, 5–6–1 | RF 67 | RA 89 | RD −22 | Latest: 9–8 away win vs Malvern (full player box included)',styles['ReportSub']))
story.append(Paragraph('BATTING | TWELVE SUPPLIED PLAYER GAMES',styles['Sect']))
batcols=['Player','Bats','PA','AB','H','2B','3B','HR','BB','SO','AVG','OBP','SLG','OPS','ISO','BB%','SB']
def addtable(rows,cols,widths):
    data=[cols]+[[('' if ((k=='SB' and str(r.get(k,'')) in ['·','.','—','-']) or (k=='K/BB' and str(r.get(k,'')) in ['—','-'])) else str(r.get(k,'') or '')) for k in cols] for r in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#15384e')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'),('BACKGROUND',(0,-1),(-1,-1),colors.HexColor('#dcebed')),('ROWBACKGROUNDS',(0,1),(-1,-2),[colors.white,colors.HexColor('#f2f6f8')]),('FONTSIZE',(0,0),(-1,-1),7.3),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),0.5,colors.HexColor('#95aebc'))]))
    story.append(t)
# Preserve the team total at the bottom, and order Melbourne hitters by numeric OPS, highest first.
def rate(row, metric):
    value=str(row.get(metric,'')).replace('*','').strip()
    try:
        return float(value)
    except ValueError:
        return float('inf') if metric=='ERA' else float('-inf')
batrows=sorted((r for r in d['melbourne']['batting'] if not r.get('Team Total')),
               key=lambda r:(-rate(r,'OPS'),str(r.get('Player','')).casefold()))
batrows += [r for r in d['melbourne']['batting'] if r.get('Team Total')]
addtable(batrows,batcols,[112,29]+[35]*8+[38]*7)
story.append(Spacer(1,9))
story.append(Paragraph('* AVG qualifies at 24 PA (2 per 12 official games): only AVG carries the asterisk. OBP/OPS estimates use H, BB and AB because historical HBP, SF, CI are incomplete. Unknown hands and SB blank; 10 documented steals are minimums. RBI omitted by design.',styles['SmallNote']))
story.append(Paragraph('November 24 Malvern win: 9 H, 1 double, 1 HR, 6 BB, 2 HBP, 3 SO, 1 SB, 9 R. Zak Skinner 4-for-4, HR, double and 5 RBI. Source also records 4 PA / 4 AB / 1 sac bunt for Skinner; scoring conflict flagged. Game 8 Perrett remains provisional.',styles['SmallNote']))
story.append(PageBreak())
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PITCHING & COACHING',styles['ReportTitle']))
story.append(Paragraph('PITCHING | TWELVE SUPPLIED PLAYER GAMES | Innings displayed as full innings plus outs',styles['Sect']))
pitcols=['Player','IP','H','BB','SO','ER','ERA','WHIP','K/9','BB/9','K/BB']
# ERA low-to-high; ignore asterisk for comparison; team total stays last.
pitrows=sorted((r for r in d['melbourne']['pitching'] if not r.get('Team Total')),
               key=lambda r:(rate(r,'ERA'),str(r.get('Player','')).casefold()))
pitrows += [r for r in d['melbourne']['pitching'] if r.get('Team Total')]
addtable(pitrows,pitcols,[155]+[60]*10)
story.append(Spacer(1,10))
story.append(Paragraph('* ERA qualifies at 12 outs (4.0 IP), one out per 12 official team games. Only ERA carries *. Malvern game pitching: 5.0 IP, 8 H, 8 BB, 3 SO, 8 R / 8 ER across three pitchers. Official 12-game team runs unchanged. Prior Game 8 Perrett remains provisional.',styles['SmallNote']))
story.append(Paragraph('LINEUP & COACHING USAGE',styles['Sect']))
notes=[
"Malvern 9–8 win (Nov 24): 9 hits, including Zak Skinner 4-for-4 (double, home run, five RBI and steal); Wade Mcconnon two hits, two runs; Blake Mitchell three walks, two runs.",
"Game-level discipline: six walks and two HBP helped create traffic with only three strikeouts. This alone does not establish pitch selection without video or the lineup card.",
"Staff threw five documented innings and allowed eight runs, all earned, on eight hits and eight walks. Charles Chislett: 2.1 IP, 3 H, 6 BB, 6 R/ER. Walk prevention should be a primary coaching emphasis.",
"Joey White recorded 1.0 scoreless IP (1 H, 1 BB, 1 SO); Max Saggers: 1.2 IP, 4 H, 1 BB, 1 SO, 2 R/ER. Do not infer appearance order or current rest from a batting/pitching summary alone.",
"Skinner's 18 cumulative PA and 1.222 estimated OPS are promising but still a limited batting sample for Melbourne's 24-PA AVG qualification. Zak's 4 PA/4 AB and one listed sacrifice bunt conflict in the source.",
"Official 5-6-1 record, 9th place, RF 67, RA 89 remains unchanged: the Malvern victory was included in the league ladder before player stats arrived. Melbourne sits one spot outside the top-eight playoff cutoff."
]
for n in notes:story.append(Paragraph('• '+n,styles['SmallNote']))
story.append(Paragraph('SOURCE & LIMITATIONS',styles['Sect']))
story.append(Paragraph('November 24 16-team official ladder plus November 24 Malvern 38-column GameDay player rows supplied by user. Twelve official games and twelve player-stat batches; 67 R in player boxes and the official RF reconcile. Historical OBP/OPS estimated; Zak Skinner 4 PA / 4 AB / one sac bunt conflict, older sacrifice-bunt issues and Game 8 pitching remain provisional. Independent coaching analysis, not official VSBL certification.',styles['SmallNote']))
doc.build(story)
lines=['MELBOURNE BASEBALL CLUB | TWELVE SUPPLIED PLAYER GAMES / TWELVE OFFICIAL GAMES','9th | 5-6-1 | RF 67 | RA 89 | RD -22 | Malvern W 9-8 (Nov 24; player box included exactly once)','','BATTING',' | '.join(batcols)]
for r in batrows:lines.append(' | '.join('' if k=='SB' and str(r.get(k,'')) in ['·','.','—','-'] else str(r.get(k,'') or '') for k in batcols))
lines+=['','PITCHING',' | '.join(pitcols)]
for r in pitrows:lines.append(' | '.join(str(r.get(k,'') or '') for k in pitcols))
lines+=['','COACHING NOTES']+notes+['','Nov24 Malvern: 9 R, 9 H, 6 BB, 3 SO, 1 SB; pitching 5.0 IP, 8 H, 8 BB, 3 SO, 8 R/ER. Source Zak Skinner sac-bunt/PA issue and older game caveats persist.']
with open(txt,'w',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
print(out)
