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



# Effective for new/updated opponent advance batting reports from November 24, 2026.
# Historical reports remain unchanged unless their individual generator is updated.
ADVANCE_BATTING_MIN_PA = 10


def apply_advance_batting_pa_cutoff(rows, min_pa=ADVANCE_BATTING_MIN_PA):
    """Classify 10+ PA batters normally; fewer PA as LIMITED unless explicit override.

    Only changes the AVG qualification asterisk and the scouting read where
    qualification requires it. All counting stats, rates and totals are preserved.
    Existing qualified read classifications (including coach overrides) are kept.
    """
    updated = []
    for source in rows:
        r = dict(source)
        if r.get("Team Total"):
            updated.append(r)
            continue
        try:
            pa_text = str(r.get("PA", "")).strip()
            if not pa_text:
                updated.append(r)
                continue
            pa = int(pa_text)
        except (TypeError, ValueError):
            updated.append(r)
            continue

        avg = str(r.get("AVG", "")).strip()
        if avg:
            if pa >= min_pa:
                if avg.endswith("*"):
                    r["AVG"] = avg[:-1]
            elif not avg.endswith("*"):
                r["AVG"] = avg + "*"

        read = str(r.get("Scouting Read", "")).strip().upper()
        if pa < min_pa and read != "LIMITED" and not r.get("ScoutingOverride"):
            r["Scouting Read"] = "LIMITED"
        elif pa >= min_pa and read == "LIMITED":
            ops = _ops_score(r)
            if ops != -inf:
                r["Scouting Read"] = "THREAT" if ops >= 0.90 else "CAUTION" if ops >= 0.68 else "ATTACK"
        updated.append(r)
    return updated

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
