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
para("<b>Data scope:</b> Eight distinct Malvern player batches for nine official games. The previously supplied 8–3 win over Sunshine is already batch 7 and was not counted twice. Newly incorporated November 17 loss 0–4 vs Newport: five singles, no runs and 5.0 identified pitching IP (4 ER). The eight supplied games account for 55 Malvern batting runs and 23 opposing runs, while the official nine-game ladder lists 70–23; the missing prior game represents a 15-run offense gap, but its score/opponent and player statistics remain unverified.")
heading("TEAM TENDENCIES & MATCHUP")
para("Malvern: 7.78 runs scored and 2.56 allowed per official game; Melbourne 5.30 scored and 6.30 allowed through ten. Malvern are 2nd (+47) and Melbourne 8th (-10). Eight available Malvern batting games yield 87 hits, seven homers, .355 AVG, .412 OBP, .506 SLG and .918 OPS; the missing ninth game prevents a certified full-season line.")
para("<b>Offensive read:</b> Jarryd Dale leads qualified hitters at .588 AVG and 1.564 OPS over 22 recorded PA; Tyler Luther-Wilson has 2 HR and 1.392 OPS in 29 PA; Hudson Priamo has 11 H, .379 AVG and .886 OPS in 32 PA. Brady Whalen and Ryan Picollo each had two singles in the 0–4 Newport loss but remain limited samples (8 PA each). Malvern managed only five singles and no runs against Newport, after its earlier 8–3 win vs Sunshine. Ulrich Bojarski has professional-level credentials beyond his 14-PA sample; do not over-weight the small-sample AVG.")
para("<b>Pitching read:</b> In the 0–4 Newport loss Zaid Elias Cummins Flynn allowed 8 H and 4 ER in 3.1 IP, 5 SO and 1 BB; Cameron Gibbens logged 1.2 scoreless IP with 3 SO. Zaid now has 17.1 IP, 25 SO, 3.12 ERA and 1.33 WHIP, classified CAUTION after the latest outing. Across the eight verified games, Malvern has 15 ER in 63.0 recorded IP (2.14 ERA) and 90 SO (12.86 K/9). Matthew Beattie has 10.0 IP/0 ER, James Squire 11.2 IP/3 ER, and Mitchell Kennedy 17.0 IP/5 ER. One earlier game is unavailable; do not infer full rotation coverage or pitcher rest.")
heading("BATTING | EIGHT SUPPLIED GAME BATCHES (OF NINE OFFICIAL)")
bat=source["batting"]
batplayers=sort_batters_by_ops(bat)
batteam=next(x for x in bat if x.get("Team Total"))
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
batrows=batplayers+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* Batting AVG qualification: 18 PA (2 per 9 official team games); only AVG carries qualification *. OBP=(H+BB+HBP)/(AB+BB+HBP+SF), ISO=SLG−AVG; figures use eight readable games and cannot represent the missing ninth. THREAT (red), CAUTION (yellow), ATTACK (green), LIMITED (gray), with existing approved scouting overrides preserved. Unverified handedness is blank.")
heading("PITCHING | IDENTIFIED APPEARANCES")
pit=source["pitching"]
pitplayers=sorted([x for x in pit if not x.get("Team Total")],key=lambda x:-(int(x["IP"].split(".")[0])*3+int(x["IP"].split(".")[1])))
pitteam=next(x for x in pit if x.get("Team Total"))
pitcols=["Player","Throws","IP","H","R","ER","BB","HBP","SO","ERA","WHIP","K/9","BB/9","Scouting Read"]
table(pitcols,pitplayers+[pitteam],[125,35,35]+[35]*6+[42]*4+[85])
para("* ERA qualification: 9 outs (3.0 IP), one per nine official team games; only ERA carries qualification *. IP is baseball innings and outs, not decimals. STRONG (red), CAUTION (yellow), ATTACK (green), LIMITED (gray); Zaid Flynn moved to CAUTION after the Newport loss. Team pitching totals cover eight batches (63.0 IP), not the full nine official games.")
heading("COACHING & LINEUP USAGE")
notes=[
"1. The latest Newport loss saw five singles and no runs: Brady Whalen and Ryan Picollo had two hits each, and James Squire one. Only Brady and Picollo remain small-sample hitters; do not overreact to one five-inning scoring ledger.",
"2. Jarryd Dale (1.564 OPS, 22 PA) and Tyler Luther-Wilson (two HR, 1.392 OPS, 29 PA) remain top power/on-base threats in the available games; Hudson Priamo (11 H in 29 AB) adds contact. Their actual order and defensive assignments require current lineups.",
"3. Zaid Elias Cummins Flynn surrendered 8 H/4 ER over 3.1 IP vs Newport, though his cumulative 25 SO in 17.1 IP indicate strikeout ability. Do not assume a fixed starter or current availability; scout count management and recent rest.",
"4. Malvern's recorded staff has 90 SO in 63.0 IP (12.86 K/9), so emphasize two-strike decisions and controlled baserunner advancement after Melbourne's own 0-0 Moorabbin draw.",
"5. Eight supplied Malvern batting games show 12 SB; monitor running game without extrapolating attempts into the one missing match. The earlier 8-3 win vs Sunshine was already counted and must not be added again.",
"6. Malvern's official 70-23 ladder and eight-batch 55-23 player runs differ by 15 Malvern runs. Obtain the missing earlier player box before calling the report fully season-complete; recheck any new standings before Nov 24."
]
for n in notes: para(n)
heading("HIGHER-LEVEL EXPERIENCE / VERIFICATION")
para("<b>Jarryd Dale (R/R):</b> Melbourne Aces ABL, San Diego Padres minors through Triple-A, Orix Buffaloes Japanese farm system, KIA Tigers KBO in 2026, Team Australia WBC. Source: Baseball Australia and MLB/MiLB player profiles (baseball.com.au/news/dale-kbo/).")
para("<b>Ryan Dale (R/R):</b> Nine ABL seasons with Melbourne Aces as of 2020-21 and Kansas City Royals organization (rookie leagues), plus Dutch Hoofdklasse. Source: Melbourne Aces 2020-21 media guide (assets.melbourneaces.com.au, V6 guide).")
para("<b>Ulrich Bojarski (R/R):</b> Detroit Tigers system through Double-A Erie; longstanding ABL hitter and Australian WBC/Premier12 representative. Sources: Baseball Australia 2026 WBC media notes and theABL player profile.")
para("<b>Chris Burke:</b> Named on the Melbourne Aces 2022 ABL roster, with Malvern local affiliation in earlier Aces media notes. <b>Tyler Luther-Wilson:</b> Experienced Geelong VSBL Division 1 catcher with U.S. high school baseball; ABL/MiLB level not confirmed. <b>Brady Whalen:</b> Name matches a minor-league profile, but Malvern identity is unverified; no professional affiliation asserted.")
heading("DATA QUALITY & NEXT UPDATE")
para("Official November 18 ladder: Malvern 8-1-0, 70 RF / 23 RA (+47), and Melbourne 4-5-1, 53 RF / 63 RA (-10). Eight distinct Malvern player batches were logged: the earlier 8-3 win vs Sunshine was already batch 7; November 17 0-4 loss vs Newport newly added once. Verified player rows show 55 batting runs and 23 runs allowed; the missing earlier game leaves a 15-run discrepancy against official RF. Do not assign runs/hits to that game without its box score. Unknown handedness blank and the two source SB columns kept separate (bunts vs steals).")
para("Before sharing with Melbourne: obtain the one missing Malvern player game (15 official team runs not represented), verify newest lineup and pitching availability after the Newport game, and recheck official standings if additional games are played. Sunshine has three missing recent individual game boxes; its 8-2 win at Upwey on November 17 is already reflected in the official 6-3 ladder.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)
lines=["MELBOURNE vs MALVERN | PRELIMINARY | 24 NOV 2026",
       "Ladder as supplied Nov 18: Malvern 2nd 8-1-0 (70 RF/23 RA/+47); Melbourne 8th 4-5-1 (53 RF/63 RA/-10). Reconfirm before sharing.",
       "Eight distinct Malvern GameDay batches (including Nov 17 0-4 Newport); earlier 8-3 Sunshine was already batch 7; one of nine official player games still missing. Eight-game batting 55 R vs 70 official.",
       "BATTING"," | ".join(batcols)]
for r in batrows: lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines+=["","PITCHING"," | ".join(pitcols)]
for r in pitplayers+[pitteam]: lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines+=["","COACHING & LINEUP USAGE"]+notes+["","HIGHER-LEVEL EXPERIENCE","Jarryd Dale, Ryan Dale, Ulrich Bojarski (details + sources in PDF); Chris Burke and Tyler Luther-Wilson additional verified involvement.","","DATA QUALITY","Eight of nine official Malvern player games imported; 0-4 loss to Newport added once, 8-3 win over Sunshine already in previous batch 7. Fifteen official runs are not represented without the one missing earlier box score; totals are incomplete."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
