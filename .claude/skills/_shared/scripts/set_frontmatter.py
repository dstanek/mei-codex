#!/usr/bin/env python3
"""Set frontmatter fields on a note, leaving everything else byte-for-byte alone.

    python3 set_frontmatter.py NOTE.md --set todoist=https://app.todoist.com/app/project/6ABC
    python3 set_frontmatter.py NOTE.md --set status=backlog --set priority=2
    python3 set_frontmatter.py NOTE.md --set drive= --dry-run

Rewrites only the lines it is told to. An empty value clears the field but keeps
the key, which is what the Project template expects for an unset `drive:`. Keys
that aren't already present are appended just before the closing `---`.

Deliberately line-based rather than a YAML round-trip: re-emitting parsed YAML
would reorder keys, restyle lists, and quote things the vault leaves bare,
producing a huge diff for a one-field change.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("note")
    ap.add_argument("--set", dest="pairs", action="append", required=True,
                    metavar="KEY=VALUE", help="repeatable; empty VALUE clears the field")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    path = Path(args.note)
    if not path.is_file():
        print(f"error: {path} does not exist", file=sys.stderr)
        return 1

    updates = {}
    for pair in args.pairs:
        if "=" not in pair:
            print(f"error: --set needs KEY=VALUE, got {pair!r}", file=sys.stderr)
            return 1
        key, _, value = pair.partition("=")
        updates[key.strip()] = value.strip()

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        print(f"error: {path} has no frontmatter block to edit", file=sys.stderr)
        return 1

    end = next((i for i in range(1, len(lines)) if lines[i].strip() in ("---", "...")), None)
    if end is None:
        print(f"error: {path} frontmatter is never closed", file=sys.stderr)
        return 1

    remaining = dict(updates)
    changed = []
    for index in range(1, end):
        match = re.match(r"^([A-Za-z0-9_-]+)\s*:", lines[index])
        if not match:
            continue
        key = match.group(1)
        if key in remaining:
            value = remaining.pop(key)
            new = f"{key}: {value}\n" if value else f"{key}:\n"
            if lines[index] != new:
                changed.append(f"{key}: {lines[index].partition(':')[2].strip() or '(empty)'} -> {value or '(empty)'}")
                lines[index] = new

    for key, value in remaining.items():
        lines.insert(end, f"{key}: {value}\n" if value else f"{key}:\n")
        end += 1
        changed.append(f"{key}: (added) -> {value or '(empty)'}")

    if not changed:
        print("no change")
        return 0
    if args.dry_run:
        print(f"would update {path}:")
    else:
        path.write_text("".join(lines), encoding="utf-8")
        print(f"updated {path}:")
    for line in changed:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
