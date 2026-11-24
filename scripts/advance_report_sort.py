"""Shared advance-scouting presentation sorting rules.

For opponent batting, put qualified (non-LIMITED) players first by OPS
descending, followed by LIMITED players separately by OPS descending.
Keep TEAM TOTAL last; never include it in player sorting.
For opponent pitching, group by recorded innings qualification, qualified first
and non-qualified next; sort each group by numeric ERA ascending.
Report generators keep TEAM TOTAL at the bottom of the full pitching section.
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
    """Qualified batters by OPS desc; LIMITED batters by OPS desc, total excluded."""
    return sorted(
        (row for row in rows if not row.get("Team Total")),
        key=lambda row: (
            str(row.get("Scouting Read", "")).strip().upper() == "LIMITED",
            -_ops_score(row),
            str(row.get("Player", "")).casefold(),
        ),
    )


def _innings_outs(value):
    """Parse baseball-style IP (3.1 = 10 outs, not 3.1 decimal innings)."""
    try:
        full, fractional = str(value).strip().split(".")
        outs = int(fractional)
        if outs not in (0, 1, 2):
            return -1
        return int(full) * 3 + outs
    except (ValueError, AttributeError):
        return -1


def _era_score(row):
    try:
        return float(str(row.get("ERA", "")).replace("*", "").strip())
    except (ValueError, TypeError):
        return inf


def sort_pitchers_by_era_qualification(rows, min_outs=9):
    """Return (qualified, unqualified), ERA ascending in each; exclude team total."""
    pitchers = [row for row in rows if not row.get("Team Total")]
    order = lambda row: (_era_score(row), str(row.get("Player", "")).casefold())
    qualified = sorted((r for r in pitchers if _innings_outs(r.get("IP")) >= min_outs), key=order)
    unqualified = sorted((r for r in pitchers if _innings_outs(r.get("IP")) < min_outs), key=order)
    return qualified, unqualified
