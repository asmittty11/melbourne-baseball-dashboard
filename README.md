# Melbourne Baseball Analytics & Scouting
### An interactive 2026–27 season resource for Melbourne Baseball Club

A public-facing dashboard for exploring player performance, team tendencies, opponent scouting and coaching reports in Australia's Victorian Summer Baseball League (VSBL) Premier Division 1.

**[Explore the Live Website ↗](https://asmittty11.github.io/melbourne-baseball-dashboard/)** &nbsp; | &nbsp; **[View the Latest Season PDF](reports/Melbourne_Season_Stats_Through_Game12_Malvern_Updated.pdf)** &nbsp; | &nbsp; **[Read Weekly Tendencies](text_reports/Melbourne_Weekly_Season_Tendencies_2026-11-25.md)**

---

## The Project at a Glance

| Season snapshot | November 25, 2026 (official ladder November 24) |
| :--- | :--- |
| **Melbourne official record** | **5–6–1**, 9th place, 67 runs for / 89 against (−22) |
| **Official Melbourne games** | 12 |
| **Melbourne player-stat batches** | 12 (all 12 completed official games, through November 24 Malvern win) |
| **Official ladder coverage** | 16 teams, dated snapshot with top-eight playoff cutoff |
| **Regular-season schedule** | Approximately 30 Melbourne games |
| **Publishing approach** | Manual, source-checked game uploads and GitHub-hosted reports |

The Visual Insights tab also shows **Melbourne Hit Distribution** (single/double/triple/home-run proportions) and **Melbourne Hit Leaders** (top eight players by cumulative hits, each subdivided by hit type). Singles are calculated as H−2B−3B−HR and the team and player totals currently reconcile. These are not field-location spray charts: batted-ball coordinates and directional hit data have not been supplied. The new visuals refresh automatically from the same JSON and do not affect original scouting or player tables.

Visual Insights charts read from the existing `data/league_stats.json` file at page load; they do not store duplicate or manually maintained chart values. Official W–L–D and runs scored/allowed come from the official standings; player leaderboards use Melbourne's existing PA and pitching-out qualification rules. Pooled league comparisons use only uploaded team totals (currently 10 teams, Melbourne included), so they should not be described as complete official 16-team benchmarks. Historical estimated OBP/OPS and provisional source limitations remain. Do not add game-by-game trend lines until complete verified game-level data support them.

The **live website** is the best place to explore the project. This repository documents its data, production workflow and archived outputs.

## What the Website Includes

| Section | Purpose |
| :--- | :--- |
| **Overview** | Official standings, season results, top-eight playoff cutoff and direct links into the analysis |
| **Melbourne Players** | Sortable cumulative batting and pitching, advanced rates and independent TEAM TOTAL rows |
| **Visual Insights** | Responsive, source-derived season W–L–D and run balance, uploaded-league batting/pitching benchmarks, and qualified Melbourne player OPS/ERA leaderboards |
| **Opponent Batting** | Filterable hitter performance and color-coded scouting assessments |
| **Opponent Pitching** | Pitcher usage, ERA, WHIP, strikeout/walk rates and scouting assessments |
| **League Comparison** | Combined uploaded statistical samples across Melbourne and scouted opponents |
| **Report Text** | Searchable versions of completed tendencies and advance scouting reports |
| **Original PDFs** | Downloadable club reports and preserved historical versions |
| **Data Notes** | Missing games, source exceptions, estimates and reporting-window definitions |

All interactive data remains on the site; the README is an orientation page, not a replacement for the dashboard.

## Where the Data Come From

Game-level player statistics are compiled from supplied GameDay scoring records; official league standings are maintained as separately dated snapshots. The central structured source is **[`data/league_stats.json`](data/league_stats.json)**, with report PDFs in [`reports/`](reports/) and text versions in [`text_reports/`](text_reports/).

The dashboard is **not** a live GameDay synchronization or an authoritative replacement for the VSBL's official records. Player-level game coverage often trails the official ladder until the game's box scores are published. Missing or unverified statistics remain blank or explicitly flagged, rather than treated as zero.

### Statistical conventions

- **Batting:** AVG, estimated OBP, SLG, OPS, ISO and BB%. Historical HBP/SF/CI may be incomplete; OBP and OPS are labeled estimates. Known stolen bases are retained; unknown values stay blank.
- **Pitching:** Baseball innings notation (`0.1` = one out, `0.2` = two outs), ERA, WHIP, K/9, BB/9 and K/BB.
- **Melbourne qualification:** AVG requires two PA per official team game; ERA requires one out per official team game. Qualification asterisks appear only on AVG and ERA.
- **Opponent advance scouting batting qualification (effective November 24, 2026):** **10 or more PA** is qualified, including exactly 10. Players below 10 PA are **LIMITED** unless explicitly overridden by the coaching staff. Only qualifying AVG asterisks change with the cutoff; preserve all other batting statistics and scouting colors. This applies to updated and future advance scouting reports, not historical archived PDFs.
- **Opponent batting PDF order:** Qualified batters in **descending OPS**, followed by LIMITED batters in **descending OPS**, with TEAM TOTAL last.
- **Opponent Pitching dashboard qualification (effective November 24, 2026):** pitchers with at least **3.0 IP (nine recorded outs)** are shown with regular STRONG, CAUTION, or ATTACK classifications. Those below 3.0 IP are **LIMITED**, sorted last, and their ERA alone carries the qualification asterisk. This dashboard-only display rule does not change League Comparison, source pitching data, or advance scouting PDF qualification rules.
- **Opponent pitching PDF order:** QUALIFIED PITCHERS | ERA, then NON-QUALIFIED PITCHERS | ERA; each subsection by ascending ERA.
- **Scouting classifications:** Batting THREAT (red), CAUTION (yellow), ATTACK (green), LIMITED (gray); pitching STRONG (red), CAUTION, ATTACK, LIMITED. Explicit coaching-approved player overrides, such as the Sunshine batting STRONG cases, are retained as supplied. Team assessments are evaluated separately relative to league-wide team performances.
- **Team-level scouting-read baseline (effective November 27, 2026):** Compare each team's batting *and* pitching TEAM TOTAL rates to the pooled LEAGUE TOTALS dynamically computed from uploaded team totals in the dashboard's League Comparison, rather than to generic MLB or neutral-league standards. This is a hitter-friendly VSBL environment and difficult for pitchers. For the currently uploaded **10 teams**, pooled batting is **0.291 AVG / 0.372 estimated OBP / 0.428 SLG / 0.800 estimated OPS**, while pooled pitching is **6.61 ERA / 1.80 WHIP / 9.00 K/9 / 5.06 BB/9** across **523.0 IP**. Recalculate the pooled baseline whenever teams or game batches change; never assume it is the full official 16-team league. Lower ERA, WHIP and BB/9 indicate stronger pitching; higher K/9 is favorable, but assess the combination rather than requiring every individual rate to beat average. Higher AVG, OBP, SLG and OPS generally indicate stronger team batting. Consider sample size and missing/inconsistent box scores before assigning an overall team read. Fitzroy's **4.97 ERA / 1.34 WHIP / 8.32 K/9 / 2.59 BB/9** merits **Above Average** team pitching, despite its slightly below-baseline strikeout rate. This guidance is for TEAM TOTAL scouting reads only; do not change individual player categories.
- **Handedness:** Only verified batter/pitcher handedness is displayed. Unknown cells remain empty and inherit their row background.

All TEAM TOTAL and LEAGUE TOTAL rows are separated from player sorting. The official team ladder is never derived by summing incomplete player scouting samples.

## Report Generation and Site Updates

This is a static website deployed with **GitHub Pages**, using JavaScript, HTML, CSS and JSON. Python report generators and GitHub Actions produce and publish downloadable PDFs. The dashboard fetches the structured data at page load; it does not require a backend server or a live sports-data API.

The normal sequence is:

1. Collect the newly published game box score, verify its column mapping and check hits, runs, innings and possible scoring discrepancies.
2. Add the game **once** to the player-stat dataset; update the official ladder separately when supplied.
3. Regenerate cumulative season reporting and, for upcoming opponents, the advance scouting reports.
4. Publish PDFs, update the dashboard and retain a dated explanation of missing or provisional data.

**Advance report venue policy:** Melbourne home games list **Surrey Park Arthur Field**. For away games, reports omit the venue and start time rather than inserting unknown placeholders.

## Source Files and Reporting Archive

- [Dashboard website](index.html)
- [Structured season/scouting data](data/league_stats.json)
- [Current November 24 league ladder snapshot](data/official_ladder_20261124.json)
- [November 24 Melbourne–Malvern player scorebook](data/melbourne_malvern_game12_20261124.json)
- [12-player-game cumulative snapshot](data/melbourne_game12_snapshot.json)
- [Latest weekly tendencies report](text_reports/Melbourne_Weekly_Season_Tendencies_2026-11-25.md)
- [Published PDFs](reports/) and [report-generation scripts](scripts/)
- [Historical project and methodology notes](docs/Project_Methodology_Archive_2026-11-18.md)

## Project Context

Melbourne Baseball Club receives recurring performance and opponent analysis from this project during the VSBL 2026–27 season. The goal is to translate available statistics into useful, clearly qualified insights for preparation and coaching. Source quality is treated as part of the analysis: missing game boxes, inconsistent scorebook entries, and provisional historical mappings are documented instead of obscured.

**[Open the Dashboard](https://asmittty11.github.io/melbourne-baseball-dashboard/)** · **[See More SQL & Analytics Projects](https://github.com/asmittty11/baseball-analytics-portfolio)**

<sub>Last README refresh: November 25, 2026. The published dashboard and latest dated source files should be consulted for newer results as the season progresses.</sub>
