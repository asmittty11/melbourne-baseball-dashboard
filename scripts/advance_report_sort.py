"""Shared advance-scouting presentation rules.

All future opponent advance-scouting batting tables must place qualified
individual hitters first, sorted by numeric OPS descending. Batters with
Scouting Read LIMITED come afterwards, also sorted by numeric OPS descending.
Break ties alphabetically. Never include TEAM TOTAL in player sorting;
report generators append it as the last row.

Pitching retains the established appearance/innings order; OPS is a batting
metric and is not used for pitchers.
"""
from math import inf


def _ops_score(row):
    value = row.get("OPS")
    if value is None or str(value).strip() in ("", "-", "—", "–"):
        return -inf
    try:
        return float(str(value).replace("*", "").strip())
    except (ValueError, TypeError):
        return -inf


def sort_batters_by_ops(rows):
    """Qualified OPS high-to-low, then LIMITED OPS high-to-low; totals excluded."""
    return sorted(
        (row for row in rows if not row.get("Team Total")),
        key=lambda row: (
            str(row.get("Scouting Read", "")).strip().upper() == "LIMITED",
            -_ops_score(row),
            str(row.get("Player", "")).casefold(),
        ),
    )
