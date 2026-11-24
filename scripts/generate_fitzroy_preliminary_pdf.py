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
para("<b>Pending:</b> The 12-0 Fitzroy victory on November 24 IS ALREADY INCLUDED in the official 4-7-0 team record and 48/62 ledger, but its player box score is not included in these tables. The November 28 result and player box are not yet verified. Never double count either.")
para("<b>Sample reconciliation:</b> Ten supplied player-stat game batches total 37 batting runs against an expected 36 before the November 24 12-0 win (+1 mismatch), while the individual pitchers account for 60 runs against vs 62 in the official ladder (-2 mismatch). Preserve both the official ladder and unreconciled player totals rather than inventing corrections.")
heading("TEAM TENDENCIES & MATCHUP")
para("Fitzroy scores 4.36 runs and allows 5.64 per official game. The supplied 16-team ladder has a pooled run environment of roughly 5.68 per team-game. Fitzroy's offense is BELOW AVERAGE and its overall run prevention is around AVERAGE; its leading individual pitchers are substantially stronger than the overall position might suggest.")
para("<b>Batting in ten supplied boxes:</b> 360 PA, 309 AB, 79 H, 14 doubles, 0 HR, 32 BB, 68 SO, 10 recorded SB; source AVG .256, estimated OBP .354, SLG .301, OPS .655, ISO .045, BB% 8.9%. No November 24 or November 28 player lines are added.")
para("<b>Pitching in ten supplied boxes:</b> 76.1 IP, 85 H, 23 BB, 68 SO, 46 ER. Reconstructed 5.42 ERA, 1.41 WHIP, 8.02 K/9, 2.71 BB/9. Player totals have small unresolved differences from the official team ledger.")
para("<b>Primary matchup priority:</b> Former NPB pitchers Kodai Hamaya (left-handed) and Kazutomo Iguchi (right-handed) have high-level professional experience, recent Melbourne Aces associations, and dominant strikeout records in the supplied VSBL sample.")
heading("BATTING | 10 SUPPLIED GAME BATCHES / 11 OFFICIAL / OPS - HIGH TO LOW")
bat=source["batting"]
batteam=next(r for r in bat if r.get("Team Total"))
batplayers=sort_batters_by_ops(bat)
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
batrows=batplayers+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* Batting qualification: 10 or more plate appearances. Qualified hitters first, OPS highest to lowest, then LIMITED (<10 PA) hitters by OPS; TEAM TOTAL last. Only AVG receives a qualification asterisk. Batting reads: THREAT red, CAUTION yellow, ATTACK green, LIMITED gray. All unknown handedness remains blank with background matching the player row.")
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
para("* Pitching qualification: at least 11 recorded outs (3.2 IP), one out per official team game. Qualified and LIMITED pitchers are each ordered by ERA low to high. Only ERA receives a qualification asterisk. Pitching reads: STRONG red, CAUTION yellow, ATTACK green, LIMITED gray. Unknown throwing hands remain blank.")
para("Brock Pawley has an appearance with zero recorded pitching outs, one earned run and one hit. Its zero-denominator ERA and WHIP are intentionally blank. Team total AVERAGE is evaluated against the official league-wide run environment, not the strongest individual pitchers.")
heading("LINEUP & COACHING USAGE")
notes=[
"1. Daniel Huryn and Sodai Shimizu each appear in all ten supplied batting batches; Billy Findlay, Kalan Ellis and Mitchell Legge in nine; Cameron Deeble and Zachary Breen in eight. These are playing-frequency trends, not a verified upcoming batting order.",
"2. Among qualified batters Brock Pawley (.926 OPS, 16 PA) is THREAT. Sodai Shimizu (.878 OPS, 44 PA), Daniel Huryn (.860 OPS, 36 PA) and Cameron Deeble (.804 OPS, 36 PA and 7 RBI) merit CAUTION. Tom Dicker (1.500 OPS) has only 7 PA and correctly remains LIMITED.",
"3. The ten supplied boxes have 14 doubles, no recorded HR, 32 walks, 15 HBP and 10 stolen bases. Prepare for pressure from contact, runners in motion and advancement; unknown per-game strategies should not be asserted without video.",
"4. Hamaya (18.0 IP, 30 SO, 2 ER) and Iguchi (14.0 IP, 21 SO, 1 ER) account for 51 of the staff's 68 available strikeouts. Their high-level careers and efficiency require a disciplined two-strike approach; pitch shape and velocity are NOT known from this data.",
"5. The remaining supplied pitcher sample has uneven run prevention. Bucello (17.2 IP, 16 ER), Holmes (9.1 IP, 10 ER), and Nakaza (7.1 IP, 6 ER) are possible attack opportunities depending on actual availability and sequence.",
"6. Hamaya and Iguchi are associated with Melbourne Aces, but availability for December 1 must not be inferred. Update probable starter, recent pitch counts and bullpen use after Nov 24 and Nov 28 boxes are published.",
"7. Four supplied batter lines have PA breakdown discrepancies and supplied batting R differs by one from the inferred official pre-Nov24 total. Avoid false precision and recheck the most recent official scorer posts."
]
for n in notes: para(n)
heading("HIGHER-LEVEL PLAYING EXPERIENCE | VERIFIED SOURCES")
para("<b>Kodai Hamaya (LHP):</b> Former Rakuten Eagles and Yokohama DeNA BayStars NPB pitcher; also Canberra Cavalry (ABL), Melbourne Aces and Baseball United experience. Source: https://www.kodaihamaya.com/en and https://melbourneaces.com.au/news/. Only throwing hand L has been verified; bats unknown.")
para("<b>Kazutomo Iguchi (RHP):</b> Former Hokkaido Nippon-Ham Fighters and Orix Buffaloes NPB pitcher; member of the 2016 Japan Series championship team; subsequently active in international professional baseball and Melbourne Aces. Source: https://npb.jp/bis/eng/players/31335132.html and https://melbourneaces.com.au/news/. Verified right-hand throw.")
para("No additional Fitzroy player is labeled as a former professional or national-team player unless source identity and playing level can be specifically matched.")
heading("DATA QUALITY & REQUIRED NEXT UPDATE")
para("Source: ten user-pasted GameDay-style player-stat batches; separate official November 24 VSBL ladder snapshot. Fitzroy's 12-0 November 24 victory is official in the 11-game ladder but not in the ten supplied individual game-stat batches. November 28 result and player statistics are also pending.")
para("Batters have 37 aggregate source runs compared with an implied 36 through the first ten official games, while pitchers have 60 aggregate runs allowed versus official 62 across eleven games, including the November 24 shutout. Component mismatches are flagged rather than silently reconciled. Confirm source PA accounting and updated scoring, and refresh playing experience, lineup roles, sample qualification and scouting reads when missing boxes become available.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)
lines=["MELBOURNE vs FITZROY | PRELIMINARY | 01 DEC 2026",
"Fitzroy 12th 4-7-0; 11 official, 48 RF/62 RA/-14. Melbourne 9th 5-6-1; 12 official 67 RF/89 RA/-22.",
"Ten supplied Fitzroy player-stat batches; Nov24 12-0 already in official standings but player box missing; Nov28 result/player stats pending.",
"","BATTING | 10 SUPPLIED GAME BATCHES / 11 OFFICIAL / OPS - HIGH TO LOW"," | ".join(batcols)]
for r in batrows:lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines += ["","PITCHING","QUALIFIED PITCHERS | ERA"," | ".join(pitcols)]
for r in pitqualified:lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines += ["","NON-QUALIFIED PITCHERS | ERA"," | ".join(pitcols)]
for r in pitnonqualified+[pitteam]:lines.append(" | ".join(str(r.get(k,"") or "") for k in pitcols))
lines += ["","LINEUP & COACHING USAGE"]+notes+["","EXPERIENCE","Kodai Hamaya former NPB and ABL LHP; Kazutomo Iguchi former NPB 2016 Japan Series champion RHP. See PDF for URLs.","","DATA QUALITY","Player batting R37 vs implied pre-Nov24 R36; pitcher R60 vs official 11-game RA62. Nov24 and Nov28 individual data pending."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
