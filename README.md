# Melbourne Baseball Club — Public Scouting Dashboard

**Website:** https://asmittty11.github.io/melbourne-baseball-dashboard/

This is a static, responsive, browser-based conversion of the Melbourne Baseball Club (VSBL Premier 1) scouting dashboard, requiring no RStudio, R Shiny, or server account.

## Live dashboard contents

- **Overview:** six-game Melbourne and five-game Sandringham snapshots, plus report links.
- **Melbourne Players:** original supplied Melbourne season statistics PDF.
- **Opponent Batting:** searchable and sortable Sandringham batting statistics, including classifications and qualification handling.
- **Opponent Pitching:** searchable Sandringham pitching statistics and scouting classifications.
- **Advance Reports:** original five PDF reports, stored in `reports/` and readable in the embedded viewer or as separate files.
- **Data Notes:** historical data provenance and limitations.

## Files

- `index.html` — full interactive dashboard.
- `data/dashboard.json` — Sandringham cumulative batting/pitching and report manifest.
- `data/melbourne_batting_source.txt`, `data/melbourne_pitching_source.txt` — Melbourne cumulative sources.
- `reports/` — five original PDF reports, unchanged from the supplied package.
- `assets/Melbourne_Baseball_Web_Dashboard.zip` — complete source archive.
- `.github/workflows/extract-assets.yml` — reproducible extraction from the source archive.

## Maintenance

Update `index.html`, `data/`, or `reports/` through GitHub. GitHub Pages uses the repository's branch publication process. Updating the ZIP triggers the extraction workflow and can overwrite these files with the archive versions.

**Important:** All statistics are historical snapshots, not automatically updated official league data. Player data and historical appearances have not been fully reconciled and the reports should be interpreted with their respective date and source limitations.
