# Melbourne Baseball Club — Web Scouting Dashboard

Public, browser-based analytics for Melbourne Baseball Club (VSBL Premier 1, 2026–27).

**Website:** https://asmittty11.github.io/melbourne-baseball-dashboard/

## Included in this repository

- `index.html`: responsive, interactive dashboard with overview, player statistics access, searchable/sortable Sandringham batting data, searchable pitching data, reports panel, and data notes.
- `data/dashboard.json`: 15 Sandringham hitters, 5 pitchers, and scouting/report metadata.
- `data/melbourne_batting_source.txt` and `data/melbourne_pitching_source.txt`: six-game Melbourne reference data.
- `.github/workflows/pages.yml`: automatic Pages deployment on commits to `main`.

## Original PDF reports

**Pending upload:** the five original PDF files referenced by the dashboard in the `reports/` directory have *not* been transferred yet. PDF viewer/download links will not work until those exact originals are present. Please do not interpret these missing files as published reports.

The original PDFs are available in the dashboard archive created in ChatGPT. This repository currently contains the interactive website and text data. No PDF substitutes have been silently published.

## Data accuracy

Figures are historical snapshots, not live league results. Qualification thresholds and data-quality exceptions are explained in the source notes. The Melbourne six-game reference is not a fully reconciled game-level database.

## Maintenance

GitHub Pages publishes automatically when files are committed to the default branch. Report filenames used by the dashboard are in `data/dashboard.json`.
