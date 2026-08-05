#!/usr/bin/env python3
"""Create `01 Projects/{Name}/{Name}.md` from the vault's Project template.

    python3 new_project_note.py --check --name "Kitchen Remodel" --domain personal
    python3 new_project_note.py --name "Kitchen Remodel" --domain personal \
        --todoist https://app.todoist.com/app/project/6ABC --priority 2

`--check` validates and prints what it would do without touching disk. Run it
before creating the Todoist project, so a bad name or a collision surfaces
before anything exists anywhere.

The note is rendered from `99 Meta/Templates/Project.md` rather than from a copy
kept here. Templater's `<% ... %>` expressions only expand inside Obsidian, so
this resolves the ones it recognises (`tp.file.title`, `tp.file.creation_date`)
and fills the frontmatter by key - which means the template can be reworded or
reordered without breaking this script.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared" / "scripts"))
from vaultlib import find_vault_root, load_config, url_id  # noqa: E402

TEMPLATER = re.compile(r"<%[-_]?\s*(.*?)\s*[-_]?%>", re.DOTALL)


def render_template(raw: str, values: dict, now: datetime) -> tuple[str, list[str]]:
    """Resolve the Templater expressions we understand; report the rest."""
    leftovers: list[str] = []

    def resolve(match: re.Match) -> str:
        expr = match.group(1)
        if "tp.file.title" in expr:
            return values["title"]
        fmt = re.search(r"tp\.file\.creation_date\(\s*['\"](.+?)['\"]\s*\)", expr)
        if fmt:
            return now.strftime(
                fmt.group(1).replace("YYYY", "%Y").replace("MM", "%m")
                .replace("DD", "%d").replace("HH", "%H").replace("mm", "%M")
            )
        if "tp.system.suggester" in expr:
            return ""      # frontmatter values are set by key below
        leftovers.append(expr.strip()[:80])
        return ""

    text = TEMPLATER.sub(resolve, raw)

    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == "---":
        end = next((i for i in range(1, len(lines)) if lines[i].strip() in ("---", "...")), None)
        if end is not None:
            remaining = dict(values)
            for index in range(1, end):
                key_match = re.match(r"^([A-Za-z0-9_-]+)\s*:", lines[index])
                if key_match and key_match.group(1) in remaining:
                    key = key_match.group(1)
                    value = remaining.pop(key)
                    lines[index] = f"{key}: {value}\n" if value not in (None, "") else f"{key}:\n"
            for key, value in remaining.items():
                if value in (None, ""):
                    continue
                lines.insert(end, f"{key}: {value}\n")
                end += 1
            text = "".join(lines)

    return text, leftovers


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="canonical short name, reused across all three systems")
    ap.add_argument("--domain", required=True)
    ap.add_argument("--status", default="active")
    ap.add_argument("--priority", help="1-4; omitted means unset, which is fine")
    ap.add_argument("--todoist", help="full Todoist project URL")
    ap.add_argument("--drive", help="full Drive folder URL")
    ap.add_argument("--vault")
    ap.add_argument("--config")
    ap.add_argument("--check", action="store_true", help="validate only; write nothing")
    args = ap.parse_args()

    vault = Path(args.vault) if args.vault else find_vault_root()
    config = load_config(args.config)
    paths = config["paths"]

    problems: list[str] = []
    warnings: list[str] = []

    name = args.name.strip()
    if not name:
        problems.append("name is empty")
    if name != args.name:
        warnings.append("name had surrounding whitespace; using the trimmed form")
    for bad in "/\\:":
        if bad in name:
            problems.append(f"name contains {bad!r}, which cannot be a folder name")
    if name.startswith("."):
        problems.append("name starts with a dot; Obsidian will hide the folder")

    if args.domain not in config["domains"]:
        problems.append(
            f"domain {args.domain!r} is not one of the seven: " + ", ".join(config["domains"])
        )
    if args.status not in config["statuses"]:
        problems.append(
            f"status {args.status!r} is not one of: " + ", ".join(config["statuses"])
        )
    if args.priority and args.priority not in ("1", "2", "3", "4"):
        problems.append(f"priority {args.priority!r} is not 1-4")

    if args.todoist and not url_id(args.todoist):
        problems.append(f"--todoist is not a usable URL: {args.todoist!r}")
    if args.drive and not url_id(args.drive):
        problems.append(f"--drive is not a usable URL: {args.drive!r}")
    if not args.todoist and not args.check:
        problems.append(
            "no --todoist URL. Conventions.md makes it required on every project note - "
            "create the Todoist project first, then pass its URL"
        )
    if args.status == "active" and not args.todoist:
        warnings.append("an `active` project also needs a due-dated next action in Todoist "
                        "(the GTD rule), which this script does not create")

    target_dir = vault / paths["projects_dir"] / name
    target = target_dir / f"{name}.md"
    if target.exists():
        problems.append(f"{target.relative_to(vault)} already exists")
    elif target_dir.exists():
        warnings.append(f"{target_dir.relative_to(vault)} already exists; adding the index note to it")

    projects_root = vault / paths["projects_dir"]
    if projects_root.is_dir():
        folded = name.casefold()
        for sibling in projects_root.iterdir():
            if sibling.name.casefold() == folded and sibling.name != name:
                problems.append(
                    f"{sibling.name!r} already exists and differs only by case - "
                    "pick one canonical short name"
                )

    template_path = vault / paths["project_template"]
    if not template_path.is_file():
        problems.append(f"template not found: {template_path}")

    if problems:
        print("cannot create:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        for warning in warnings:
            print(f"  ~ {warning}", file=sys.stderr)
        return 1

    now = datetime.now()
    values = {
        "title": name,
        "type": "project",
        "status": args.status,
        "domain": args.domain,
        "priority": args.priority or "",
        "created": now.strftime("%Y-%m-%d %H:%M"),
        "todoist": args.todoist or "",
        "drive": args.drive or "",
    }
    body, leftovers = render_template(
        template_path.read_text(encoding="utf-8"), values, now
    )
    for expr in leftovers:
        warnings.append(f"template expression left unresolved: <% {expr} %>")

    meta = config["domains"][args.domain]
    if args.check:
        print(f"would create {target.relative_to(vault)}")
        print(f"  domain {args.domain} -> Todoist parent {meta['todoist_parent_id']}, "
              f"Drive folder {meta['drive_folder_id']}")
        print(f"  status {args.status}, priority {args.priority or '(unset)'}")
        print(f"  todoist {args.todoist or '(none yet)'}")
        print(f"  drive   {args.drive or '(none yet)'}")
    else:
        target_dir.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        print(f"created {target.relative_to(vault)}")

    for warning in warnings:
        print(f"  ~ {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
