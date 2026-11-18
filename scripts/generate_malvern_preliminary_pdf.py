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
para("<b>Data scope:</b> NINE GameDay player boxes for Malvern’s NINE official games. New November 7 Werribee 15–5 win contributes 21 H, seven HR and 15 R; independently corroborated in Baseball Victoria’s VSBL Week 6 Wrap Up. Earlier Sunshine 8–3 is already batch 7 and Newport 0–4 remains batch 8; Werribee is batch 9 with no double-count. The nine supplied batting boxes now total 70 runs, agreeing with official RF 70. Pitcher run fields total 28, exceeding official RA 23 by five; preserve the discrepancy for review rather than changing original game stats.")
heading("TEAM TENDENCIES & MATCHUP")
para("Malvern: official 2nd, 8–1–0, 70 RF, 23 RA, +47 (9 games). Melbourne 8th, 4–5–1, 53 RF, 63 RA, −10 (10 games). Malvern now has all nine batting boxes: 108 H, 14 HR, .382 AVG, .434 OBP, .604 SLG, 1.038 OPS and .223 ISO. The nine pitching boxes include 70.0 IP, 19 ER, 93 SO and a 2.44 source ERA. Pitcher recorded R=28 vs official RA=23 is unresolved and must not be presented as reconciled official defense.")
para("<b>Offensive read:</b> Malvern’s November 7 15–5 win over Werribee included seven homers and 21 hits. Ryan Dale was 4-for-4 with THREE HR and six RBI; Jarryd Dale was 3-for-5 with a HR and three RBI; Ulrich Bojarski hit two HR, and Jack Hanger one. Matthew Johnston went 4-for-4. Nine-game leaders in supplied sample: Jarryd Dale .591 AVG / 1.667 OPS (27 PA); Tyler Luther-Wilson .519 / 1.448 (34 PA); Hudson Priamo .394 AVG (36 PA). Ryan Dale has four season HR and a 3.639 OPS in just nine PA (LIMITED). Ulrich Bojarski now has 19 PA, three HR and qualifies as a THREAT rather than LIMITED. Confirm lineup card before projecting precise batting order.")
para("<b>Pitching read:</b> Werribee 15–5: James Squire 3.0 IP/1 H/2 SO/1 R (0 ER), Mitchell Kennedy 4.0 IP/10 H/1 SO/4 R (4 ER). New cumulative sample: Squire 14.2 IP, Kennedy 21.0 IP, and overall 70.0 IP with 93 SO, 19 ER (2.44 ERA) and 1.33 WHIP. Zaid Elias Cummins Flynn remains user-confirmed STRONG: 17.1 IP, 25 SO, 3.12 ERA and 12.98 K/9, despite allowing 4 ER in 3.1 IP versus Newport. The sum of pitcher R is 28 whereas official nine-game ladder RA is 23; do not infer an official team pitching reconciliation without investigating older source rows.")
heading("BATTING | NINE SUPPLIED GAME BATCHES / NINE OFFICIAL")
bat=source["batting"]
batplayers=sort_batters_by_ops(bat)
batteam=next(x for x in bat if x.get("Team Total"))
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
batrows=batplayers+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* Batting AVG qualification: 18 PA (2 PA per 9 team games), with * only beside AVG. OBP=(H+BB+HBP)/(AB+BB+HBP+SF); OPS=OBP+SLG; ISO=SLG−AVG. Nine player box-score samples yield 70 batting runs, matching official RF. Ryan Dale 9 PA remains a LIMITED sample despite four HR; Ulrich Bojarski 19 PA is now a qualified THREAT. Unknown hands stay blank. Matthew Johnston November 7 row has 4 PA, 4 AB and a sacrifice bunt, a source accounting conflict flagged without altering supplied data.")
heading("PITCHING | IDENTIFIED APPEARANCES")
pit=source["pitching"]
pitplayers=sorted([x for x in pit if not x.get("Team Total")],key=lambda x:-(int(x["IP"].split(".")[0])*3+int(x["IP"].split(".")[1])))
pitteam=next(x for x in pit if x.get("Team Total"))
pitcols=["Player","Throws","IP","H","R","ER","BB","HBP","SO","ERA","WHIP","K/9","BB/9","Scouting Read"]
table(pitcols,pitplayers+[pitteam],[125,35,35]+[35]*6+[42]*4+[85])
para("* ERA qualification: 9 recorded outs (3.0 IP), one per nine team games. Only ERA has qualification *. IP is baseball innings plus outs. Pitcher source nine-game totals: 70.0 IP, 93 SO, 19 ER, 28 R; official ladder records 23 RA, an unresolved five-run conflict. Scouting classifications STRONG (red), CAUTION (yellow), ATTACK (green), LIMITED (gray). Zaid Flynn is STRONG per user-approved override.")
heading("COACHING & LINEUP USAGE")
notes=[
"1. November 7 vs Werribee featured a seven-homer Malvern attack with 21 hits: Ryan Dale 3 HR/6 RBI, Jarryd Dale 1 HR/3 RBI, Ulrich Bojarski 2 HR/3 RBI and Jack Hanger 1 HR. The next supplied Nov 17 game was a five-single shutout loss to Newport; avoid overreacting to either one-game extreme.",
"2. Jarryd Dale (.591 AVG, 1.667 OPS, 27 PA) and Tyler Luther-Wilson (.519, 1.448, 34 PA) are priority threats. Ulrich Bojarski now qualifies at 19 PA with three HR and THREAT classification. Ryan Dale has four HR in only nine PA; treat as major power consideration but LIMITED sample.",
"3. Zaid Elias Cummins Flynn remains STRONG per coach-selected assessment (17.1 IP, 25 SO, 3.12 ERA, 12.98 K/9) despite one difficult Newport appearance. Mitchell Kennedy had 4 ER in 4.0 IP vs Werribee. Confirm rest and current roles before guessing a starting pitcher.",
"4. Nine-game pitching sample totals 93 SO in 70.0 IP (11.96 K/9), with 19 ER and 2.44 source ERA. The player-game pitcher R total of 28 conflicts with the official ladder RA 23; investigate the prior pitching rows rather than altering the official record.",
"5. Malvern logged 13 SB in nine supplied games; advance defensive preparation for both qualified hitters and extraordinary small-sample HR threats. Verify recent lineup placement and the running game on new video before issuing individual shifts.",
"6. Nine distinct Malvern player boxes are now supplied, and all 70 offensive runs reconcile. Outstanding work is to investigate a five-run pitching ledger discrepancy and a Matthew Johnston sacrifice-bunt/PA inconsistency. Sunshine still lacks three of nine individual games."
]
for n in notes: para(n)
heading("HIGHER-LEVEL EXPERIENCE / VERIFICATION")
para("<b>Jarryd Dale (R/R):</b> Melbourne Aces ABL, San Diego Padres minors through Triple-A, Orix Buffaloes Japanese farm system, KIA Tigers KBO in 2026, Team Australia WBC. Source: Baseball Australia and MLB/MiLB player profiles (baseball.com.au/news/dale-kbo/).")
para("<b>Ryan Dale (R/R):</b> Nine ABL seasons with Melbourne Aces as of 2020-21 and Kansas City Royals organization (rookie leagues), plus Dutch Hoofdklasse. Source: Melbourne Aces 2020-21 media guide (assets.melbourneaces.com.au, V6 guide).")
para("<b>Ulrich Bojarski (R/R):</b> Detroit Tigers system through Double-A Erie; longstanding ABL hitter and Australian WBC/Premier12 representative. Sources: Baseball Australia 2026 WBC media notes and theABL player profile.")
para("<b>Chris Burke:</b> Named on the Melbourne Aces 2022 ABL roster, with Malvern local affiliation in earlier Aces media notes. <b>Tyler Luther-Wilson:</b> Experienced Geelong VSBL Division 1 catcher with U.S. high school baseball; ABL/MiLB level not confirmed. <b>Brady Whalen:</b> Name matches a minor-league profile, but Malvern identity is unverified; no professional affiliation asserted.")
heading("DATA QUALITY & NEXT UPDATE")
para("Official November 18 ladder: Malvern 8–1–0 (70 RF, 23 RA), Melbourne 4–5–1 (53 RF, 63 RA). Nine GameDay batting boxes now add to 70 Malvern runs; all nine games accounted for, including 8–3 Sunshine (saved batch 7), 0–4 Newport (batch 8) and 15–5 Werribee Nov 7 (new batch 9). Source pitcher-run rows total 28, five more than official RA=23. The Werribee individual pitching lines themselves match the independent 15–5 score. Matthew Johnston’s Werribee 4 PA/4 AB/1 SAC remains an inconsistent source field; no replacement invented. Two batting SB fields are distinguished (sacrifice bunt vs stolen base).")
para("Before sharing with Melbourne: batting games are complete by count, but verify the unresolved five-run difference between summed pitcher game rows and official RA. Cross-check previous Malvern pitching results and the Matthew Johnston PA/sacrifice-bunt discrepancy against the GameDay record. Reconfirm the most recent lineups, pitcher availability, and official standings near Nov 24. Sunshine still lacks three recent individual player boxes, including 8–2 Upwey Nov 17.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)
lines=["MELBOURNE vs MALVERN | PRELIMINARY | 24 NOV 2026",
       "Ladder as supplied Nov 18: Malvern 2nd 8-1-0 (70 RF/23 RA/+47); Melbourne 8th 4-5-1 (53 RF/63 RA/-10). Reconfirm before sharing.",
       "Nine Malvern GameDay player boxes / nine official games, including 15-5 Werribee on Nov 7 (21 H, 7 HR). Batting R=70 matches official RF. Pitching R=28 differs from official RA=23 by five; audit required.",
       "BATTING"," | ".join(batcols)]
for r in batrows: lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines+=["","PITCHING"," | ".join(pitcols)]
for r in pitplayers+[pitteam]: lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines+=["","COACHING & LINEUP USAGE"]+notes+["","HIGHER-LEVEL EXPERIENCE","Jarryd Dale, Ryan Dale, Ulrich Bojarski (details + sources in PDF); Chris Burke and Tyler Luther-Wilson additional verified involvement.","","DATA QUALITY","All nine game batting boxes are present and total 70 runs, matching official RF. Nine pitcher boxes total 28 R versus 23 official RA; five-run reconciliation pending. Nov 7 Matthew Johnston 4 PA/4 AB/1 SAC source conflict retained. Zaid Flynn STRONG (user approved)."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
