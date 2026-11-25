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
para("<b>November 24 player box:</b> Newly supplied and included once as Werribee batch nine. The listed Doncaster matchup is consistent with the prior fixture, but the official final was not independently verified. Players total four Werribee runs and 12 pitcher runs allowed in five recorded innings (both pitchers entered with zero earned). The existing ten-game official ladder remains unchanged.")
para("<b>Player source coverage:</b> Nine supplied GameDay-style player batches: eight undated and one for November 24. Their hitter rows total 17 runs, while the separately dated official ten-game ladder lists 40 RF; incomplete/mismatched game coverage remains. Pitching rows total 63.1 IP, 111 R and 86 ER, including important scorer discrepancies. Do not assume all league games are included.")
heading("TEAM TENDENCIES & MATCHUP")
para("The retained official ten-game standings show Werribee averaging 4.00 runs scored and 11.00 allowed, with −70 RD; Melbourne 5.58 scored and 7.42 allowed. The batting and pitching rows below include nine supplied batches and are not reconciled to this dated official snapshot.")
para("<b>Available batting sample:</b> Nine supplied batches: 275 PA, 238 AB, 60 hits, nine doubles, four home runs, 24 walks, 57 strikeouts and two recorded stolen bases; AVG .252, estimated OBP .337, SLG .340, OPS .677. November 24 contributed six hits, four runs, one double, five walks and no home runs. Previous hit-component inconsistencies are retained and flagged.")
para("<b>Available pitching sample:</b> Nine batches: 63.1 recorded IP, 116 H, 59 BB, 52 SO and 111 R, including 86 ER and calculated source ERA 12.22. The latest two pitchers combined for 5.0 IP, 8 H, 7 BB, 7 SO and 12 R with zero ER listed; prior Trent Pantalleresco batch D shows 14 R / 16 ER. Both scoring discrepancies require verification.")
para("<b>Matchup priority:</b> Manuel Jackson remains a coaching-approved THREAT and added two singles on Nov24 (now nine hits, 20 PA, 1.893 OPS in the supplied sample). Cooper Bishop-Worn added a single, double and two RBI; Parks Halasz singled and walked. Tevz Gantar allowed six H, five BB and nine R in three innings per source (zero ER entered). Verify scoring and current pitcher availability before final plans.")
heading("BATTING | 9 SUPPLIED GAME BATCHES / 10 OFFICIAL / OPS - HIGH TO LOW")
bat=apply_advance_batting_pa_cutoff(source["batting"])
batteam=next(x for x in bat if x.get("Team Total"))
def opsval(r):
    try: return float(str(r.get("OPS","")).replace("*",""))
    except ValueError: return -1.0
# All batters including LIMITED are in the same numeric OPS-high-to-low list.
batplayers=sorted((r for r in bat if not r.get("Team Total")), key=lambda r:(-opsval(r), str(r.get("Player","")).casefold()))
batcols=["Player","Bats","PA","AB","R","H","1B","2B","3B","HR","RBI","BB","HBP","SO","SB","AVG","OBP","SLG","OPS","ISO","BB%","Scouting Read"]
# Normalize only the font-limited accented spelling; raw JSON preserves Tevž.
batrows=[dict(r,Player=("Tevz Gantar" if r["Player"]=="Tevž Gantar" else r["Player"])) for r in batplayers]+[batteam]
table(batcols,batrows,[105,25]+[25]*13+[35]*5+[38,72])
para("* Batting AVG and scouting qualification: minimum 10 PA. Only AVG gets a qualification asterisk. All batting players, including LIMITED, appear together by numeric OPS high-to-low with TEAM TOTAL at the bottom. Manuel Jackson (20 PA) remains THREAT; Darcy Boyd now meets 10 PA and is ATTACK. Colors remain THREAT red, CAUTION yellow, ATTACK green, LIMITED gray; unknown handedness blank.")
para("Source exceptions remain: Jimmy Bent's older hit-versus-single/double breakdown, older PA/sacrifice-bunt mismatches for Cooper Bishop-Worn and Tevz Gantar, and new November 24 Jimmy Bent 0 AB/1 SO. Do not silently adjust missing or contradictory data; team batting read remains WEAK and official standings remain separate.")
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
para("Werribee team pitching read remains VERY WEAK, but the source ERA does not represent a verified full season. Earlier Trent Pantalleresco 14 R/16 ER and November 24 12 combined R/0 ER must be checked against official scoring; all source values are kept as supplied.")
heading("COACHING & LINEUP USAGE")
notes=[
"1. Latest November 24 game rows: six hits, five walks and four runs. Cooper Bishop-Worn singled, doubled and drove in two; Manuel Jackson singled twice and Parks Halasz singled and walked. This is player source data, not a verified official result.",
"2. Manuel Jackson, a verified left-handed hitter with Norfolk State NCAA Division I, MLB Draft League and Pioneer League experience, is still the lead THREAT. His sample now shows nine H in 14 AB, 20 PA and 1.893 OPS; check latest lineup placement.",
"3. Tevz Gantar has international and Swedish top-division pitching experience. On November 24 he recorded 3.0 IP, six H, five BB, two SO and nine R with zero ER entered. That earned-run line requires verification; check bullpen rest and usage.",
"4. Cooper Bishop-Worn's November 24 pitching line is 2.0 IP, two H, five SO, two BB, three R and zero ER as supplied. These pitchers allowed seven BB in five source innings; emphasize plate discipline, without guessing pitch mix.",
"5. Nine supplied player batches include nine to twelve named players per game; November 24 has eleven including an all-zero line. This is not evidence of a verified roster cap. Recheck game-to-game lineup and fielding assignment.",
"6. Werribee's previous official ten-game ladder stands at 1–9–0 with −70 RD. The November 24 batting/pitching figures are added without presuming that the official result or updated league ladder is confirmed.",
"7. Melbourne's saved ladder included its 9–8 road win at Malvern. Confirm current Melbourne and Werribee pitcher availability from club scorebooks before November 28."
]
for n in notes: para(n)
heading("HIGHER-LEVEL PLAYING EXPERIENCE | VERIFIED SOURCES")
para("<b>Manuel (Manny) Jackson (L/R):</b> Norfolk State NCAA Division I catcher, 2024 HBCU Swingman Classic selection, and experience in the MLB Draft League and Pioneer League. Sources: Norfolk State 2024 roster (nsuspartans.com/sports/baseball/roster/manny-jackson/6533); baseballjobsoverseas.com/players/manuel-jackson/; Wyndham Star Weekly November 2026.")
para("<b>Tevz Gantar (R/R):</b> Slovenian national-team pitcher, 2026 Swedish Elitserien Pitcher of the Year with Karlskoga Bats; played in the Croatian league and European competition. Sources: Wyndham Star Weekly November 19, 2026; baseballjobsoverseas.com/players/tevz-gantar/.")
para("<b>Cooper Bishop-Worn:</b> Werribee youth/Victorian representative experience, documented by Baseball Victoria. <b>Parks Halasz:</b> Baseball Victoria youth state representative and national youth championship experience. Do NOT label either as adult professional without verifying additional credentials.")
heading("DATA QUALITY & NEXT UPDATE")
para("Sources: eight undated user-supplied GameDay player batches plus the separately dated November 24 box, official ten-game ladder snapshot, Melbourne home fixture, and existing verified playing-experience profiles. Latest source provides four Werribee runs and twelve pitcher runs allowed but no independently confirmed final result; dates and opponents for earlier batches remain unknown.")
para("Before final distribution: verify the November 24 official result and any newer league ladder; obtain remaining older Werribee player-game boxes; check Jimmy Bent's zero AB/one SO on Nov24, new 12 R/0 ER pitcher split, old Trent 14 R/16 ER, and earlier batting decomposition/sacrifice-bunt inconsistencies. Missing handedness remains unknown.")
SimpleDocTemplate(str(pdf),pagesize=landscape(A4),leftMargin=24,rightMargin=24,topMargin=25,bottomMargin=24).build(story)
lines=["MELBOURNE vs WERRIBEE | PRELIMINARY | 28 NOV 2026",
       "Werribee 15th 1-9-0, 40 RF/110 RA/-70 (10 official); Melbourne 9th 5-6-1, 67 RF/89 RA/-22 (12 official).",
       "9 supplied Werribee statistical batches: eight undated plus Nov24 player box. Official ten-game ladder remains separately dated; latest result unverified.",
       "", "BATTING | 9 SUPPLIED GAME BATCHES / 10 OFFICIAL / OPS - HIGH TO LOW", " | ".join(batcols)]
for r in batrows: lines.append(" | ".join(str(r.get(k,"") or "") for k in batcols))
lines += ["","PITCHING","QUALIFIED PITCHERS | ERA"," | ".join(pitcols)]
for r in pitqualified: lines.append(" | ".join(str(pitcherdisplay(r).get(k,"") or "") for k in pitcols))
if pitnonqualified:
    lines += ["","NON-QUALIFIED PITCHERS | ERA"," | ".join(pitcols)]
    for r in pitnonqualified: lines.append(" | ".join(str(pitcherdisplay(r).get(k,"") or "") for k in pitcols))
lines.append(" | ".join(str(pitteam.get(k,"") or "") for k in pitcols))
lines += ["","COACHING & LINEUP USAGE"] + notes + ["","EXPERIENCE","Manuel Jackson: NCAA D1/MLB Draft League/Pioneer League. Tevz Gantar: Slovenia/Swedish Elitserien. Details in PDF.","","DATA QUALITY","Nov24 4 batting R/12 pitcher R and zero earned are box-score source entries, not independent official final; Jimmy Bent zero AB/one SO, older Trent 14 R/16 ER and batting errors flagged."]
txt.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("Generated",pdf,"and",txt)
