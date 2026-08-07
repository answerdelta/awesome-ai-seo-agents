#!/usr/bin/env python3
"""
verify.py — turn agents.csv into a re-verification checklist.

Rows are printed weakest-evidence-first, because the rows most likely to be wrong are the
ones sourced from a vendor marketing page, not the ones sourced from a repository. A list
like this rots from its softest claims outward.

    python verify.py             # every row, weakest evidence first
    python verify.py --stale 60  # only rows not re-checked in the last 60 days
    python verify.py --json      # machine-readable

Exit code 1 if any row is staler than --stale, so it drops into a scheduled job.
No dependencies beyond the standard library.
"""

import argparse
import csv
import datetime as dt
import json
import sys

# How much a source is worth. A repo under the vendor's own org beats anything they wrote
# about themselves; a marketing page is the weakest thing that still counts as evidence.
STRENGTH = {
    "public repo": 3,
    "public repos": 3,
    "public org listing": 3,
    "vendor doc": 2,
    "vendor changelog": 2,
    "vendor page": 1,
}
LABEL = {3: "STRONG", 2: "OK", 1: "WEAK", 0: "UNKNOWN"}


def load(path="agents.csv"):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def age_days(checked, today):
    try:
        return (today - dt.date.fromisoformat(checked)).days
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    ap.add_argument("--csv", default="agents.csv")
    ap.add_argument("--stale", type=int, default=None,
                    help="only show rows older than N days; exit 1 if any")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--today", default=None,
                    help="override today's date (YYYY-MM-DD), for reproducible output")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    rows = []
    for r in load(args.csv):
        strength = STRENGTH.get(r["evidence_type"].strip(), 0)
        rows.append({
            "agent": r["agent"],
            "code_access": r["code_access"],
            "evidence": r["evidence"],
            "evidence_type": r["evidence_type"],
            "strength": strength,
            "label": LABEL[strength],
            "checked": r["checked"],
            "age_days": age_days(r["checked"], today),
        })

    rows.sort(key=lambda x: (x["strength"], -(x["age_days"] or 0)))

    if args.stale is not None:
        rows = [r for r in rows if (r["age_days"] or 0) > args.stale]

    if args.as_json:
        print(json.dumps(rows, indent=2))
    elif not rows:
        print(f"  nothing staler than {args.stale} days. Nice.")
    else:
        for r in rows:
            age = f"{r['age_days']}d" if r["age_days"] is not None else "?"
            print(f"  {r['label']:6} {r['agent']:14} {r['evidence_type']:18} "
                  f"-> {r['evidence']}  ({age} old)")

    return 1 if (args.stale is not None and rows) else 0


if __name__ == "__main__":
    sys.exit(main())
