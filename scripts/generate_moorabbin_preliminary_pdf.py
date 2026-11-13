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
para("<b>Official ladder:</b> Moorabbin 5–1, 48 RF, 28 RA, +20 RD (6 games); Melbourne 4–4, 52 RF, 57 RA, −5 RD (8 games). Moorabbin November 10 victory already included in ladder; player stats for that game are pending. Both clubs have one additional game before this fixture.")
para("<b>Data scope:</b> The individual tables below aggregate the five supplied game-by-game player-stat batches, not the full six-game official season. The November 10 box score is not added twice. Bats/throws are unverified and left blank. GameDay fractional IP values are converted to outs (0.33=one out, 0.66=two outs).")
heading("TEAM TENDENCIES & MATCHUP")
para("Moorabbin average 8.0 runs scored and 4.7 allowed per official game. Melbourne average 6.5 scored and 7.1 allowed. Moorabbin have a +20 run differential and five wins in six games, indicating a strong early team profile; avoid projecting this directly into a single-game outcome.")
para("<b>Offensive read:</b> Jake Bertucci, Brady Jeffcoat, Nicholas Coy and Nicholas Bertucci have produced notable extra-base damage in the supplied sample. Jeffcoat has three HR across the five entered games; Jake Bertucci and Nicholas Coy each have a HR. Attack hitters individually rather than treating the entire lineup as uniform.")
para("<b>Defensive / pitching read:</b> Christopher Nielsen carries the largest identified workload in the sample. Evaluate his workload and availability after Moorabbin's intervening game. Recorded pitcher totals may omit appearances; no unverified rotation or handedness is assumed.")
heading("BATTING | FIVE PROVIDED GAME BATCHES")
bathead=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG*","OBP","SLG","OPS","ISO","BB%","SCOUTING READ"]
bat=source["batting"]
batplayers=sorted([x for x in bat if not x.get("Team Total")],key=lambda x:(-int(x["PA"]),x["Player"]))
batteam=next(x for x in bat if x.get("Team Total"))
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
batrows=batplayers+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* AVG qualification follows the approved preliminary report; asterisks appear only on AVG. OBP uses (H+BB+HBP)/PA as an approximation where SF and CI affect official denominators; recheck against official cumulative tables. SCOUTING READ: threat (red), caution (yellow), attack (green), limited (gray); provisional classification based on limited results.")
heading("PITCHING | IDENTIFIED APPEARANCES")
pit=source["pitching"]
pitplayers=sorted([x for x in pit if not x.get("Team Total")],key=lambda x:-(int(x["IP"].split(".")[0])*3+int(x["IP"].split(".")[1])))
pitteam=next(x for x in pit if x.get("Team Total"))
pitcols=["Player","Throws","IP","H","R","ER","BB","HBP","SO","ERA","WHIP","K/9","BB/9","Scouting Read"]
table(pitcols,pitplayers+[pitteam],[125,35,35]+[35]*6+[42]*4+[85])
para("* Pitching ERA qualification: at least one out per official team game (6 outs for six games). All pitching metrics are based only on identified appearances. Recorded pitching R/ER totals may not reconcile with the official six-game ladder. Do not interpret partial-team ERA as full-season ERA.")
heading("COACHING & LINEUP USAGE")
notes=[
"1. Prepare for Jeffcoat as a power threat; avoid predictable middle-in pitches and unnecessary free passes, especially with runners aboard.",
"2. Jake Bertucci and Nicholas Coy show extra-base impact and multiple-hit games. Prioritize clean first-pitch plans, location discipline and defensive readiness for hard contact.",
"3. Nicholas Bertucci and Euan Clarkin have appeared frequently in supplied batting orders; monitor on-base opportunities and any run-game aggressiveness.",
"4. Confirm Nielsen's latest pitch count and whether he starts or relieves in Moorabbin's next game; do not infer Tuesday availability from historical innings alone.",
"5. Use aggressive but selective baserunning when pitcher/catcher batteries show vulnerability; the available box scores alone cannot verify pop times or pickoff tendencies.",
"6. Review lineup order and substitution patterns from the final pre-match box score before issuing specific defensive shifts or bullpen matchup assignments."]
for line in notes: para(line)
heading("HIGHER-LEVEL EXPERIENCE / VERIFICATION")
para("No higher-level playing history is confirmed from the supplied box scores alone. Player names should be checked against ABL, college, representative and international rosters before adding credentials. Unverified name matches are intentionally omitted.")
heading("DATA QUALITY & NEXT UPDATE")
para("Sources: user-provided VSBL ladder screenshot, fixture screenshot and five GameDay player-stat batches. Official team record: 6 games; player samples: 5 batches. Missing November 10 player stats, one future Moorabbin game and one future Melbourne game. Some GameDay values can be incomplete or entered incorrectly; differences are flagged rather than filled with invented figures. Verified batting and pitching handedness remains unavailable.")
para("Next refresh: add the November 10 Moorabbin player box score once published, then both intervening game results and player lines. Recompute team totals, qualification asterisks, scout classifications, lineup usage and tactical priorities.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)

lines=["MELBOURNE vs MOORABBIN | PRELIMINARY | 17 NOV 2026",
       "Moorabbin 4th: 5-1-0, 48 RF, 28 RA, +20; Melbourne 8th: 4-4-0, 52 RF, 57 RA, -5",
       "Source: five player-stat batches; November 10 player data unavailable. Handedness blank.",
       "BATTING"," | ".join(bathead)]
for r in batrows: lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines+=["","PITCHING"," | ".join(pitcols)]
for r in pitplayers+[pitteam]: lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines+=["","COACHING & LINEUP USAGE"]+notes+["","HIGHER-LEVEL EXPERIENCE / VERIFICATION","No higher-level playing history confirmed.","DATA QUALITY & NEXT UPDATE","All stats provisional; November 10 player box score missing."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
