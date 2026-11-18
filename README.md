# Melbourne Baseball Club — Interactive League Scouting Dashboard

**Public dashboard:** https://asmittty11.github.io/melbourne-baseball-dashboard/

This is a public, browser-based analytics and advance-scouting dashboard for Melbourne Baseball Club in the semi-professional VSBL Premier Division 1. It is a **living 2026–27 season project**, built to grow as games are played across Melbourne's scheduled **30-game season**. The current Melbourne dataset covers **ten games** (4–5–1); future updates are added when source statistics are available and checked. Updates are manual, not an automatic live-game feed. Scouting and performance reports are published as completed with Melbourne Baseball Club's approval. No RStudio or Shiny server is required.

## Interactive views
- **Overview:** Melbourne's latest uploaded ten-game snapshot (4–5–1, 8th; 53 runs for and 63 against), updated as the season progresses.
- **Melbourne Players:** sortable cumulative batting and pitching data through ten games, with separate team totals and provisional source fields labeled.
- **Opponent Batting / Opponent Pitching:** filter available opponent data by club; search and sort columns; export filtered CSV.
- **League Comparison:** Melbourne and available scouting opponents (including Doncaster, Upwey FTG, Sandringham, Waverley, and Moorabbin) for cross-team comparisons; coverage varies by opponent.
- **Report Text:** searchable text versions of available published reports.
- **Original PDFs:** scouting, season performance, and historical reports published and archived as completed with club approval.
- **Data Notes:** scope, source and missing-data cautions.

## Source data
- `data/league_stats.json`: structured player rows and report references.
- `data/dashboard.json`: earlier Sandringham scouting snapshot.
- `text_reports/`: searchable text extracted from available uploaded reports.
- `reports/`: published scouting, performance, and archived PDF reports.
- `assets/Melbourne_Baseball_Web_Dashboard.zip`: complete dashboard source archive.

Data windows differ: Melbourne currently covers **ten games**; uploaded opponent samples cover different numbers of games and may be preliminary. These are **only the uploaded opponent teams**, not the entire VSBL. Some source reports omit PA, OPS, or pitching appearances; those fields are blank or explicitly labeled as estimates rather than invented. Team totals are displayed separately and are not ranked as players. The Melbourne Round 5 weekly report is archival and is not counted twice in cumulative season totals.

## Publishing
The `.github/workflows/extract-assets.yml` workflow extracts the dashboard archive into the repository and commits the website, data, PDFs, and text reports. GitHub Pages builds from the `main` branch.

Underlying data last compiled: November 18, 2026 (per `data/league_stats.json` metadata).

## Season coverage, publication and refresh policy
Melbourne's schedule includes **30 games** for 2026–27. This project will grow throughout the season, with the latest uploaded Melbourne data currently spanning **ten games**. The ten-game snapshot is a reporting cutoff, not a final season dataset or a claim that all 30 games have been played.

Melbourne player and team statistics are refreshed after new game statistics are uploaded and checked. Opponent datasets are updated when new advance-scouting work is completed, often before a matchup. Reports are **published as they are completed with Melbourne Baseball Club's approval**. Updates are manual and do **not** represent automatic live GameDay synchronization. Where a source contains missing fields, estimates, or provisional stat mappings, those limitations are documented.

## Table sorting and pitching display
ERA and WHIP default to ascending order (lowest first) when selected, including on initial ERA-based views; AVG remains descending. Melbourne pitching displays neither Throws nor games/appearances. The Melbourne batting table does not display RBI.

The package extraction workflow refreshes archived reports only; it deliberately avoids overwriting independently maintained dashboard code or statistical tables.

## Current Melbourne snapshot — through Game 10 (November 17, 2026)
Melbourne is **8th, 4–5–1** on the November 18 user-supplied ladder after the **0–0 draw with Moorabbin**. Runs scored and allowed remain **53–63 (−10)**. The new game adds four singles, two walks, five offensive strikeouts and six recorded scoreless pitching innings (Taylor Perrett 5.0, Joey White 1.0). The current cumulative team batting line is **330 PA / 275 AB / 66 H / .240 AVG / .339 estimated OBP / .345 SLG / .684 estimated OPS / .105 ISO**; pitching is **70.1 IP / 100 H / 36 BB / 67 SO / 60 ER / 7.68 ERA / 1.93 WHIP**. Game 8 Perrett statistics remain provisional; one Zak Skinner source row has a PA/sacrifice-bunt inconsistency. Melbourne's eight documented stolen bases are a known minimum, not a verified complete team total. The latest PDF is `reports/Melbourne_Season_Stats_Through_Game10_Moorabbin_Updated.pdf` and weekly analysis is `text_reports/Melbourne_Weekly_Season_Tendencies_2026-11-18.md`.

November 18 opponent standings update: **Waverley 7–0 (1st), Malvern 8–1 (2nd), Moorabbin 6–1–1 (4th), Sunshine 6–3 (5th)**. Sunshine scouting remains based on **six usable of nine official player-game batches**; its November 17 8–2 win over Upwey FTG is already counted in the team ladder, with three recent player boxes missing. Malvern scouting now includes **eight of nine official game boxes**, including the November 17 0–4 loss to Newport; the 8–3 victory over Sunshine was previously batch 7 and is not double-counted. The one remaining missing Malvern game leaves 15 official runs not reflected in the cumulative batting ledger.


## November 18 opponent source reconciliation

**Malvern (2nd, 8–1–0, 70 RF / 23 RA):** The 8–3 Sunshine game was already imported as game batch 7. The Nov 17 0–4 loss to Newport was added as the eighth distinct player batch: 27 PA, 24 AB, five hits, two BB and one HBP; 5.0 documented pitching innings, eight hits, four earned runs and eight strikeouts. Eight verified batches yield a .355 batting average, .412 OBP, .918 OPS, 63.0 IP and 2.14 ERA. **One older game remains unavailable**; the 55 batting runs in supplied player rows are 15 below the official 70, while pitcher runs (23) reconcile to the official 23 allowed. A missing-game result or individual stats have not been invented.

**Sunshine (5th, 6–3–0, 65 RF / 30 RA):** The November 17 **8–2 win against Upwey FTG** is already included in the nine-game ladder and is not added to team RF again. Three recent individual box scores, including the Nov 17 game and two preceding games, are unavailable; the existing player data represent **six valid batches**. One older pasted batch was malformed and excluded. These are tracked as missing, not zeros.

## Historical Melbourne snapshot — through Game 8 (archived)
The archived Melbourne Game 8 dataset covers **eight games**: **4–4–0**, **8th** in the supplied ladder, **52 runs scored**, **57 runs allowed**, and a **−5 run differential**. Game 8 was a **5–1 win over Sandringham**. The current cumulative report is `reports/Melbourne_Season_Stats_Through_Game8_Sandringham_Updated.pdf`.

**Data-quality note:** The supplied Game 8 player table did not include complete column headers, so some player-stat mappings remain provisional. The record and team runs use the official ladder/final-score information; provisional player-stat interpretations should not be treated as verified official totals. Some OBP/OPS values are also explicitly estimated because historical HBP/SF/CI data are incomplete.

### Historical Game 7 source note (November 7, 2026)
The earlier 21–4 win over Upwey FTG brought Melbourne to 3–4–0 (47 runs for, 56 against). Its report, `reports/Melbourne_Season_Stats_Through_Game7_UpweyFTG_Updated.pdf`, is preserved for reference. The Game 7 pitching row's R values conflicted with the official runs allowed, so the official final score was used for team runs. Previous six-game files remain archived. Melbourne's RBI column is omitted from the player dashboard.

## Melbourne OBP and OPS estimates
The sortable Melbourne player/team tables now display **estimated** OBP and OPS for every batter and the team total. OBP uses `(H+BB)/(AB+BB)` because full historical HBP, SF and CI are unavailable; OPS adds SLG calculated from cumulative total bases divided by AB before rounding. These are approximations rather than verified official OBP/OPS. Opponent scouting tables, reports, source windows and game totals remain unchanged.

## Sandringham advance scouting — November 8, 2026 update
New six-game report for the November 10 matchup incorporates the November 7 4–3 win: Sandringham 9th (3–3, RF 34, RA 43, RD −9), Melbourne 10th (3–4). Player batting and pitching tables now reflect six games. OBP and OPS are explicitly estimated due to incomplete historical HBP/SF/CI. Original five-game PDF remains archived. New PDF: `reports/Melbourne_vs_Sandringham_Advance_Scouting_Nov10_2026_Six_Game_Updated.pdf`.

## Waverley preliminary advance — November 14, 2026 away matchup
Added preliminary Waverley scouting with four scored games (4–0, 54 RF, 8 RA, 3rd) and 13 batters, five pitchers. The games scheduled October 3, October 31 and November 7 are unreported and **not** included. Updated standings and player totals only after source verification. Original PDF and readable text are in `reports/` and `text_reports/`; source dataset is `data/waverley_preliminary_20261109.json`. Existing opponents and Melbourne data remain preserved.
