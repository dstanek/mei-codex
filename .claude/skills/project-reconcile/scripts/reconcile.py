#!/usr/bin/env python3
"""Run the reconciliation procedure and write the report. Read-only.

Implements steps 2, 4, 5 and 6 of `99 Meta/Project Reconciliation.md` - the
join, the classification, and the report. Steps 1 and 3 (collecting Todoist and
Drive) belong to the agent, because MCP tools are not reachable from a
subprocess; the agent writes what it collected to a JSON file and passes it in.

    python3 reconcile.py --remote /tmp/remote.json
    python3 reconcile.py --remote /tmp/remote.json --out "99 Meta/Reports/Reconciliation 2026-08-05.md"

Expected --remote shape (only `overview` is required):

    {
      "overview":       <get-overview response verbatim>,
      "tasks":          [ <task objects from find-tasks> ],
      "completed":      [ <task objects from find-completed-tasks> ],
      "activity":       [ <event objects from find-activity> ],
      "drive_folders":  [ {"id","title","parentId"}, ... from search_files ],
      "drive_scanned":  true
    }

This script never mutates Todoist, Drive, or any note. It writes exactly one
file: the report. Per the procedure, the pass reports and then stops.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared" / "scripts"))
from vaultlib import (  # noqa: E402
    derive_status,
    domain_parent_ids,
    find_vault_root,
    flatten_overview,
    load_config,
    load_remote,
    one_off_ids,
    parse_date,
    resolve_domain,
    scan_projects,
    status_conflict,
    task_due_date,
    today_utc,
)


def esc(text) -> str:
    if text is None:
        return "—"
    return str(text).replace("|", "\\|").replace("\n", " ").strip() or "—"


def normal(name) -> str:
    """Fold a name for *proposing* a binding. Never for asserting one."""
    if not name:
        return ""
    text = unicodedata.normalize("NFKD", str(name)).casefold()
    return re.sub(r"[^a-z0-9]+", "", text)


def build(args):
    vault = Path(args.vault) if args.vault else find_vault_root()
    config = load_config(args.config)
    today = parse_date(args.today) if args.today else today_utc()
    stale_cutoff = today - timedelta(days=args.stale_days)

    remote = load_remote(args.remote)
    td = flatten_overview(remote["overview"])
    domains = config["domains"]
    parent_ids = domain_parent_ids(config)
    one_offs = one_off_ids(config)
    excluded = config.get("excluded_todoist_project_ids") or {}
    # One-Off buckets are skipped by rule (Conventions.md), holding pens by the
    # human's own choice. Both are exempt from the GTD and stalled checks; only
    # the second is a preference, which is why they come from different places.
    skip_checks = set(one_offs) | set(excluded)

    for pid, node in td.items():
        node.update(resolve_domain(pid, td, config))
        node["is_container"] = bool(node["child_ids"])

    tasks_by_project = defaultdict(list)
    for task in remote["tasks"]:
        if task.get("checked"):
            continue
        pid = task.get("projectId") or task.get("project_id")
        if pid:
            tasks_by_project[pid].append(task)

    signals = {}
    have_signals = bool(remote["completed"] or remote["activity"])
    for task in remote["completed"]:
        pid = task.get("projectId") or task.get("project_id")
        when = parse_date(task.get("completedAt") or task.get("completed_at"))
        if pid and when:
            signals[pid] = max(when, signals.get(pid, when))
    for event in remote["activity"]:
        pid = event.get("parentProjectId") or event.get("projectId")
        when = parse_date(event.get("eventDate") or event.get("event_date"))
        if pid and when:
            signals[pid] = max(when, signals.get(pid, when))

    scan = scan_projects(vault, config, args.projects_dir)
    notes = scan["scanned"]
    notes_by_todoist = defaultdict(list)
    for note in notes:
        if note["todoist_id"]:
            notes_by_todoist[note["todoist_id"]].append(note)

    drive = {f["id"]: f for f in remote["drive_folders"] if f.get("id")}
    drive_scanned = bool(remote.get("drive_scanned") or drive)
    undated_included = bool(remote.get("tasks_include_undated"))

    F = {key: [] for key in (
        "dangling", "unlinked", "drift", "no_next_action", "orphan_parent",
        "nesting", "loose_task", "stalled", "name_drift", "structural", "drive",
        "informational", "data", "duplicate_binding",
    )}

    # -- structural (Obsidian) -------------------------------------------
    for item in scan["structural"]:
        F["structural"].append({
            "finding": "Structural",
            "subject": item["path"],
            "detail": item["detail"],
            "action": "Reshape to `{Name}/{Name}.md` per Conventions.md",
        })

    for note in notes:
        for problem in note["problems"]:
            F["data"].append({
                "subject": note["index_path"],
                "detail": problem,
                "action": "Correct the frontmatter",
            })

    # -- bindings ---------------------------------------------------------
    for tid, group in notes_by_todoist.items():
        if len(group) > 1:
            F["duplicate_binding"].append({
                "finding": "Duplicate binding",
                "subject": ", ".join(f"`{n['index_path']}`" for n in group),
                "detail": f"{len(group)} notes share `todoist:` {tid}",
                "action": "One project, one note — merge or repoint",
            })

    unbound_projects = {}
    for pid, node in td.items():
        if node.get("is_inbox") or pid in parent_ids:
            continue
        if not notes_by_todoist.get(pid):
            unbound_projects[normal(node["name"])] = node

    for note in notes:
        if not note["todoist_url"]:
            proposal = unbound_projects.get(normal(note["name"]))
            F["unlinked"].append({
                "finding": "Unlinked note",
                "subject": note["index_path"],
                "detail": f"status `{note['status'] or 'unset'}`, no `todoist:` at all",
                "action": (
                    f"**Proposed** binding to Todoist `{proposal['name']}` "
                    f"({proposal['id']}) — name match only, confirm before writing"
                    if proposal else
                    "Create the Todoist project, or move the note out of `01 Projects/` — "
                    "without a Todoist project it is an idea, not a project"
                ),
            })
            continue

        if not note["todoist_id"]:
            continue  # already reported as a data problem
        node = td.get(note["todoist_id"])
        if node is None:
            F["dangling"].append({
                "finding": "Dangling note",
                "subject": note["index_path"],
                "detail": f"`todoist:` {note['todoist_id']} resolves to no live project",
                "action": "Archive the note, or repoint it at the right project",
            })
            continue

        if note["name"] != node["name"]:
            F["name_drift"].append({
                "finding": "Name drift",
                "subject": note["index_path"],
                "detail": f"Obsidian `{note['name']}` vs Todoist `{node['name']}`",
                "action": "Pick the canonical short name; rename the other",
            })
        if note["domain"] and node["domain"] and note["domain"] != node["domain"]:
            F["drift"].append({
                "finding": "Status drift",
                "subject": note["index_path"],
                "detail": f"`domain: {note['domain']}` vs Todoist parent `{node['domain']}`",
                "action": f"Sync the note to `domain: {node['domain']}` — Todoist wins",
            })
        elif note["domain"] and node["domain"] is None:
            F["drift"].append({
                "finding": "Status drift",
                "subject": note["index_path"],
                "detail": f"`domain: {note['domain']}` but the Todoist project has no domain parent",
                "action": "Move the Todoist project under the right domain parent",
            })
        # `status` is derived from Todoist state, not read from a field that
        # doesn't exist. So it can genuinely be checked: a note claiming
        # `active` while Todoist has nothing due-dated is the GTD rule restated.
        note_tasks = tasks_by_project.get(note["todoist_id"], [])
        derived = derive_status(any(task_due_date(t) for t in note_tasks))
        conflict = status_conflict(note["status"], derived)
        if conflict:
            if derived == "archived" or (note["status"] or "").lower() == "archived":
                action = (f"Archive in Todoist, or correct the note — and move it to "
                          f"`{config['paths']['archive_projects_dir']}/`")
            elif derived == "active":
                action = "Sync the note to `status: active`"
            else:
                action = ("Add a due-dated next action, or set the note to `backlog` / "
                          "`on-hold` — whichever is true")
            F["drift"].append({
                "finding": "Status drift",
                "subject": note["index_path"],
                "detail": conflict,
                "action": action,
            })

    # -- Todoist structure -------------------------------------------------
    for pid, node in td.items():
        if node.get("is_inbox") or pid in parent_ids:
            continue
        if node["domain"] is None:
            F["orphan_parent"].append({
                "finding": "Orphan parent",
                "subject": f"`{node['name']}` ({pid})",
                "detail": "top level, and not one of the seven domain parents",
                "action": "Move under the domain parent it belongs to",
            })
        elif node["depth"] and node["depth"] > 1:
            chain = " › ".join(td[c]["name"] for c in reversed(node["chain"]) if c in td)
            F["nesting"].append({
                "finding": "Orphan parent",
                "subject": f"`{node['name']}` ({pid})",
                "detail": f"{node['depth']} levels deep: {chain} › {node['name']}",
                "action": f"Move directly under `{domains[node['domain']]['label']}` — "
                          "the invariant is one level",
            })

    for domain, meta in domains.items():
        if meta["todoist_parent_id"] not in td:
            F["orphan_parent"].append({
                "finding": "Orphan parent",
                "subject": f"domain `{domain}`",
                "detail": f"parent project {meta['todoist_parent_id']} is not in the overview",
                "action": "Recreate the domain parent, or fix the ID in `_shared/domains.json`",
            })

    # -- Loose tasks -------------------------------------------------------
    # A domain parent holds no tasks directly. Where a loose task belongs
    # depends on what kind of task it is, and lumping the three kinds together
    # would produce a single wrong instruction for 51 rows, so they stay apart.
    project_by_name = {
        normal(n["name"]): n for pid, n in td.items()
        if not n.get("is_inbox") and pid not in parent_ids and pid not in one_offs
    }
    loose_by_domain = defaultdict(lambda: {"one_off": [], "recurring": [], "owned": []})
    for pid, domain in parent_ids.items():
        for task in tasks_by_project.get(pid, []):
            content = (task.get("content") or "").strip()
            bucket = loose_by_domain[domain]
            if task.get("recurring"):
                bucket["recurring"].append(content)
                continue
            prefix = content.split(":", 1)[0].strip() if ":" in content else ""
            owner = project_by_name.get(normal(prefix)) if prefix else None
            if owner:
                bucket["owned"].append((content, owner))
            else:
                bucket["one_off"].append(content)

    def sample(items, limit=4):
        shown = ", ".join(f"`{c}`" for c in items[:limit])
        return shown + (f", +{len(items) - limit} more" if len(items) > limit else "")

    def plural(count, noun):
        return f"{count} {noun}" if count == 1 else f"{count} {noun}s"

    for domain, bucket in sorted(loose_by_domain.items()):
        label = domains[domain]["label"]
        one_off_id = domains[domain].get("one_off_project_id")
        if bucket["one_off"]:
            F["loose_task"].append({
                "finding": "Loose task",
                "subject": f"`{label}` — " + plural(len(bucket["one_off"]), "one-off task"),
                "detail": sample(bucket["one_off"]),
                "action": f"Move to `{label} › One-Off` (`{one_off_id}`)",
            })
        for content, owner in bucket["owned"]:
            F["loose_task"].append({
                "finding": "Loose task",
                "subject": f"`{label}` — `{content}`",
                "detail": f"prefixed with a real project name, `{owner['name']}`",
                "action": f"Move to `{owner['name']}` (`{owner['id']}`), **not** One-Off",
            })
        if bucket["recurring"]:
            F["loose_task"].append({
                "finding": "Loose task",
                "subject": f"`{label}` — " + plural(len(bucket["recurring"]), "recurring task"),
                "detail": sample(bucket["recurring"]),
                "action": "Leave in the domain's `Recurring Tasks` section — a repeating "
                          "task is not one-off. Listed so the count reconciles",
            })

    # -- GTD + stalled -----------------------------------------------------
    for pid, node in td.items():
        if node.get("is_inbox") or pid in parent_ids or node["is_container"]:
            continue
        if pid in skip_checks:
            continue
        tasks = tasks_by_project.get(pid, [])
        dues = sorted(d for d in (parse_date(task_due_date(t)) for t in tasks) if d)
        note = (notes_by_todoist.get(pid) or [None])[0]
        where = f" — note `{note['index_path']}`" if note else ""

        if not dues:
            count = (
                f"{len(tasks)} open task(s)" if undated_included
                else (f"{len(tasks)} due-dated task(s) came back; undated tasks were not collected"
                      if tasks else "no due-dated tasks; undated tasks were not collected")
            )
            F["no_next_action"].append({
                "finding": "No next action",
                "subject": f"`{node['name']}` ({pid})",
                "detail": f"{count}, none due-dated{where}",
                "action": "Add a due-dated next action, or drop to `backlog` / `on-hold`",
            })

        # "Stalled" per Project Reconciliation.md means tasks that are all *long*
        # overdue, or untouched. A task that slipped three days is overdue, not
        # stalled - it is already reported as overdue and does not need a second,
        # scarier label.
        last = signals.get(pid)
        untouched = have_signals and (last is None or last <= stale_cutoff)
        all_long_overdue = bool(dues) and dues[-1] <= stale_cutoff
        if tasks and (all_long_overdue or (not dues and untouched)):
            F["stalled"].append({
                "finding": "Stalled project",
                "subject": f"`{node['name']}` ({pid})",
                "detail": (
                    f"latest due {dues[-1].isoformat()}" if dues else "no dated tasks"
                ) + (
                    f", last touched {last.isoformat()}" if last
                    else f", nothing in the last {args.stale_days} days of activity"
                ) + f", {len(tasks)} open{where}",
                "action": "Reschedule, break it down, or drop out of active",
            })

    # -- Drive -------------------------------------------------------------
    if drive_scanned:
        root_id = config["drive"]["projects_root_id"]
        domain_folder_ids = {m["drive_folder_id"]: k for k, m in domains.items()}
        seen_domain_ids = {f["id"] for f in drive.values()
                           if f.get("parentId") == root_id and f["id"] in domain_folder_ids}
        for domain, meta in domains.items():
            if meta["drive_folder_id"] not in seen_domain_ids and drive:
                F["drive"].append({
                    "finding": "Drive",
                    "subject": f"`1. Projects/{meta['label']}/`",
                    "detail": f"domain folder {meta['drive_folder_id']} not found under `1. Projects/`",
                    "action": "Create it, or fix the ID in `_shared/domains.json`",
                })

        for folder in drive.values():
            if folder.get("parentId") == root_id and folder["id"] not in domain_folder_ids:
                F["drive"].append({
                    "finding": "Drive",
                    "subject": f"`{folder.get('title')}` ({folder['id']})",
                    "detail": "project folder sitting at the `1. Projects/` root",
                    "action": "**By hand** — move it under its domain folder. The connector "
                              "cannot move, rename, or delete",
                })

        for note in notes:
            if not note["drive_id"]:
                continue
            folder = drive.get(note["drive_id"])
            if folder is None:
                F["drive"].append({
                    "finding": "Drive",
                    "subject": note["index_path"],
                    "detail": f"`drive:` {note['drive_id']} was not found in the scanned tree",
                    "action": "The folder may live outside `1. Projects/` — an existing folder "
                              "stays valid wherever it sits. Confirm it still exists",
                })
                continue
            expected = domains.get(note["domain"], {}).get("drive_folder_id")
            if expected and folder.get("parentId") not in (expected, None):
                F["drive"].append({
                    "finding": "Drive",
                    "subject": note["index_path"],
                    "detail": f"folder `{folder.get('title')}` is not under "
                              f"`1. Projects/{domains[note['domain']]['label']}/`",
                    "action": "**By hand**, and only if you want the path tidy — the URL binding "
                              "is already correct",
                })

    # -- informational -----------------------------------------------------
    bound_note_names = {normal(n["name"]) for n in notes}
    for pid, node in td.items():
        if node.get("is_inbox") or pid in parent_ids or node["is_container"]:
            continue
        if pid in one_offs:
            continue  # One-Off never gets a note or a folder; not "missing" one
        if notes_by_todoist.get(pid):
            continue
        hint = " (a note of the same name exists but is unbound)" if normal(node["name"]) in bound_note_names else ""
        F["informational"].append({
            "subject": f"`{node['name']}`",
            "detail": f"no Obsidian note{hint}",
        })

    counts = {
        "todoist_projects": sum(1 for p, n in td.items()
                                if not n.get("is_inbox") and p not in parent_ids),
        "obsidian_notes": len(notes),
        "bound": sum(1 for n in notes if n["todoist_id"] and n["todoist_id"] in td),
        "drive_folders": len(drive),
    }
    return render(F, counts, config, today, args, scan, drive_scanned,
                  have_signals, undated_included), F


SECTIONS = [
    ("1", "Bindings", ["dangling", "unlinked", "duplicate_binding"],
     "An Obsidian note pointing at a Todoist project that no longer exists is an error. "
     "A Todoist project with no note is not."),
    ("2", "Drift", ["drift", "name_drift"],
     "`status` and `domain` are mirrors of Todoist. **Todoist wins** — every fix below "
     "changes the note, never Todoist."),
    ("3", "GTD rule — active projects need a due-dated task", ["no_next_action"], None),
    ("4", "Stalled", ["stalled"], None),
    ("5", "Todoist structure", ["orphan_parent", "nesting"],
     "Every project sits directly under the parent matching its domain. Only the domain "
     "parents themselves live at top level."),
    ("6", "Loose tasks", ["loose_task"],
     "A domain parent holds no tasks directly. Each goes to its owning project, or to that "
     "domain's `One-Off` — except recurring tasks, which stay in `Recurring Tasks`."),
    ("7", "Obsidian structure", ["structural"],
     "Every project in `01 Projects/` is a directory containing an index note of the same name."),
    ("8", "Drive", ["drive"],
     "The connector can **create** folders but cannot move, rename, or delete them. "
     "Anything marked *by hand* has to be done in the Drive UI."),
    ("9", "Frontmatter", ["data"], None),
]


def render(F, counts, config, today, args, scan, drive_scanned,
           have_signals, undated_included) -> str:
    L: list[str] = []
    add = L.append
    total = sum(len(F[k]) for k in F if k != "informational")

    add("---")
    add("type: meta")
    add(f"created: {today.isoformat()}")
    add("---")
    add(f"# Reconciliation Report — {today.isoformat()}")
    add("")
    add("Run under [[Project Reconciliation]]. **Nothing has been changed.** "
        "Every item below is a proposal awaiting approval.")
    add("")
    sources = [
        f"{counts['obsidian_notes']} notes under `{scan['projects_dir']}/`",
        f"`get-overview` ({counts['todoist_projects']} Todoist projects)",
    ]
    sources.append(
        f"Drive `1. Projects/` (`{config['drive']['projects_root_id']}`, "
        f"{counts['drive_folders']} folders)" if drive_scanned else "**Drive was not scanned**"
    )
    add("Sources: " + ", ".join(sources) + ".")
    add("")

    add("## Summary")
    add("")
    add("| | Count |")
    add("|---|---|")
    add(f"| Todoist projects | {counts['todoist_projects']} |")
    add(f"| Obsidian project notes | {counts['obsidian_notes']} |")
    add(f"| …bound to a live Todoist project | **{counts['bound']}** |")
    for number, title, keys, _ in SECTIONS:
        n = sum(len(F[k]) for k in keys)
        add(f"| §{number} {title} | {'**' + str(n) + '**' if n else '0'} |")
    add(f"| **Actionable findings** | **{total}** |")
    add("")
    if total == 0:
        add("A clean run. Every invariant in [[Project Reconciliation]] holds.")
        add("")

    for number, title, keys, blurb in SECTIONS:
        rows = [r for k in keys for r in F[k]]
        add("---")
        add("")
        add(f"## {number}. {title}")
        add("")
        if blurb:
            add(f"> {blurb}")
            add("")
        if not rows:
            add("Clean — nothing to do.")
            add("")
            continue
        add("| # | Finding | Subject | Detail | Proposed action |")
        add("|---|---|---|---|---|")
        for index, row in enumerate(rows, 1):
            add(f"| {number}.{index} | {esc(row.get('finding', title))} | {esc(row['subject'])} "
                f"| {esc(row['detail'])} | {esc(row['action'])} |")
        add("")

    add("---")
    add("")
    add("## 10. Informational — no action")
    add("")
    add("Todoist projects with no Obsidian note. **Allowed by the contract** — Obsidian and "
        "Drive are optional supporting material. `One-Off` buckets are not listed: they never "
        "get a note or a folder, so they are not missing one.")
    add("")
    if F["informational"]:
        add(", ".join(f"{r['subject']}" + (r["detail"].replace("no Obsidian note", ""))
                      for r in F["informational"]))
    else:
        add("Every Todoist project has an Obsidian note.")
    add("")

    add("---")
    add("")
    add("> **Stop here.** This pass reports; it does not fix. Apply changes only after the "
        "report is reviewed.")
    add("")
    caveats = [
        "Bindings are by URL. Anything labelled *proposed* came from a name match and must be "
        "confirmed by a human before it is written anywhere.",
        "`status` is derived from Todoist state, not read from a field: archived → "
        "`archived`, a due-dated task → `active`, otherwise `backlog`/`on-hold`. Todoist "
        "cannot distinguish `backlog` from `on-hold`, so neither is drift against the other.",
        "`One-Off` buckets are skipped by rule in §3, §4 and §10 — they are permanent "
        "buckets that never complete.",
    ]
    if not drive_scanned:
        caveats.append("Drive was not collected, so §7 is empty by omission, not by cleanliness.")
    if not have_signals:
        caveats.append("No completion or activity data was supplied, so §4 rests on due dates alone.")
    if not undated_included:
        caveats.append(
            "Only due-dated tasks were collected, so §3 cannot tell an empty project from one "
            "whose tasks are all undated. Collect the `no date` sweep too for a full pass."
        )
    excluded = config.get("excluded_todoist_project_ids") or {}
    if excluded:
        caveats.append(
            "Excluded from §3 and §4 by `_shared/domains.json`: "
            + ", ".join(f"`{pid}` ({why})" for pid, why in excluded.items())
        )
    caveats.append(f"Stalled threshold: {args.stale_days} days.")
    for line in caveats:
        add(f"- {line}")

    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--remote", required=True, help="JSON the agent wrote from its MCP calls")
    ap.add_argument("--vault", help="vault root (default: auto-detected)")
    ap.add_argument("--config", help="path to domains.json")
    ap.add_argument("--dir", dest="projects_dir", help="projects folder (default: 01 Projects)")
    ap.add_argument("--today", help="override today's date, YYYY-MM-DD")
    ap.add_argument("--stale-days", type=int, default=14)
    ap.add_argument("--out", help="report path; default 99 Meta/Reports/Reconciliation <today>.md")
    ap.add_argument("--stdout", action="store_true", help="print instead of writing the report")
    args = ap.parse_args()

    markdown, _ = build(args)
    if args.stdout:
        sys.stdout.write(markdown)
        return 0

    vault = Path(args.vault) if args.vault else find_vault_root()
    config = load_config(args.config)
    today = parse_date(args.today) if args.today else today_utc()
    out = Path(args.out) if args.out else (
        vault / config["paths"]["reports_dir"] / f"Reconciliation {today.isoformat()}.md"
    )
    if not out.is_absolute():
        out = vault / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
