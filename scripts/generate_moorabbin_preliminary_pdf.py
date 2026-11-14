#!/usr/bin/env python3
"""Publish approved preliminary Moorabbin report using the established VSBL advance-scouting layout."""
import json
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import landscape, A4

ROOT=Path(__file__).resolve().parent.parent
source=json.loads((ROOT/"data/moorabbin_preliminary_nov17_2026.json").read_text(encoding="utf-8"))
stem="Melbourne_vs_Moorabbin_Advance_Scouting_Preliminary_Nov17_2026_Final"
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

heading("MELBOURNE vs MOORABBIN | ADVANCE SCOUTING")
para("<b>Tuesday 17 November 2026 | 18:15 | A W Oliver Reserve | PRELIMINARY</b>")
para("<b>Official ladder:</b> Moorabbin 4th, 6–1–0, 57 RF, 31 RA, +26 RD (7 games); Melbourne 9th, 4–5–0, 53 RF, 63 RA, −10 RD (9 games). Moorabbin's November 14 result is a 9–3 win and is already reflected in the ladder; its individual player stats remain outstanding.")
para("<b>Data scope:</b> Six supplied game-by-game player-stat batches, now INCLUDING November 10, cover six of Moorabbin's seven official games. November 14 is included in the official record but NOT in player totals. No game is counted twice. Unknown batting/throwing hands remain blank. GameDay fractional IP values use baseball outs notation (0.33=one out; 0.66=two outs).")
heading("TEAM TENDENCIES & MATCHUP")
para("Moorabbin average 8.14 runs scored and 4.43 allowed per official game; Melbourne average 5.89 scored and 7.00 allowed. Moorabbin's +26 differential and six wins in seven games support a strong early team profile, but the win on November 14 has no published individual statistics in this edition.")
para("<b>Offensive read:</b> Jake Bertucci, Brady Jeffcoat, Nicholas Coy and Nicholas Bertucci remain key extra-base threats in the six uploaded games. In the November 10 box score, Nicholas Bertucci homered and drove in three; Jake Bertucci and Nicholas Coy drove in two each, while Diego Aragon added a two-hit game with a double. Jeffcoat has three recorded HR in the available sample. Avoid free passes before these hitters.")
para("<b>Defensive / pitching read:</b> Christopher Nielsen remains the largest identified workload (22.2 IP) and is rated STRONG. The November 10 pitching records add Liam Puncher 4.0 IP, 4 H, 2 ER, 2 BB, 6 SO and Cody Hill 1.0 IP, 2 H, 1 ER, 0 BB, 2 SO. Evaluate availability after the November 14 game, whose pitcher usage is still unknown; do not presume a starter.")
heading("BATTING | SIX PROVIDED GAME BATCHES")
bathead=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG*","OBP","SLG","OPS","ISO","BB%","SCOUTING READ"]
bat=source["batting"]
batplayers=sorted([x for x in bat if not x.get("Team Total")],key=lambda x:(-int(x["PA"]),x["Player"]))
batteam=next(x for x in bat if x.get("Team Total"))
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
batrows=batplayers+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* AVG qualification: 2 PA per official team game = 14 PA through seven games; only AVG receives an asterisk. OBP uses (H+BB+HBP)/PA as an approximation; historical SF/CI can affect exact denominators. SCOUTING READ: THREAT (red), CAUTION (yellow), ATTACK (green), LIMITED (gray). The November 14 box score is pending.")
heading("PITCHING | IDENTIFIED APPEARANCES")
pit=source["pitching"]
pitplayers=sorted([x for x in pit if not x.get("Team Total")],key=lambda x:-(int(x["IP"].split(".")[0])*3+int(x["IP"].split(".")[1])))
pitteam=next(x for x in pit if x.get("Team Total"))
pitcols=["Player","Throws","IP","H","R","ER","BB","HBP","SO","ERA","WHIP","K/9","BB/9","Scouting Read"]
table(pitcols,pitplayers+[pitteam],[125,35,35]+[35]*6+[42]*4+[85])
para("* Pitching ERA qualification: one out per official team game = 7 outs (2.1 IP) through seven games; only ERA receives an asterisk. Pitching reflects identified appearances from six games (44.0 IP); the November 14 appearance ledger is not yet available. Team R totals through November 10 match the pre-November 14 official ladder, but do not interpret the partial-team ERA as a full-season ERA.")
heading("COACHING & LINEUP USAGE")
notes=[
"1. Brady Jeffcoat remains a three-HR power threat in the available six-game batting sample. Minimize free passes ahead of him and avoid predictable hittable locations, especially with runners on.",
"2. Nicholas Bertucci homered with three RBI on November 10; Jake Bertucci and Nicholas Coy contributed two RBI each. Prioritize disciplined first-pitch plans and reliable defense against extra-base contact.",
"3. Diego Aragon collected two hits including a double and scored twice on November 10; Christopher Nielsen added two singles and a walk as a hitter. These are single-game observations, not established lineup tendencies.",
"4. Christopher Nielsen owns the largest documented pitching workload (22.2 IP), while Puncher threw 4.0 IP and Hill 1.0 IP on November 10. Check the November 14 box score for current arm usage before projecting Tuesday availability.",
"5. Moorabbin's six-game recorded offense includes seven homers and 34 walks, so emphasize strike throwing and avoiding multi-run rallies. Use selective baserunning only when pitcher/catcher execution supports it; no pop times or pickoff data are verified.",
"6. The November 14 9–3 Moorabbin win is recorded in the ladder but not these player tables. Confirm its batting order, substitutions and pitcher appearances before final defensive shifts or bullpen assignments."]
for line in notes: para(line)
heading("HIGHER-LEVEL EXPERIENCE / VERIFICATION")
para("No higher-level playing history is confirmed from the supplied box scores alone. Player names should be checked against ABL, college, representative and international rosters before adding credentials. Unverified name matches are intentionally omitted.")
heading("DATA QUALITY & NEXT UPDATE")
para("Sources: user-provided VSBL November 14 ladder screenshot, fixture and six GameDay player-stat batches (including November 10). Official team record: 7 Moorabbin games and 9 Melbourne games; individual Moorabbin data: 6 batches, Melbourne player data: 8 games. The November 14 Moorabbin player box score and Melbourne player game data are not yet supplied. Historical steals and any game entry discrepancies remain provisional. Unknown batting/pitching handedness is blank.")
para("Next refresh: incorporate Moorabbin's November 14 individual player box score when published. November 10 is already included and must not be duplicated. Recompute player and team totals, qualification marks, scouting classifications and coaching usage, without changing the seven-game ladder record unless an official correction is posted.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)

lines=["MELBOURNE vs MOORABBIN | PRELIMINARY | 17 NOV 2026",
       "Moorabbin 4th: 6-1-0, 57 RF, 31 RA, +26 (7 games); Melbourne 9th: 4-5-0, 53 RF, 63 RA, -10 (9 games)",
       "Source: six player-stat batches including November 10; November 14 player data unavailable. Handedness blank.",
       "BATTING"," | ".join(bathead)]
for r in batrows: lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines+=["","PITCHING"," | ".join(pitcols)]
for r in pitplayers+[pitteam]: lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines+=["","COACHING & LINEUP USAGE"]+notes+["","HIGHER-LEVEL EXPERIENCE / VERIFICATION","No higher-level playing history confirmed.","DATA QUALITY & NEXT UPDATE","Six player batches entered including November 10. November 14 player box score pending; official 7-game ladder current."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
