import json,os
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer,PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import landscape,A4
from reportlab.lib.units import mm
root=os.path.dirname(os.path.dirname(__file__))
d=json.load(open(os.path.join(root,'data/waverley_preliminary_20261109.json')))
m=d['metadata']
name='Melbourne_vs_Waverley_Advance_Scouting_Nov14_2026_Five_Game_Update'
pdf=os.path.join(root,'reports',name+'.pdf')
txt=os.path.join(root,'text_reports',name+'.txt')
os.makedirs(os.path.dirname(pdf),exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='H',parent=styles['Title'],fontSize=17,leading=20,textColor=colors.HexColor('#15384e')))
styles.add(ParagraphStyle(name='S',parent=styles['Normal'],fontSize=9,leading=13,spaceAfter=9))
styles.add(ParagraphStyle(name='N',parent=styles['Normal'],fontSize=8,leading=11,spaceAfter=7))
story=[Paragraph('MELBOURNE vs WAVERLEY | ADVANCE SCOUTING',styles['H']),Paragraph('Saturday 14 November 2026 | Melbourne away | Waverley 3rd (5–0–0), 58 RF, 11 RA, +47 | Melbourne 8th (4–4–0), 52 RF, 57 RA, −5',styles['S']),Paragraph('WAVERLEY BATTING | CUMULATIVE AVAILABLE GAME DATA',styles['Heading2'])]
batcols=['Player','G','PA','AB','H','2B','3B','HR','RBI','BB','SO','SB','AVG','OBP','SLG','OPS','ISO','BB%','Scouting Read']
pitcols=['Player','Throws','G','IP','H','ER','BB','SO','ERA','WHIP','K/9','BB/9','Scouting Read']
def table(rows,cols,widths):
    cells=[cols]+[[str(r.get(c,'') if r.get(c,'') is not None else '') for c in cols] for r in rows]
    t=Table(cells,colWidths=widths,repeatRows=1)
    commands=[('BACKGROUND',(0,0),(-1,0),colors.HexColor('#15384e')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),7),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f2f6f8')]),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    for i,r in enumerate(rows,1):
        c=r.get('Scouting Read','')
        color={'THREAT':'#ffd1d1','CAUTION':'#ffe6a1','ATTACK':'#ccebd8','LIMITED':'#e3e6e9'}.get(c)
        if color:commands.append(('BACKGROUND',(-1,i),(-1,i),colors.HexColor(color)))
    t.setStyle(TableStyle(commands));story.append(t)
batrows=sorted(d['batting'],key=lambda x:float(str(x.get('OPS','0')).replace('—','0')) if str(x.get('OPS','0'))!='—' else 0,reverse=True)
bat_total={'Player':'TEAM TOTAL'}
for k in ['PA','AB','H','2B','3B','HR','RBI','BB','SO','SB']:
    bat_total[k]=sum(int(p.get(k,0)) for p in d['batting'])
ab=bat_total['AB'];h=bat_total['H'];bb=bat_total['BB']
bat_total['AVG']=f'{h/ab:.3f}' if ab else '—'
bat_total['SLG']=f'{(h+bat_total["2B"]+2*bat_total["3B"]+3*bat_total["HR"])/ab:.3f}' if ab else '—'
den=ab+bb+sum(int(p.get('HBP',0))+int(p.get('SF',0)) for p in d['batting'])
obp=(h+bb+sum(int(p.get('HBP',0)) for p in d['batting']))/den if den else 0
slg=(h+bat_total["2B"]+2*bat_total["3B"]+3*bat_total["HR"])/ab if ab else 0
bat_total['OBP']=f'{obp:.3f}'
bat_total['OPS']=f'{obp+slg:.3f}'
bat_total['ISO']=f'{slg-h/ab:.3f}' if ab else '—'
bat_total['BB%']=f'{100*bb/sum(int(p.get("PA",0)) for p in d["batting"]):.1f}%'
table(batrows+[bat_total],batcols,[110]+[31]*11+[38]*6+[77])
story.extend([Spacer(1,9),Paragraph('SCOUTING READ: red = priority threat; yellow = caution; green = attack; gray = insufficient sample. AVG asterisks only below 2 PA per team game (10 PA through five games). Unknown handedness is blank. Player totals incorporate available game records and may not cover all five official games.',styles['N']),PageBreak(),Paragraph('WAVERLEY PITCHING | MATCHUP PREPARATION',styles['H'])])
table(d['pitching'],pitcols,[135,43]+[46]*10+[88])
story.extend([Spacer(1,9),Paragraph('ERA asterisk only below one out per team game (1.2 IP through five games). New game pitching row was supplied without headings, so its mapping and derived rates are provisional. Previously verified Conor Myles throws left-handed; other unverified hands remain blank.',styles['N']),Paragraph('LINEUP & COACHING USAGE',styles['Heading2'])])
notes=[
'Waverley is unbeaten (5–0) with 58 runs scored and 11 allowed; the newest official ladder adds a 4–3 result. Do not equate this with a verified five-game individual-stat dataset.',
'Cooper Busch, Damon Hill, Charlie Collins and Benjamin Fierenzi remain primary power/on-base concerns based on available cumulative data. Avoid predictable fastballs in damage counts.',
'Oliver Dunn and Reece Longstaff contributed extra-base hits in the newest supplied rows. Prepare for aggressive baserunning, but do not infer new steals from ambiguous fields.',
'Pitching preparation: Cooper Busch has a strong earlier four-inning outing; Kai Reum and Kynan Jones have the most established recorded workloads. Recheck their newest pitching lines against a headed scorecard.',
'Melbourne should emphasize baserunner control, avoiding walks and limiting extra-base damage. Actual lineup positions and substitutions across five games are not fully verified.'
]
for n in notes:story.append(Paragraph('• '+n,styles['N']))
story.append(Paragraph('NOTABLE HIGHER-LEVEL PLAYING EXPERIENCE',styles['Heading2']))
for e in d['metadata'].get('higherExperience',[]):
    story.append(Paragraph(e['Player']+': '+e['Experience']+' ('+e['Source']+')',styles['N']))
story.append(Paragraph('DATA QUALITY',styles['Heading2']))
story.append(Paragraph('Official ladder five-game record, RF/RA and positions are verified from the supplied screenshot. New GameDay rows lack column headings; player-specific totals and classifications are provisional. The five named pitchers total 27.2 IP and 9 ER, an incomplete sample of five games. Missing pitching appearances remain unidentified. Earlier dataset had four reported games and does not necessarily reconcile to the five official games. No missing games were fabricated.',styles['N']))
SimpleDocTemplate(pdf,pagesize=landscape(A4),leftMargin=11*mm,rightMargin=11*mm,topMargin=11*mm,bottomMargin=11*mm).build(story)
with open(txt,'w') as f:
 f.write('MELBOURNE vs WAVERLEY | 14 NOV 2026\nWaverley 3rd 5-0-0 58 RF 11 RA +47 | Melbourne 8th 4-4-0 52 RF 57 RA -5\nBATTING\n')
 for p in d['batting']+[bat_total]:f.write(' | '.join(str(p.get(k,'')) for k in batcols)+'\n')
 f.write('PITCHING\n')
 for p in d['pitching']+[pit_total]:f.write(' | '.join(str(p.get(k,'')) for k in pitcols)+'\n')
 f.write('COACHING\n'+'\n'.join(notes)+'\nUnheaded newest game rows; player components provisional.\n')
print(pdf)
