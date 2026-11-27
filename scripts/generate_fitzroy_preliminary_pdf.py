#!/usr/bin/env python3
"""Publish approved preliminary Werribee report using the established VSBL advance-scouting layout."""
import json
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import landscape, A4
from advance_report_sort import apply_advance_batting_pa_cutoff, sort_batters_by_ops, sort_pitchers_by_era_qualification

ROOT=Path(__file__).resolve().parent.parent
source=json.loads((ROOT/"data/fitzroy_preliminary_dec01_2026.json").read_text(encoding="utf-8"))
stem="Melbourne_vs_Fitzroy_Advance_Scouting_Preliminary_Dec01_2026"
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
      ("ROWBACKGROUNDS",(0,1),(-1,-2 if records[-1].get("Team Total") else -1),[colors.white,colors.HexColor("#edf3f7")]),
      ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
      ("BOTTOMPADDING",(0,0),(-1,-1),4),
      ("TOPPADDING",(0,0),(-1,-1),4)]
    if records[-1].get("Team Total"):
        style.extend([("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#dbe7ee")),
                      ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold")])
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




heading("MELBOURNE vs FITZROY | ADVANCE SCOUTING")
para("<b>Tuesday 1 December 2026 | Melbourne HOME | Surrey Park Arthur Field | PRELIMINARY</b>")
para("<b>Official November 24 ladder snapshot:</b> Fitzroy 12th (4-7-0, 11 official, 48 RF, 62 RA, -14 RD). Melbourne 9th (5-6-1, 12 official, 67 RF, 89 RA, -22 RD). Top eight currently occupy playoff positions.")
para("<b>November 24 box score now supplied:</b> Fitzroy's 12-0 win was ALREADY INCLUDED in the official eleven-game 4-7-0 record and 48/62 run totals. Its player lines now add twelve runs, thirteen hits (five doubles), and seven scoreless pitching innings ONCE to the batting/pitching source tables. November 28 fixture and player rows are pending; no future results inferred.")
para("<b>Sample reconciliation:</b> Eleven supplied player batches now account for 49 Fitzroy batting runs versus 48 official RF (+1 historical inconsistency). Pitcher source rows total 60 R allowed versus 62 official RA (-2). The new November 24 game itself reconciles to 12 runs scored and zero allowed; preserve earlier source discrepancies without manufacturing corrections.")
heading("TEAM TENDENCIES & MATCHUP")
para("Fitzroy scores 4.36 runs and allows 5.64 per official game. The supplied 16-team ladder has a pooled run environment of roughly 5.68 per team-game. Fitzroy's offense is BELOW AVERAGE and its overall run prevention is around AVERAGE; its leading individual pitchers are substantially stronger than the overall position might suggest.")
para("<b>Batting in eleven supplied boxes:</b> 397 PA, 339 AB, 92 hits, 19 doubles, zero home runs, 36 walks, 70 strikeouts and 10 recorded stolen bases. Sample AVG .271, estimated OBP .366, SLG .327, OPS .694, ISO .056 and BB% 9.1%. The new game had 13 hits and 12 runs; previous source-component inconsistencies remain flagged.")
para("<b>Pitching in eleven supplied boxes:</b> 83.1 IP, 88 H, 24 BB, 77 SO and 46 ER. Recalculated sample ERA 4.97, WHIP 1.34, K/9 8.32, BB/9 2.59. Kodai Hamaya added 4.0 scoreless IP with 5 SO; Billy Findlay added 3.0 scoreless IP with 4 SO. Past team-run reconciliation differences remain unresolved.")
para("<b>Primary matchup priority:</b> Former NPB pitchers Kodai Hamaya (LHP) and Kazutomo Iguchi (RHP) have verified high-level experience. Hamaya now shows 22.0 IP, 35 SO and 2 ER after 4.0 scoreless November 24 innings. Iguchi's 1-for-1 batting appearance is his first supplied offensive sample, not a verified recurring lineup role.")
heading("BATTING | 11 SUPPLIED GAME BATCHES / 11 OFFICIAL / OPS - HIGH TO LOW")
bat=source["batting"]
batteam=next(r for r in bat if r.get("Team Total"))
# All hitters including LIMITED are ranked in one numeric OPS-high-to-low table.
batplayers=sorted((r for r in bat if not r.get("Team Total")),key=lambda r:(-float(str(r.get("OPS","0")).replace("*","") or 0),str(r.get("Player","")).casefold()))
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
batrows=batplayers+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* Batting qualification: 10 or more PA. All qualified and LIMITED batters are shown together in one OPS-high-to-low order; TEAM TOTAL remains last. AVG alone carries a qualification asterisk. Tom Dicker now reaches 10 PA and is THREAT. New one-PA batter Kazutomo Iguchi remains LIMITED even though his initial OPS is high. THREAT red, CAUTION yellow, ATTACK green, LIMITED gray. Unknown batting handedness remains blank.")
heading("PITCHING | IDENTIFIED APPEARANCES")
pit=source["pitching"]
pitteam=next(r for r in pit if r.get("Team Total"))
pitqualified,pitnonqualified=sort_pitchers_by_era_qualification(pit,min_outs=11)
pitcols=["Player","Throws","IP","H","R","ER","BB","HBP","SO","ERA","WHIP","K/9","BB/9","Scouting Read"]
para("<b>QUALIFIED PITCHERS | ERA</b>")
table(pitcols,pitqualified+([pitteam] if not pitnonqualified else []),[125,35,35]+[35]*6+[42]*4+[85])
if pitnonqualified:
    para("<b>NON-QUALIFIED PITCHERS | ERA</b>")
    table(pitcols,pitnonqualified+[pitteam],[125,35,35]+[35]*6+[42]*4+[85])
para("* Pitching qualification: at least 11 recorded outs (3.2 IP), one out per eleven official team games. Qualified and non-qualified pitchers remain in separate ERA low-to-high sections, and only ERA receives the asterisk. New game adds 7.0 scoreless IP (Hamaya 4.0, Findlay 3.0). STRONG red, CAUTION yellow, ATTACK green, LIMITED gray; unknown throws blank.")
para("Brock Pawley has an appearance with zero recorded pitching outs, one earned run and one hit. Its zero-denominator ERA and WHIP are intentionally blank. Team total AVERAGE is evaluated against the official league-wide run environment, not the strongest individual pitchers.")
heading("LINEUP & COACHING USAGE")
notes=[
"1. Daniel Huryn and Sodai Shimizu have now appeared in eleven supplied batting batches each; Billy Findlay and Mitchell Legge in ten, while Zachary Breen appears in nine. These are player appearances within supplied boxes, not a confirmed December 1 lineup order.",
"2. Kodai Hamaya had two doubles at the plate and 4.0 IP/3 H/5 SO with no walks or runs allowed on November 24. His cumulative 22.0 IP, 35 SO and 0.82 ERA make him a clear STRONG pitching threat; verify his availability before Dec 1.",
"3. Billy Findlay supplied 3.0 scoreless innings with 4 SO and one walk, bringing him to 7.2 IP. Kazutomo Iguchi remains a high-experience right-handed pitching STRONG but made only a one-PA batting appearance in the new supplied game.",
"4. Tom Dicker's latest double and walk lift him to ten PA, qualifying his batting AVG and THREAT scouting read on this sample. The one-PA, 1-for-1 Kazutomo Iguchi batting line remains LIMITED despite an inflated small-sample OPS.",
"5. The eleven supplied games feature 19 doubles, no home runs, 36 BB, 16 HBP and 10 documented steals. Emphasize preventing free bases and hard contact while confirming actual running and lineup tendencies with video.",
"6. Former NPB pitchers Hamaya and Iguchi have high-level professional experience, but team-game box scores cannot confirm who starts December 1. Check current pitching availability and actual usage before the matchup.",
"7. Source player totals after adding November 24 are 49 batting runs versus 48 official RF (+1), and 60 pitching runs allowed versus 62 official RA (-2). The new 12-0 box itself reconciles; earlier one-run and two-run source mismatches remain open."
]
for n in notes: para(n)
heading("HIGHER-LEVEL PLAYING EXPERIENCE | VERIFIED SOURCES")
para("<b>Kodai Hamaya (LHP):</b> Former Rakuten Eagles and Yokohama DeNA BayStars NPB pitcher; also Canberra Cavalry (ABL), Melbourne Aces and Baseball United experience. Source: https://www.kodaihamaya.com/en and https://melbourneaces.com.au/news/. Only throwing hand L has been verified; bats unknown.")
para("<b>Kazutomo Iguchi (RHP):</b> Former Hokkaido Nippon-Ham Fighters and Orix Buffaloes NPB pitcher; member of the 2016 Japan Series championship team; subsequently active in international professional baseball and Melbourne Aces. Source: https://npb.jp/bis/eng/players/31335132.html and https://melbourneaces.com.au/news/. Verified right-hand throw.")
para("No additional Fitzroy player is labeled as a former professional or national-team player unless source identity and playing level can be specifically matched.")
heading("DATA QUALITY & REQUIRED NEXT UPDATE")
para("Source: eleven user-provided GameDay player-stat batches, now including the 12-0 November 24 shutout, plus the separately confirmed official November 24 ladder snapshot. The Nov24 win was already in official 11-game standings and is not double-counted. November 28 game not yet played as of the latest source submission and has no player rows.")
para("Batters now have 49 summed runs against official RF 48 (+1), while pitchers have 60 total source runs allowed compared with official RA 62 (-2). This discrepancy predates the November 24 box and is explicitly unreconciled. Historical PA-component errors remain flagged. Confirm the next game box and pitcher availability before a final coaching release.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)
lines=["MELBOURNE vs FITZROY | PRELIMINARY | 01 DEC 2026",
"Fitzroy 12th 4-7-0; 11 official, 48 RF/62 RA/-14. Melbourne 9th 5-6-1; 12 official 67 RF/89 RA/-22.",
"Eleven supplied Fitzroy player-stat batches; Nov24 12-0 newly added to player stats but already in official 11-game ladder. Nov28 pending.",
"","BATTING | 11 SUPPLIED GAME BATCHES / 11 OFFICIAL / OPS - HIGH TO LOW"," | ".join(batcols)]
for r in batrows:lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines += ["","PITCHING","QUALIFIED PITCHERS | ERA"," | ".join(pitcols)]
for r in pitqualified:lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines += ["","NON-QUALIFIED PITCHERS | ERA"," | ".join(pitcols)]
for r in pitnonqualified+[pitteam]:lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines += ["","LINEUP & COACHING USAGE"]+notes+["","EXPERIENCE","Kodai Hamaya former NPB / ABL LHP; Kazutomo Iguchi former NPB / 2016 Japan Series champion RHP. See PDF sources.","","DATA QUALITY","Nov24 12-0 player game added once; sample batting R49 vs official RF48 and pitching R60 vs official RA62; historical scoring/PA issues unresolved. Nov28 pending."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
