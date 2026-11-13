# Melbourne Baseball Club — Interactive League Scouting Dashboard

**Public dashboard:** https://asmittty11.github.io/melbourne-baseball-dashboard/

This is a public, browser-based analytics and advance-scouting dashboard for Melbourne Baseball Club in the semi-professional VSBL Premier Division 1. It is a **living 2026–27 season project**, built to grow as games are played across Melbourne's scheduled **30-game season**. The current Melbourne dataset covers **eight games**; future updates are added when source statistics are available and checked. Updates are manual, not an automatic live-game feed. Scouting and performance reports are published as completed with Melbourne Baseball Club's approval. No RStudio or Shiny server is required.

## Interactive views
- **Overview:** Melbourne's latest uploaded eight-game snapshot (4–4–0, 8th; 52 runs for and 57 against), updated as the season progresses.
- **Melbourne Players:** sortable cumulative batting and pitching data through eight games, with separate team totals and provisional source fields labeled.
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

Data windows differ: Melbourne currently covers **eight games**; uploaded opponent samples cover different numbers of games and may be preliminary. These are **only the uploaded opponent teams**, not the entire VSBL. Some source reports omit PA, OPS, or pitching appearances; those fields are blank or explicitly labeled as estimates rather than invented. Team totals are displayed separately and are not ranked as players. The Melbourne Round 5 weekly report is archival and is not counted twice in cumulative season totals.

## Publishing
The `.github/workflows/extract-assets.yml` workflow extracts the dashboard archive into the repository and commits the website, data, PDFs, and text reports. GitHub Pages builds from the `main` branch.

Underlying data last compiled: November 11, 2026 (per `data/league_stats.json` metadata).

## Season coverage, publication and refresh policy
Melbourne's schedule includes **30 games** for 2026–27. This project will grow throughout the season, with the latest uploaded Melbourne data currently spanning **eight games**. The eight-game snapshot is a reporting cutoff, not a final season dataset or a claim that all 30 games have been played.

Melbourne player and team statistics are refreshed after new game statistics are uploaded and checked. Opponent datasets are updated when new advance-scouting work is completed, often before a matchup. Reports are **published as they are completed with Melbourne Baseball Club's approval**. Updates are manual and do **not** represent automatic live GameDay synchronization. Where a source contains missing fields, estimates, or provisional stat mappings, those limitations are documented.

## Table sorting and pitching display
ERA and WHIP default to ascending order (lowest first) when selected, including on initial ERA-based views; AVG remains descending. Melbourne pitching displays neither Throws nor games/appearances. The Melbourne batting table does not display RBI.

The package extraction workflow refreshes archived reports only; it deliberately avoids overwriting independently maintained dashboard code or statistical tables.

## Current Melbourne snapshot — through Game 8
The currently uploaded Melbourne dataset covers **eight games**: **4–4–0**, **8th** in the supplied ladder, **52 runs scored**, **57 runs allowed**, and a **−5 run differential**. Game 8 was a **5–1 win over Sandringham**. The current cumulative report is `reports/Melbourne_Season_Stats_Through_Game8_Sandringham_Updated.pdf`.

**Data-quality note:** The supplied Game 8 player table did not include complete column headers, so some player-stat mappings remain provisional. The record and team runs use the official ladder/final-score information; provisional player-stat interpretations should not be treated as verified official totals. Some OBP/OPS values are also explicitly estimated because historical HBP/SF/CI data are incomplete.

### Historical Game 7 source note (November 7, 2026)
The earlier 21–4 win over Upwey FTG brought Melbourne to 3–4–0 (47 runs for, 56 against). Its report, `reports/Melbourne_Season_Stats_Through_Game7_UpweyFTG_Updated.pdf`, is preserved for reference. The Game 7 pitching row's R values conflicted with the official runs allowed, so the official final score was used for team runs. Previous six-game files remain archived. Melbourne's RBI column is omitted from the player dashboard.

## Melbourne OBP and OPS estimates
The sortable Melbourne player/team tables now display **estimated** OBP and OPS for every batter and the team total. OBP uses `(H+BB)/(AB+BB)` because full historical HBP, SF and CI are unavailable; OPS adds SLG calculated from cumulative total bases divided by AB before rounding. These are approximations rather than verified official OBP/OPS. Opponent scouting tables, reports, source windows and game totals remain unchanged.

## Sandringham advance scouting — November 8, 2026 update
New six-game report for the November 10 matchup incorporates the November 7 4–3 win: Sandringham 9th (3–3, RF 34, RA 43, RD −9), Melbourne 10th (3–4). Player batting and pitching tables now reflect six games. OBP and OPS are explicitly estimated due to incomplete historical HBP/SF/CI. Original five-game PDF remains archived. New PDF: `reports/Melbourne_vs_Sandringham_Advance_Scouting_Nov10_2026_Six_Game_Updated.pdf`.

## Waverley preliminary advance — November 14, 2026 away matchup
Added preliminary Waverley scouting with four scored games (4–0, 54 RF, 8 RA, 3rd) and 13 batters, five pitchers. The games scheduled October 3, October 31 and November 7 are unreported and **not** included. Updated standings and player totals only after source verification. Original PDF and readable text are in `reports/` and `text_reports/`; source dataset is `data/waverley_preliminary_20261109.json`. Existing opponents and Melbourne data remain preserved.
