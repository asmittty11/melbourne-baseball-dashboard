#!/usr/bin/env python3
import json, os
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import mm

root=os.path.dirname(os.path.dirname(__file__))
with open(os.path.join(root,'data','melbourne_game11_snapshot.json'),encoding='utf-8') as f: d=json.load(f)
out=os.path.join(root,'reports','Melbourne_Season_Stats_Through_Game11_Sunshine_Updated.pdf')
txt=os.path.join(root,'text_reports','Melbourne_Season_Stats_Through_Game11_Sunshine_Updated.txt')
os.makedirs(os.path.dirname(out),exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportTitle',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=17,leading=21,textColor=colors.HexColor('#15384e'),spaceAfter=9))
styles.add(ParagraphStyle(name='ReportSub',parent=styles['Normal'],fontSize=9,leading=13,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallNote',parent=styles['Normal'],fontSize=8,leading=11,spaceAfter=7))
styles.add(ParagraphStyle(name='Sect',parent=styles['Heading2'],fontSize=12,textColor=colors.HexColor('#15384e'),spaceBefore=9,spaceAfter=7))
doc=SimpleDocTemplate(out,pagesize=landscape(A4),rightMargin=12*mm,leftMargin=12*mm,topMargin=12*mm,bottomMargin=12*mm)
story=[]
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PLAYER TENDENCIES',styles['ReportTitle']))
story.append(Paragraph('2026–27 season | 11 supplied player games | Official: 12 G, 9th, 5–6–1 | RF 67 | RA 89 | RD −22 | Latest official: 9–8 win at Malvern; player box pending',styles['ReportSub']))
story.append(Paragraph('BATTING | ELEVEN SUPPLIED PLAYER GAMES',styles['Sect']))
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
story.append(Paragraph('* AVG qualifies at 24 PA (2 per 12 official games): only AVG carries the asterisk. OBP/OPS estimates use H, BB and AB because historical HBP, SF, CI are incomplete. Unknown hands and SB blank; 9 team steals are documented minimums. RBI omitted by design.',styles['SmallNote']))
story.append(Paragraph('November 21 Sunshine loss adds 9 H, 1 double, 2 HR (Aslett and O\'Connor), 2 BB, 9 SO and 5 R. Lennard Pietersz row lists 4 PA/4 AB/1 sac bunt, a source conflict. Nov 24 Malvern 9–8 win is standings-only pending its box; Game 8 Perrett remains provisional.',styles['SmallNote']))
story.append(PageBreak())
story.append(Paragraph('MELBOURNE BASEBALL CLUB | PITCHING & COACHING',styles['ReportTitle']))
story.append(Paragraph('PITCHING | ELEVEN SUPPLIED PLAYER GAMES | Innings displayed as full innings plus outs',styles['Sect']))
pitcols=['Player','IP','H','BB','SO','ER','ERA','WHIP','K/9','BB/9','K/BB']
# ERA low-to-high; ignore asterisk for comparison; team total stays last.
pitrows=sorted((r for r in d['melbourne']['pitching'] if not r.get('Team Total')),
               key=lambda r:(rate(r,'ERA'),str(r.get('Player','')).casefold()))
pitrows += [r for r in d['melbourne']['pitching'] if r.get('Team Total')]
addtable(pitrows,pitcols,[155]+[60]*10)
story.append(Spacer(1,10))
story.append(Paragraph('* ERA qualifies at 12 outs (4.0 IP), one out per 12 official team games. Only ERA carries *. Sunshine supplied pitching: 8.0 IP, 19 H, 8 BB, 9 SO, 18 R / 11 ER. The Malvern 9–8 victory player pitching stats are not supplied. Prior Game 8 Perrett remains provisional.',styles['SmallNote']))
story.append(Paragraph('LINEUP & COACHING USAGE',styles['Sect']))
notes=[
"Sunshine 18–5 loss (November 21): 9 hits, including Ben Aslett and Lochlann O'Connor home runs, plus Harvey Chinn's double; 5 runs on 35 reported PA and 9 strikeouts to 2 walks.",
"Joshua Hendricks still has four tracked homers. Aslett and O'Connor supplied the other two. Oscar Hargreaves (11 hits, 6 walks) and Blake Mitchell (9 hits, 8 walks) remain useful baserunner-creation options subject to lineup and RISP confirmation.",
"Six Melbourne pitchers allowed 18 R / 11 ER over 8.0 IP, giving up 19 H and 8 BB; Simon Fitzmaurice yielded 8 R / 7 ER on 10 hits in 3.1 IP. Henry Mcintyre was charged with 7 R / 1 ER and four walks in 0.1 IP. Verify the scorer's earned/unearned assignments before attributing causes.",
"Joey White worked one scoreless inning with two strikeouts; Blake Mitchell contributed 0.2 scoreless IP with one strikeout. Prior appearances and 12-game qualification rules should inform any available-arm assessment.",
"Melbourne's November 24 9–8 road win over Malvern improves the official record to 5–6–1 (ninth place) but its individual batting/pitching game lines are still pending. Team RF 67 / RA 89 differ from the eleven-game player batch totals.",
"2026–27 top-eight playoff cutoff: Melbourne is ninth, immediately behind Cheltenham in the dated Nov 24 ladder. Qualification: AVG 24 PA, ERA 4.0 IP; prior sacrifice-bunt source inconsistencies and older Game 8 pitching remain flagged."
]
for n in notes:story.append(Paragraph('• '+n,styles['SmallNote']))
story.append(Paragraph('SOURCE & LIMITATIONS',styles['Sect']))
story.append(Paragraph('November 24 16-team official ladder and Sunshine Nov 21 full GameDay player rows supplied by user. Eleven-game cumulative archive frozen; 12 official games. Malvern Nov 24 9–8 win player box missing. Historic OBP/OPS estimated, sac-bunt/PA conflicts and Game 8 entry provisional. Independent coaching analysis, not official VSBL certification.',styles['SmallNote']))
doc.build(story)
lines=['MELBOURNE BASEBALL CLUB | ELEVEN SUPPLIED PLAYER GAMES / TWELVE OFFICIAL GAMES','9th | 5-6-1 | RF 67 | RA 89 | RD -22 | Sunshine L 5-18 (Nov 21) + Malvern W 9-8 (Nov 24, player box pending)','','BATTING',' | '.join(batcols)]
for r in batrows:lines.append(' | '.join('' if k=='SB' and str(r.get(k,'')) in ['·','.','—','-'] else str(r.get(k,'') or '') for k in batcols))
lines+=['','PITCHING',' | '.join(pitcols)]
for r in pitrows:lines.append(' | '.join(str(r.get(k,'') or '') for k in pitcols))
lines+=['','NOTES']+notes+['','11th player batch Nov 21 Sunshine reconciled at 5 scored / 18 allowed (11 ER); Malvern Nov 24 win official only, missing individual game stats. Sacrifice-bunt/PA conflicts and Game 8 remain provisional.']
with open(txt,'w',encoding='utf-8') as f:f.write('\n'.join(lines)+'\n')
print(out)
