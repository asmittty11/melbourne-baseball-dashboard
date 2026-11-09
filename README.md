# Melbourne Baseball Club — Interactive League Scouting Dashboard

**Public dashboard:** https://asmittty11.github.io/melbourne-baseball-dashboard/

This is a static, browser-based VSBL Premier 1 analytics and advance scouting dashboard; no RStudio or Shiny server is required.

## Interactive views
- **Overview:** Melbourne's seven-game season snapshot (3–4, 10th; 47 RF and 56 RA).
- **Melbourne Players:** sortable seven-game batting and pitching data, with source team totals separated.
- **Opponent Batting / Opponent Pitching:** filter by all uploaded opponents or a specific club; search and sort columns; export filtered CSV.
- **League Comparison:** combined Melbourne, Doncaster, Upwey FTG and Sandringham player tables for cross-team comparisons.
- **Report Text:** searchable, plain-text versions of all five original PDFs.
- **Original PDFs:** original scouting and season reports preserved.
- **Data Notes:** scope, source and missing-data cautions.

## Source data
- `data/league_stats.json`: structured player rows and report references.
- `data/dashboard.json`: earlier Sandringham scouting snapshot.
- `text_reports/`: full text extracted from the five uploaded PDFs.
- `reports/`: the unchanged original five PDFs.
- `assets/Melbourne_Baseball_Web_Dashboard.zip`: complete dashboard source archive.

Data windows differ: Melbourne six games, Doncaster five, Upwey FTG four, Sandringham six. These are **all uploaded opponent teams**, not the entire VSBL. Some source reports omit PA, OPS, or pitching appearances; those fields are blank rather than invented. Team totals are displayed separately and are not ranked as players. The Melbourne Round 5 weekly report is archival and is not added again to six-game totals.

## Publishing
The `.github/workflows/extract-assets.yml` workflow extracts the dashboard archive into the repository and commits the website, data, PDFs, and text reports. GitHub Pages builds from the `main` branch.

Last compiled: November 6, 2026.

## Data refresh policy
Melbourne player and team season statistics are updated in the sortable tables shortly after each game's verified stats are uploaded into the system. Opponent data is updated only when a new advance scouting report is published for that opponent, generally in preparation for an upcoming rematch. These updates are manual-upload-driven and not an automatic live GameDay synchronization.

## Table sorting and pitching display
ERA and WHIP default to ascending order (lowest first) when selected, including on initial ERA-based views; AVG remains descending. Melbourne pitching displays neither Throws nor games/appearances. The Melbourne batting table does not display RBI.

The package extraction workflow refreshes archived reports only; it deliberately avoids overwriting independently maintained dashboard code or statistical tables.

## Latest Melbourne result (uploaded November 7, 2026)
21–4 win over Upwey FTG; official ladder snapshot: 10th place, 7 games, 3–4–0, 47 runs scored and 56 allowed, 42.86% won, run differential −9.

New primary season PDF: `reports/Melbourne_Season_Stats_Through_Game7_UpweyFTG_Updated.pdf`. Previous six-game PDF preserved for audit. Season totals update from the supplied fixed-position game data. **Caution:** the new game's pitcher R fields total 8, conflicting with the official four runs allowed. Team record and RA use the final score. Pitching component metrics remain subject to game-level verification. OBP/OPS are omitted for affected hitters because incomplete old HBP/SF/CI totals prevent defensible recalculation; they are not zero. MLB-style innings notation is preserved. Melbourne's RBI column remains omitted at the user's request.

## Melbourne OBP and OPS estimates
The sortable Melbourne player/team tables now display **estimated** OBP and OPS for every batter and the team total. OBP uses `(H+BB)/(AB+BB)` because full historical HBP, SF and CI are unavailable; OPS adds SLG calculated from cumulative total bases divided by AB before rounding. These are approximations rather than verified official OBP/OPS. Opponent scouting tables, reports, source windows and game totals remain unchanged.

## Sandringham advance scouting — November 8, 2026 update
New six-game report for the November 10 matchup incorporates the November 7 4–3 win: Sandringham 9th (3–3, RF 34, RA 43, RD −9), Melbourne 10th (3–4). Player batting and pitching tables now reflect six games. OBP and OPS are explicitly estimated due to incomplete historical HBP/SF/CI. Original five-game PDF remains archived. New PDF: `reports/Melbourne_vs_Sandringham_Advance_Scouting_Nov10_2026_Six_Game_Updated.pdf`.

## Waverley preliminary advance — November 14, 2026 away matchup
Added preliminary Waverley scouting with four scored games (4–0, 54 RF, 8 RA, 3rd) and 13 batters, five pitchers. The games scheduled October 3, October 31 and November 7 are unreported and **not** included. Updated standings and player totals only after source verification. Original PDF and readable text are in `reports/` and `text_reports/`; source dataset is `data/waverley_preliminary_20261109.json`. Existing opponents and Melbourne data remain preserved.
