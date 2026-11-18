#!/usr/bin/env python3
"""Publish approved preliminary Sunshine report using the established VSBL advance-scouting layout."""
import json
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import landscape, A4
from advance_report_sort import sort_batters_by_ops

ROOT=Path(__file__).resolve().parent.parent
source=json.loads((ROOT/"data/sunshine_preliminary_nov21_2026.json").read_text(encoding="utf-8"))
stem="Melbourne_vs_Sunshine_Advance_Scouting_Preliminary_Nov21_2026"
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


heading("MELBOURNE vs SUNSHINE | ADVANCE SCOUTING")
para("<b>Saturday 21 November 2026 | Melbourne HOME | Surrey Park Arthur Field | PRELIMINARY</b>")
para("<b>Official ladder (November 18 screenshot):</b> Sunshine 5th, 6-3-0, 65 RF, 30 RA, +35 RD (nine games); Melbourne 8th, 4-5-1, 53 RF, 63 RA, -10 RD (ten games). Sunshine beat Upwey FTG 8-2 on Tuesday November 17 at Kings Park, but that result is ALREADY included in this ladder. Its player box and the two preceding Sunshine player games remain unavailable.")
para("<b>Sample rules:</b> Six readable player-stat batches out of nine official Sunshine games; the most recent three player boxes are missing or unusable, including November 17 8-2 at Upwey and November 10 vs Essendon. Seven copied batches were received earlier, but one had impossible batting decomposition and was excluded. Six valid samples: 43 batting runs, 23 allowed, 46.0 pitching IP. Do not count the eight Upwey runs twice or invent player lines. Unknown handedness blank.")
heading("TEAM TENDENCIES & MATCHUP")
para("Sunshine scored 65 and allowed 30 in nine official games (7.22 RF, 3.33 RA per game; +35 RD). Melbourne scored 53 and allowed 63 in ten (5.30 RF, 6.30 RA). The six usable Sunshine player games alone have 59 H, .307 AVG, .403 estimated OBP, .438 SLG, .840 OPS and two HR. No cumulative player totals have been guessed for the three missing games.")
para("<b>Offensive approach:</b> Jamie Young is the best established two-way threat in the usable sample, with 12 H, 3 doubles, 1 HR and 9 RBI. Jordan Young, Darryl George and Hunter Jones have 8 H each; Jordan Young has 4 doubles, while Darryl George's hit rate is supported by 19 recorded PA. Adrian Fittock provides another recorded HR and multi-RBI games. Keep priority hitters from extending innings via free passes.")
para("<b>Pitching outlook:</b> Jamie Young (27.1 IP, 4.61 ERA, 1.21 WHIP), Jeremy Young (13.0 IP, 2.08 ERA, 16.00 K/9) and Hunter Jones (5.2 IP, 6.35 ERA) are the identified contributors. Jeremy Young's zero recorded walks and 16 K in the usable sample stand out; against Jones, force him to throw competitive strikes. Exact Saturday availability is unverified.")
heading("BATTING | SIX USABLE GAME BATCHES")
bat=source["batting"]
# All red opponent BATTING player scouting reads are THREAT, never STRONG.
# Team-total assessments and PITCHING classifications retain their existing meanings.
for batting_row in bat:
    if not batting_row.get("Team Total") and str(batting_row.get("Scouting Read", "")).upper() == "STRONG":
        batting_row["Scouting Read"] = "THREAT"
batplayers=sort_batters_by_ops(bat)
batteam=next(x for x in bat if x.get("Team Total"))
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
batrows=batplayers+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* AVG qualification uses 18 PA (2 per 9 official team games). Only AVG and ERA get qualification asterisks; historical player OBP/OPS and SB rely on readable source columns. Batting classifications: THREAT (red), CAUTION (yellow), ATTACK (green), LIMITED (gray); Jordan Young and Hunter Jones THREAT (red) per coaching override. Team total STRONG reflects available sample.")
heading("PITCHING | SIX USABLE GAME BATCHES")
pit=source["pitching"]
pitplayers=sorted([x for x in pit if not x.get("Team Total")],key=lambda x:-(int(x["IP"].split(".")[0])*3+int(x["IP"].split(".")[1])))
pitteam=next(x for x in pit if x.get("Team Total"))
pitcols=["Player","Throws","IP","H","R","ER","BB","HBP","SO","ERA","WHIP","K/9","BB/9","Scouting Read"]
table(pitcols,pitplayers+[pitteam],[125,35,35]+[35]*6+[42]*4+[85])
para("* ERA qualification uses 9 recorded outs (3.0 IP) for nine official team games. Only ERA receives a qualification asterisk; IP uses innings plus outs. Pitching classifications STRONG (red), CAUTION (yellow), ATTACK (green), LIMITED (gray). Team total reflects six usable pitching batches, not the full season.")
heading("COACHING & LINEUP USAGE")
notes=[
"1. Manage the middle order as a power/contact combination: Jamie Young's two-way contributions plus Adrian Fittock's HR and Jordan Young's doubles are demonstrated in the usable batches. Avoid unnecessary runners ahead of them.",
"2. Darryl George is an experienced professional and WBC veteran; do not rely on VSBL box-score sample alone when planning pitch selection and defense.",
"3. Prepare for Jeremy Young as a strike-throwing, swing-and-miss option (16 SO, 0 BB in 13.0 verified IP). Be ready to adjust for chase tendencies, count leverage and bullpen sequencing.",
"4. When facing Hunter Jones, take a disciplined approach: 6 walks over 5.2 recorded IP. Use pitches-per-plate-appearance and timing to test whether command issues persist.",
"5. Sunshine has allowed 30 runs through nine official games (3.33/game). Melbourne generated four singles but no runs in the November 17 Moorabbin draw: prioritize baserunner advancement, productive contact and situational hitting.",
"6. Manager Stuart Clayton described planned multi-pitcher usage early in the season. Prior to Nov 21, review Sunshine's latest lineup and pitching usage; avoid asserting a starting pitcher from an incomplete sample."
]
for n in notes: para(n)
heading("HIGHER-LEVEL EXPERIENCE / VERIFICATION")
para("<b>Darryl George:</b> Long-time Melbourne Aces professional (ABL), former Tampa Bay Rays minor-league player, and Australia 2023 World Baseball Classic representative. Melbourne Aces 2026 roster and biography: melbourneaces.com.au/news/ and /player/darryl-george-607977.")
para("<b>Jamie Young:</b> NCAA Division II Maryville, NJCAA Division I Lake Land, Melbourne Aces development roster and Australia junior representative; bats/throws R/R. Source: baseballjobsoverseas.com/players/jamie-young/ and Baseball-Reference.")
para("<b>Jeremy Young:</b> Sunshine Baseball Club historical ABL representative listing includes him with Melbourne Aces; verify current active ABL status separately. <b>Hunter Jones & Amerson Dix:</b> named as 2026 Sunshine additions/imports by Brimbank Star Weekly; specific prior levels not established.")
heading("DATA QUALITY & NEXT UPDATE")
para("Sources: user-supplied November 18 Sunshine ladder, 8-2 Upwey FTG November 17 score screenshot and previously supplied Sunshine GameDay player rows; Baseball Victoria/club media for earlier context. Six valid player batches of nine official games; latest three Sunshine boxes unavailable, with one earlier malformed submission excluded. The Nov 17 result is already in the official 6-3-0/65-30 totals and is not added to the player sample.")
para("Corrections needed before final report: obtain the November 10 Essendon box score, re-send the malformed game batch with aligned 38-column headers, verify latest starting-pitcher usage and batting/throwing handedness. Until then, do NOT equate the six-batch player aggregates with the eight-game standings, nor infer missing data as zeros.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)
lines=["MELBOURNE vs SUNSHINE | PRELIMINARY | 21 NOV 2026","Sunshine 5th: 6-3-0 65 RF 30 RA +35 (9 games) | Melbourne 8th: 4-5-1 53 RF 63 RA -10 (10 games)","Six readable Sunshine game samples; three most recent individual boxes unavailable (Nov 17 8-2 Upwey and two preceding); one copied malformed batch excluded.","","BATTING"," | ".join(batcols)]
for r in batrows: lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines+=["","PITCHING"," | ".join(pitcols)]
for r in pitplayers+[pitteam]: lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines+=["","COACHING & LINEUP USAGE"]+notes+["","DATA QUALITY","Nov 17 Sunshine 8-2 Upwey result is already in official nine-game ladder (6-3-0, 65-30). Three recent individual-game boxes remain unavailable; six validated historical player batches are the complete supplied sample."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
