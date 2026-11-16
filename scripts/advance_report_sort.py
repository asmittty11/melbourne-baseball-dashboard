"""Shared advance-scouting presentation rules.

For all future opponent advance scouting PDFs, sort individual BATTERS by
OPS descending (highest first), using player name to break ties.
Keep TEAM TOTAL rows outside this sort and append at the bottom.
Pitching does not have an OPS metric, so its established ordering is unchanged.
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
    """Return only player rows, sorted by decreasing numeric OPS, then name."""
    return sorted(
        (row for row in rows if not row.get("Team Total")),
        key=lambda row: (-_ops_score(row), str(row.get("Player", "")).casefold()),
    )
