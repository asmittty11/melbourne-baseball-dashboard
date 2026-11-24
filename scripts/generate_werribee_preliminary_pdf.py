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
source=json.loads((ROOT/"data/werribee_preliminary_nov28_2026.json").read_text(encoding="utf-8"))
stem="Melbourne_vs_Werribee_Advance_Scouting_Preliminary_Nov28_2026"
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



heading("MELBOURNE vs WERRIBEE | ADVANCE SCOUTING")
para("<b>Saturday 28 November 2026 | Melbourne HOME | Surrey Park Arthur Field | PRELIMINARY</b>")
para("<b>Official November 24 ladder snapshot:</b> Werribee 15th, 1-9-0, 40 RF, 110 RA, -70 differential (ten completed games); Melbourne 9th, 5-6-1, 67 RF, 89 RA, -22 differential (twelve games). Melbourne sits one place outside the top-eight playoff cutoff.")
para("<b>Unverified fixture:</b> Werribee played Doncaster on Tuesday November 24 according to the supplied schedule, but the result and player data have not been provided or verified. The ten-game 1-9-0 record and 40-110 run ledger are NOT adjusted for that game.")
para("<b>Player source coverage:</b> Eight supplied GameDay-style batches, not ten complete league games. Their hitter rows add up to only 13 runs, versus 40 runs on the official ladder; missing game boxes or incomplete individual rows must not be treated as zero. Pitchers account for 58.1 recorded IP; one entry has more earned runs than total runs and remains flagged.")
heading("TEAM TENDENCIES & MATCHUP")
para("Werribee are averaging 4.00 runs scored and 11.00 allowed per official game, with a -70 differential. Melbourne are averaging 5.58 scored and 7.42 allowed. These are team-level official ladder calculations; player scouting rates below come exclusively from eight supplied batches and are NOT full-season totals.")
para("<b>Available batting sample:</b> 250 PA, 220 AB, 54 hits, eight doubles, four homers, 19 walks, 50 strikeouts and two documented stolen bases; sample AVG .245, estimated OBP .325, SLG .336, OPS .662. Only two known stolen bases are in these uploaded rows; unknown games can increase the real total.")
para("<b>Available pitching sample:</b> 58.1 recorded innings, 108 hits, 52 walks, 45 strikeouts and 99 runs allowed. The calculated 13.27 sample ERA (86 ER) is especially provisional because Trent Pantalleresco has an impossible 14 R / 16 ER entry in one supplied game; his line is preserved for review rather than altered.")
para("<b>Matchup priority:</b> Do not equate a poor team record with a lack of dangerous individuals. Manuel Jackson has documented NCAA Division I and additional U.S. high-level experience. Tevz Gantar brings Slovenian national-team and Swedish top-division experience. Their limited VSBL batting samples should not be used to dismiss them.")
heading("BATTING | 8 SUPPLIED GAME BATCHES / 10 OFFICIAL / OPS - HIGH TO LOW")
bat=apply_advance_batting_pa_cutoff(source["batting"])
batteam=next(x for x in bat if x.get("Team Total"))
def opsval(r):
    try: return float(str(r.get("OPS","")).replace("*",""))
    except ValueError: return -1.0
batplayers=sort_batters_by_ops(bat)
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
# Normalize only the font-limited accented spelling; raw JSON preserves Tevž.
batrows=[dict(r,Player=("Tevz Gantar" if r["Player"]=="Tevž Gantar" else r["Player"])) for r in batplayers]+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* AVG and batting scouting qualification: 10 PA (double-digit plate appearances). Only AVG gets a qualification asterisk. Qualified batters appear first in descending OPS, then LIMITED batters in descending OPS, with TEAM TOTAL last. Manuel Jackson (17 PA) qualifies at this cutoff and remains THREAT. BATTING classifications: THREAT red, CAUTION yellow, ATTACK green, LIMITED gray; unknown handedness is blank and retains row shading.")
para("The source has inconsistent hits vs singles/doubles for Jimmy Bent in one batch, and PA vs sacrifice bunt for Cooper Bishop-Worn and Tevz Gantar. Supplied figures are retained. Sample team total is WEAK based on league-relative official team results, and is not a substitute for all ten complete games.")
heading("PITCHING | IDENTIFIED APPEARANCES")
pit=source["pitching"]
pitqualified,pitnonqualified=sort_pitchers_by_era_qualification(pit,min_outs=10)
pitteam=next(x for x in pit if x.get("Team Total"))
pitcols=["Player","Throws","IP","H","R","ER","BB","HBP","SO","ERA","WHIP","K/9","BB/9","Scouting Read"]
def pitcherdisplay(r): return dict(r,Player=("Tevz Gantar" if r["Player"]=="Tevž Gantar" else r["Player"]))
para("<b>QUALIFIED PITCHERS | ERA</b>")
table(pitcols,[pitcherdisplay(r) for r in pitqualified]+([pitteam] if not pitnonqualified else []),[125,35,35]+[35]*6+[42]*4+[85])
if pitnonqualified:
    para("<b>NON-QUALIFIED PITCHERS | ERA</b>")
    table(pitcols,[pitcherdisplay(r) for r in pitnonqualified]+[pitteam],[125,35,35]+[35]*6+[42]*4+[85])
para("* ERA qualification: 10 recorded outs (3.1 IP), one out per ten official team games. Only ERA receives a qualification asterisk. IP is displayed in baseball innings-and-outs notation. PITCHING classifications: STRONG red, CAUTION yellow, ATTACK green, LIMITED gray; unverified handedness blank.")
para("Werribee TEAM TOTAL pitching scouting read is VERY WEAK compared with league-wide team run prevention, but the uploaded pitching totals are incomplete. Trent Pantalleresco's batch D lists 14 runs but 16 earned. Do not interpret his calculated ERA or team-source ERA as officially verified until the scorer's box is reconciled; other missing games may affect totals.")
heading("COACHING & LINEUP USAGE")
notes=[
"1. Offensive target: Manuel Jackson (17 PA, 2.037 OPS, two HR) is the coaching-approved top red THREAT and meets the new 10-PA qualifier. Parks Halasz (29 PA, .845 OPS) and Thomas Kerr-Chapman (31 PA, .700 OPS) warrant caution.",
"2. Manuel Jackson is a verified left-handed hitter with Norfolk State Division I, MLB Draft League and Pioneer League experience. His 2.037 OPS, two home runs and advanced playing experience warrant the coaching-approved red THREAT classification (placed first in batting). His .636 AVG is qualified under the new 10-PA rule, but the sample remains only 17 PA.",
"3. Tevz Gantar is a right-handed pitcher with national-team and Swedish Elitserien experience. His five recorded innings include five strikeouts and three walks, but usage after the supplied batches is unverified. His limited sample should not be confused with overall ability.",
"4. Werribee's uploaded pitchers have allowed substantial walks and hits: 52 walks and 108 hits in 58.1 identified innings. Prioritize plate discipline, quality at-bats and productive contact, while checking their most recent starter and bullpen availability.",
"5. Roster usage / depth: Eight supplied Werribee box scores list only 9 to 12 named players each (four with 9 players, three with 10, one with 12). This points to potentially shallow game-day depth, especially for substitutes and bullpen options, but the full active roster and available bench are not verified. Cooper Bishop-Worn, Jimmy Bent, Parks Halasz, Thomas Kerr-Chapman and Erdrin Berisha appear repeatedly; exact batting-order positions and November 24 usage remain unknown.",
"6. Werribee's official -70 differential indicates significant run prevention challenges, but Baseball Victoria also documented strong recent performances from Parks Halasz and Tevz Gantar against Sandringham. Do not infer pitch shape, injury status or defense from these aggregate statistics.",
"7. Melbourne's recent 9-8 road win over Malvern is included in the 5-6-1 ladder but the individual player box score remains pending. The coaching staff should confirm current rest and likely pitching availability from its own internal scorebook before the Werribee game."
]
for n in notes: para(n)
heading("HIGHER-LEVEL PLAYING EXPERIENCE | VERIFIED SOURCES")
para("<b>Manuel (Manny) Jackson (L/R):</b> Norfolk State NCAA Division I catcher, 2024 HBCU Swingman Classic selection, and experience in the MLB Draft League and Pioneer League. Sources: Norfolk State 2024 roster (nsuspartans.com/sports/baseball/roster/manny-jackson/6533); baseballjobsoverseas.com/players/manuel-jackson/; Wyndham Star Weekly November 2026.")
para("<b>Tevz Gantar (R/R):</b> Slovenian national-team pitcher, 2026 Swedish Elitserien Pitcher of the Year with Karlskoga Bats; played in the Croatian league and European competition. Sources: Wyndham Star Weekly November 19, 2026; baseballjobsoverseas.com/players/tevz-gantar/.")
para("<b>Cooper Bishop-Worn:</b> Werribee youth/Victorian representative experience, documented by Baseball Victoria. <b>Parks Halasz:</b> Baseball Victoria youth state representative and national youth championship experience. Do NOT label either as adult professional without verifying additional credentials.")
heading("DATA QUALITY & NEXT UPDATE")
para("Sources: user-supplied 38-column GameDay rows grouped into eight undated batches; official VSBL November 24 ladder snapshot; Melbourne fixture list for Saturday November 28; independent experience verification from Baseball Victoria, Norfolk State, Werribee club coverage and player profiles. Batting and pitching player sample may omit two full official games plus individual rows. Dates and opponents of supplied batches cannot be independently assigned.")
para("Required corrections before final club distribution: November 24 Werribee-Doncaster result and player box; any other missing individual-game scorebooks; reconcile Trent Pantalleresco's 14 R / 16 ER game, Jimmy Bent's contradictory hit decomposition and sacrifice-bunt/PA discrepancies; refresh both team standings and verify latest pitcher usage. Unknown statistics and handedness must remain blank, not zero.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)
lines=["MELBOURNE vs WERRIBEE | PRELIMINARY | 28 NOV 2026",
       "Werribee 15th 1-9-0, 40 RF/110 RA/-70 (10 official); Melbourne 9th 5-6-1, 67 RF/89 RA/-22 (12 official).",
       "8 supplied Werribee statistical batches, not 10 complete games. Nov 24 game vs Doncaster unknown.",
       "", "BATTING | 8 SUPPLIED GAME BATCHES / 10 OFFICIAL / OPS - HIGH TO LOW", " | ".join(batcols)]
for r in batrows: lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines += ["","PITCHING","QUALIFIED PITCHERS | ERA"," | ".join(pitcols)]
for r in pitqualified: lines.append(" | ".join(str(pitcherdisplay(r).get(k,"") or "") for k in pitcols))
if pitnonqualified:
    lines += ["","NON-QUALIFIED PITCHERS | ERA"," | ".join(pitcols)]
    for r in pitnonqualified: lines.append(" | ".join(str(pitcherdisplay(r).get(k,"") or "") for k in pitcols))
lines.append(" | ".join(str(pitteam.get(k,"") or "") for k in pitcols))
lines += ["","COACHING & LINEUP USAGE"] + notes + ["","EXPERIENCE","Manny Jackson: NCAA D1, MLB Draft League/Pioneer League. Tevz Gantar: Slovenia National Team/Swedish Elitserien Pitcher of Year 2026. See PDF for sources.","","DATA QUALITY","Nov24 Werribee vs Doncaster result unknown; sample source flags hit decomposition, PA/sac bunt and pitcher ER > R issues."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
