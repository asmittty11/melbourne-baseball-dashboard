# Melbourne Baseball Club — Interactive League Scouting Dashboard

**Public dashboard:** https://asmittty11.github.io/melbourne-baseball-dashboard/

This is a static, browser-based VSBL Premier 1 analytics and advance scouting dashboard; no RStudio or Shiny server is required.

## Interactive views
- **Overview:** Melbourne's six-game season snapshot.
- **Melbourne Players:** sortable six-game batting and pitching data (including RBI column), with source team totals separated. Existing cumulative RBI is blank until verified from game-level uploads.
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

Data windows differ: Melbourne six games, Doncaster five, Upwey FTG four, Sandringham five. These are **all uploaded opponent teams**, not the entire VSBL. Some source reports omit PA, OPS, or pitching appearances; those fields are blank rather than invented. Team totals are displayed separately and are not ranked as players. The Melbourne Round 5 weekly report is archival and is not added again to six-game totals.

## Publishing
The `.github/workflows/extract-assets.yml` workflow extracts the dashboard archive into the repository and commits the website, data, PDFs, and text reports. GitHub Pages builds from the `main` branch.

Last compiled: November 6, 2026.

## Data refresh policy
Melbourne player and team season statistics are updated in the sortable tables shortly after each game's verified stats are uploaded into the system. Opponent data is updated only when a new advance scouting report is published for that opponent, generally in preparation for an upcoming rematch. These updates are manual-upload-driven and not an automatic live GameDay synchronization. RBI must be included in all future Melbourne batting stat reports; do not fill missing historical RBI with zero.
