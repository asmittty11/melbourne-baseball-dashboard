#!/usr/bin/env python3
"""Publish approved preliminary Malvern report using the established VSBL advance-scouting layout."""
import json
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import landscape, A4
from advance_report_sort import sort_batters_by_ops

ROOT=Path(__file__).resolve().parent.parent
source=json.loads((ROOT/"data/malvern_preliminary_nov24_2026.json").read_text(encoding="utf-8"))
stem="Melbourne_vs_Malvern_Advance_Scouting_Preliminary_Nov24_2026"
pdf=ROOT/"reports"/(stem+".pdf")
txt=ROOT/"text_reports"/(stem+".txt")
pdf.parent.mkdir(parents=True, exist_ok=True)
txt.parent.mkdir(parents=True, exist_ok=True)
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name="SmallX",fontName="Helvetica",fontSize=8.3,leading=12,spaceAfter=6))
styles.add(ParagraphStyle(name="HeadX",fontName="Helvetica-Bold",fontSize=15,leading=19,textColor=colors.HexColor("#183654"),spaceAfter=9))
story=[]
def para(t,style="SmallX"):
    story.append(Paragraph(t,styles[style]))
def heading(t):
    para(t,"HeadX")
def table(columns,records,widths):
    cells=[[{"AVG":"AVG*","ERA":"ERA*","Scouting Read":"SCOUTING READ"}.get(k,k) for k in columns]]+[[str(r.get(k,"") or "").upper() if r.get("Team Total") and k=="Scouting Read" else str(r.get(k,"") or "") for k in columns] for r in records]
    t=Table(cells,colWidths=widths,repeatRows=1,hAlign="LEFT")
    style=[("BACKGROUND",(0,0),(-1,0),colors.HexColor("#173b5e")),
      ("TEXTCOLOR",(0,0),(-1,0),colors.white),
      ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
      ("FONTSIZE",(0,0),(-1,-1),7),
      ("GRID",(0,0),(-1,-1),.25,colors.HexColor("#d7e1e8")),
      ("ROWBACKGROUNDS",(0,1),(-1,-2),[colors.white,colors.HexColor("#edf3f7")]),
      ("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#dbe7ee")),
      ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
      ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
      ("BOTTOMPADDING",(0,0),(-1,-1),4),
      ("TOPPADDING",(0,0),(-1,-1),4)]
    palette={"THREAT":"#ffd1d1","STRONG":"#ffd1d1","CAUTION":"#ffe6a1","ATTACK":"#ccebd8",
             "LIMITED":"#e3e6e9"}
    last=len(columns)-1
    for i,r in enumerate(records,1):
        if r.get("Team Total"): continue
        color=palette.get(str(r.get("Scouting Read","")).upper())
        if color: style.append(("BACKGROUND",(last,i),(last,i),colors.HexColor(color)))
    t.setStyle(TableStyle(style))
    story.append(t)
    story.append(Spacer(1,12))


heading("MELBOURNE vs MALVERN | ADVANCE SCOUTING")
para("<b>Tuesday 24 November 2026 | Away at Malvern Braves | Start time unconfirmed | PRELIMINARY</b>")
para("<b>Official ladder (Nov 18 screenshot):</b> Malvern 2nd, 8-1-0, 70 RF, 23 RA, +47 RD (9 games); Melbourne 8th, 4-5-1, 53 RF, 63 RA, -10 RD (10 games). Records are verified against the supplied screenshot; reconfirm any further games before sending.")
para("<b>Data scope:</b> Seven supplied Malvern player batches, nine official games. The seven batches contain 55 runs scored, 19 allowed and 58.0 identified pitching IP; individual statistics for two additional games are unavailable. No missing performance or batting order was inferred. The new official ladder supersedes the prior 8-0-0 snapshot.")
heading("TEAM TENDENCIES & MATCHUP")
para("Malvern: 7.78 runs scored and 2.56 allowed per official game. Melbourne: 5.30 scored and 6.30 against over ten. Malvern are now second at +47; Melbourne eighth at -10. Malvern seven-batch batting sample has 82 H, 7 HR, .371 AVG, .424 estimated OBP and .962 OPS; these do not cover all nine official games.")
para("<b>Offensive read:</b> Tyler Luther-Wilson has hit .571 with two homers and 1.577 OPS in 26 supplied PA; Jarryd Dale is .588 with 1 HR and 1.564 OPS over 22 PA. Hudson Priamo has 11 hits in 26 AB with a .983 OPS. Ulrich Bojarski has 1 HR and a 1.000 OPS but only 14 recorded PA (LIMITED under eight-game qualification). Focus on the demonstrated power threats, especially with runners aboard.")
para("<b>Pitching read:</b> Malvern have 11 recorded ER in 58.0 supplied innings (1.71 sample ERA). Matthew Beattie 10.0 IP/0 ER; Zaid Elias Cummins Flynn 14.0 IP/2 ER; James Squire 11.2 IP/3 ER, while Mitchell Kennedy has 17.0 IP/5 ER. Missing game exposure prevents a full rotation or rest assessment. For any projected starter, confirm 21-22 November usage first.")
heading("BATTING | SEVEN SUPPLIED GAME BATCHES")
bat=source["batting"]
batplayers=sort_batters_by_ops(bat)
batteam=next(x for x in bat if x.get("Team Total"))
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
batrows=batplayers+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* Batting AVG qualification: 18 PA (2 per 9 official team games), with * only beside AVG. OBP=(H+BB+HBP)/(AB+BB+HBP+SF) on available player rows, ISO=SLG-AVG. Scouting classifications THREAT red, CAUTION yellow, ATTACK green, LIMITED gray. Unverified handedness blank. Team total seven supplied batches only.")
heading("PITCHING | IDENTIFIED APPEARANCES")
pit=source["pitching"]
pitplayers=sorted([x for x in pit if not x.get("Team Total")],key=lambda x:-(int(x["IP"].split(".")[0])*3+int(x["IP"].split(".")[1])))
pitteam=next(x for x in pit if x.get("Team Total"))
pitcols=["Player","Throws","IP","H","R","ER","BB","HBP","SO","ERA","WHIP","K/9","BB/9","Scouting Read"]
table(pitcols,pitplayers+[pitteam],[125,35,35]+[35]*6+[42]*4+[85])
para("* ERA qualification: 9 outs (3.0 IP), one out per 9 official team games, with * only on ERA. IP shows innings and outs. Scouting read: STRONG red, CAUTION yellow, ATTACK green, LIMITED gray. Unknown handedness blank; recorded team ERA covers seven pitching batches (58.0 IP), not all nine games.")
heading("COACHING & LINEUP USAGE")
notes=[
"1. Malvern's recently supplied lineup has repeatedly involved Hudson Priamo, Jack Hanger, Jarryd Dale, Matthew Johnston and Tyler Luther-Wilson. Do not treat a single order as definitive: confirm the most recent lineup after the weekend game.",
"2. Prioritize Jarryd Dale, Tyler Luther-Wilson and Hudson Priamo for focused pitch plans; they show the strongest qualified OPS results. Ulrich Bojarski brings a much stronger higher-level playing background than his 14-PA small sample reveals.",
"3. Against pitcher Matthew Beattie (10.0 IP, 0 ER in available games), prepare to manufacture pressure rather than expect sustained walks. Zaid Flynn and James Squire also have strong recorded run prevention; do not assume availability without the latest game log.",
"4. Be ready for strikeouts: Malvern's 58.0 documented IP contain 82 SO (12.72 K/9). Emphasize two-strike adjustments, baserunner advancement and situational contact after Melbourne's recent ten-single, one-run result versus Waverley.",
"5. The seven supplied Malvern batting batches show 12 SB; use controlled running-game opportunities, verify actual catcher/pitcher response, and avoid projecting verified steal totals onto games with missing data.",
"6. Recheck the Malvern, Melbourne and Sunshine ladder entries before sending either advance report to the club. The upcoming fixtures can change records and qualifier thresholds before November 24."
]
for n in notes: para(n)
heading("HIGHER-LEVEL EXPERIENCE / VERIFICATION")
para("<b>Jarryd Dale (R/R):</b> Melbourne Aces ABL, San Diego Padres minors through Triple-A, Orix Buffaloes Japanese farm system, KIA Tigers KBO in 2026, Team Australia WBC. Source: Baseball Australia and MLB/MiLB player profiles (baseball.com.au/news/dale-kbo/).")
para("<b>Ryan Dale (R/R):</b> Nine ABL seasons with Melbourne Aces as of 2020-21 and Kansas City Royals organization (rookie leagues), plus Dutch Hoofdklasse. Source: Melbourne Aces 2020-21 media guide (assets.melbourneaces.com.au, V6 guide).")
para("<b>Ulrich Bojarski (R/R):</b> Detroit Tigers system through Double-A Erie; longstanding ABL hitter and Australian WBC/Premier12 representative. Sources: Baseball Australia 2026 WBC media notes and theABL player profile.")
para("<b>Chris Burke:</b> Named on the Melbourne Aces 2022 ABL roster, with Malvern local affiliation in earlier Aces media notes. <b>Tyler Luther-Wilson:</b> Experienced Geelong VSBL Division 1 catcher with U.S. high school baseball; ABL/MiLB level not confirmed. <b>Brady Whalen:</b> Name matches a minor-league profile, but Malvern identity is unverified; no professional affiliation asserted.")
heading("DATA QUALITY & NEXT UPDATE")
para("Official ladder supplied November 18: Malvern 8-1-0 (70 RF, 23 RA), Melbourne 4-5-1 (53 RF, 63 RA). Seven earlier player-stat batches remain unchanged, with batting R=55 and pitching R=19. The two missing player boxes are not reconstructed from ladder run totals. G appearances reflect supplied batches, and two SB source columns separate sacrifice bunts from steals.")
para("Before sharing with Melbourne: recheck any newly played games, obtain Malvern missing individual-game boxes, confirm recent lineups, pitcher availability and verified handedness, and then re-evaluate sample qualifications and scouting reads without inventing missing performance.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)
lines=["MELBOURNE vs MALVERN | PRELIMINARY | 24 NOV 2026",
       "Ladder as supplied Nov 18: Malvern 2nd 8-1-0 (70 RF/23 RA/+47); Melbourne 8th 4-5-1 (53 RF/63 RA/-10). Reconfirm before sharing.",
       "Seven Malvern GameDay batches; two of nine official game player boxes missing; batting 55 R, pitching 19 R in seven supplied games.",
       "BATTING"," | ".join(batcols)]
for r in batrows: lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines+=["","PITCHING"," | ".join(pitcols)]
for r in pitplayers+[pitteam]: lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines+=["","COACHING & LINEUP USAGE"]+notes+["","HIGHER-LEVEL EXPERIENCE","Jarryd Dale, Ryan Dale, Ulrich Bojarski (details + sources in PDF); Chris Burke and Tyler Luther-Wilson additional verified involvement.","","DATA QUALITY","Two games lack Malvern player data among nine official. November 18 standings updated; recheck any new results before publication."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
