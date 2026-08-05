#!/usr/bin/env python3
"""Build the daily project review from local vault data + a Todoist JSON dump.

This script never talks to Todoist or Drive. The agent makes the MCP calls and
writes the results to a JSON file; this reads that file, joins it against
`01 Projects/`, and does the arithmetic that shouldn't be done by eye.

    python3 review.py --remote /tmp/todoist.json
    python3 review.py --remote /tmp/todoist.json --stale-days 21 --out-json /tmp/analysis.json

Expected --remote shape (every key optional except `overview`):

    {
      "overview":  <get-overview response verbatim>,
      "tasks":     [ <task objects from find-tasks, concatenated across calls> ],
      "completed": [ <task objects from find-completed-tasks> ],
      "activity":  [ <event objects from find-activity> ]
    }

Writes a markdown draft to stdout (or --out). The draft contains the line

    <!-- NEXT-ACTION-PROPOSALS -->

which the agent replaces with its own suggestions: choosing a good next action
needs judgement about what the project is actually for, and that isn't
arithmetic. `--out-json` carries the raw material for those suggestions.
"""

from __future__ import annotations

import argparse
import json
import sys
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

PROPOSAL_MARKER = "<!-- NEXT-ACTION-PROPOSALS -->"


def esc(text) -> str:
    """Make a value safe inside a markdown table cell."""
    if text is None:
        return "—"
    return str(text).replace("|", "\\|").replace("\n", " ").strip() or "—"


def build(args) -> tuple[str, dict]:
    vault = Path(args.vault) if args.vault else find_vault_root()
    config = load_config(args.config)
    today = parse_date(args.today) if args.today else today_utc()
    tomorrow = today + timedelta(days=1)
    stale_cutoff = today - timedelta(days=args.stale_days)

    remote = load_remote(args.remote)
    td_projects = flatten_overview(remote["overview"])
    excluded = config.get("excluded_todoist_project_ids") or {}
    parent_ids = domain_parent_ids(config)
    one_offs = one_off_ids(config)

    # ---- Todoist side ---------------------------------------------------
    for pid, node in td_projects.items():
        node.update(resolve_domain(pid, td_projects, config))
        node["is_container"] = bool(node["child_ids"])
        node["is_excluded"] = pid in excluded
        node["is_one_off"] = pid in one_offs

    tasks_by_project: dict[str, list] = defaultdict(list)
    for task in remote["tasks"]:
        if task.get("checked"):
            continue
        pid = task.get("projectId") or task.get("project_id")
        if pid:
            tasks_by_project[pid].append(task)

    # ---- last-signal dates, for the stalled check -----------------------
    signals: dict[str, dict] = defaultdict(dict)
    sources_present = set()

    for task in remote["completed"]:
        pid = task.get("projectId") or task.get("project_id")
        when = parse_date(task.get("completedAt") or task.get("completed_at"))
        if pid and when:
            sources_present.add("completed")
            prev = signals[pid].get("completed")
            signals[pid]["completed"] = when if prev is None else max(prev, when)

    for event in remote["activity"]:
        pid = event.get("parentProjectId") or event.get("projectId") or event.get("project_id")
        when = parse_date(event.get("eventDate") or event.get("event_date"))
        if pid and when:
            sources_present.add("activity")
            signals[pid]["activity"] = max(when, signals[pid].get("activity", when))

    for pid, tasks in tasks_by_project.items():
        for task in tasks:
            when = parse_date(task.get("addedAt") or task.get("added_at"))
            if when:
                sources_present.add("addedAt")
                signals[pid]["added"] = max(when, signals[pid].get("added", when))

    # ---- Obsidian side --------------------------------------------------
    vault_scan = scan_projects(vault, config, args.projects_dir)
    notes_by_todoist: dict[str, list] = defaultdict(list)
    for note in vault_scan["scanned"]:
        if note["todoist_id"]:
            notes_by_todoist[note["todoist_id"]].append(note)

    # ---- classify -------------------------------------------------------
    # `tracked` is what the GTD and stalled checks apply to. One-Off buckets and
    # the human's holding pens are deliberately not in it - they never complete,
    # so calling them out every single morning is noise, not a finding. Their
    # tasks still appear under upcoming and overdue, which is where they matter.
    tracked, containers, skipped, one_off_nodes = [], [], [], []
    for pid, node in td_projects.items():
        if node.get("is_inbox") or pid in parent_ids:
            continue
        if node["is_one_off"]:
            one_off_nodes.append(node)
            continue
        if node["is_excluded"]:
            skipped.append((node, excluded[pid]))
            continue
        if node["is_container"]:
            containers.append(node)
            continue
        tracked.append(node)

    upcoming, overdue = [], []
    for pid, tasks in tasks_by_project.items():
        node = td_projects.get(pid, {"name": "(unknown project)", "domain": None})
        for task in tasks:
            due = parse_date(task_due_date(task))
            if not due:
                continue
            row = {
                "due": due.isoformat(),
                "content": task.get("content"),
                "project": node.get("name"),
                "domain": node.get("domain"),
                "priority": task.get("priority"),
                "recurring": task.get("recurring") or False,
                "task_id": task.get("id"),
            }
            if due < today:
                row["days_overdue"] = (today - due).days
                overdue.append(row)
            elif due in (today, tomorrow):
                row["when"] = "today" if due == today else "tomorrow"
                upcoming.append(row)

    overdue.sort(key=lambda r: (r["due"], r["project"] or "", r["content"] or ""))
    upcoming.sort(key=lambda r: (r["due"], r["domain"] or "zz", r["project"] or ""))

    no_next_action = []
    for node in tracked:
        tasks = tasks_by_project.get(node["id"], [])
        if any(task_due_date(t) for t in tasks):
            continue
        notes = notes_by_todoist.get(node["id"], [])
        no_next_action.append({
            "project": node["name"],
            "todoist_id": node["id"],
            "domain": node["domain"],
            "task_count": len(tasks),
            "note_path": notes[0]["index_path"] if notes else None,
            "note_status": notes[0]["status"] if notes else None,
            "existing_tasks": [
                {"content": t.get("content"), "description": (t.get("description") or "")[:400]}
                for t in tasks[:15]
            ],
        })
    no_next_action.sort(key=lambda r: (r["domain"] or "zz", r["project"] or ""))

    # Pass 1 supplies only due-dated tasks (the cheap sweep). Anything flagged
    # here has no material to propose a next action from until the agent fetches
    # that project's tasks and re-runs.
    undated_included = bool(remote.get("tasks_include_undated"))
    needs_task_fetch = (
        [] if undated_included
        else [{"project": r["project"], "todoist_id": r["todoist_id"]} for r in no_next_action]
    )

    no_action_ids = {r["todoist_id"] for r in no_next_action}
    stalled = []
    for node in tracked:
        dates = signals.get(node["id"], {})
        last = max(dates.values()) if dates else None
        if last and last > stale_cutoff:
            continue
        tasks = tasks_by_project.get(node["id"], [])
        if not tasks and node["id"] in no_action_ids:
            # No tasks came back and no activity did either, so there is no
            # evidence of quiet - only absence of evidence. It is already listed
            # under "no next action" with the same remedy; saying it twice just
            # makes the report longer.
            continue
        dues = sorted(d for d in (parse_date(task_due_date(t)) for t in tasks) if d)
        if dues and dues[-1] >= today:
            continue  # something is still scheduled ahead; not stalled
        notes = notes_by_todoist.get(node["id"], [])
        stalled.append({
            "project": node["name"],
            "todoist_id": node["id"],
            "domain": node["domain"],
            "last_signal": last.isoformat() if last else None,
            "days_quiet": (today - last).days if last else None,
            "open_tasks": len(tasks),
            "latest_due": dues[-1].isoformat() if dues else None,
            "note_path": notes[0]["index_path"] if notes else None,
            "note_status": notes[0]["status"] if notes else None,
        })
    stalled.sort(key=lambda r: (r["days_quiet"] is None, -(r["days_quiet"] or 0)))

    # ---- drift ----------------------------------------------------------
    drift, dangling, unlinked_active = [], [], []
    for note in vault_scan["scanned"]:
        if not note["todoist_id"]:
            if (note["status"] or "").lower() == "active":
                unlinked_active.append(note)
            continue
        node = td_projects.get(note["todoist_id"])
        if node is None:
            dangling.append(note)
            continue
        if note["domain"] and node["domain"] and note["domain"] != node["domain"]:
            drift.append({
                "note": note["index_path"],
                "field": "domain",
                "obsidian": note["domain"],
                "todoist": node["domain"],
                "detail": f"Todoist has it under {node['domain']}",
            })
        if note["domain"] and node["domain"] is None:
            drift.append({
                "note": note["index_path"],
                "field": "domain",
                "obsidian": note["domain"],
                "todoist": None,
                "detail": "Todoist project sits under no domain parent",
            })
        # `status` has no Todoist field; Conventions.md derives it from whether
        # the project has a due-dated task. So "status: active with nothing
        # due-dated" is a contradiction the note can be checked against, not
        # just an unverifiable mirror.
        node_tasks = tasks_by_project.get(note["todoist_id"], [])
        derived = derive_status(any(task_due_date(t) for t in node_tasks))
        conflict = status_conflict(note["status"], derived)
        if conflict:
            drift.append({
                "note": note["index_path"],
                "field": "status",
                "obsidian": note["status"],
                "todoist": derived,
                "detail": conflict,
            })
        if note["name"] != node["name"]:
            drift.append({
                "note": note["index_path"],
                "field": "name",
                "obsidian": note["name"],
                "todoist": node["name"],
                "detail": "bound by URL, but the names differ",
            })

    analysis = {
        "today": today.isoformat(),
        "stale_days": args.stale_days,
        "counts": {
            "todoist_projects_tracked": len(tracked),
            "todoist_containers": len(containers),
            "todoist_excluded": len(skipped),
            "obsidian_project_notes": len(vault_scan["scanned"]),
            "upcoming": len(upcoming),
            "overdue": len(overdue),
            "no_next_action": len(no_next_action),
            "stalled": len(stalled),
            "drift": len(drift),
        },
        "upcoming": upcoming,
        "overdue": overdue,
        "no_next_action": no_next_action,
        "stalled": stalled,
        "drift": drift,
        "dangling_notes": [n["index_path"] for n in dangling],
        "unlinked_active_notes": [n["index_path"] for n in unlinked_active],
        "needs_task_fetch": needs_task_fetch,
        "containers": [{"name": n["name"], "id": n["id"], "domain": n["domain"]} for n in containers],
        "excluded": [{"name": n["name"], "id": n["id"], "reason": why} for n, why in skipped],
        "one_off": [{"name": n["name"], "id": n["id"], "domain": n["domain"]} for n in one_off_nodes],
        "signal_sources": sorted(sources_present),
    }

    return render(analysis, config), analysis


def render(a: dict, config: dict) -> str:
    L: list[str] = []
    add = L.append

    add(f"# Project Review — {a['today']}")
    add("")
    add("**Read-only.** Nothing below has been changed in Todoist, Obsidian, or Drive. "
        "Any next actions are proposals — say the word and they get added.")
    add("")
    c = a["counts"]
    add(f"{c['todoist_projects_tracked']} active Todoist projects · "
        f"{c['upcoming']} due today/tomorrow · {c['overdue']} overdue · "
        f"{c['no_next_action']} with no next action · {c['stalled']} stalled · "
        f"{c['drift']} drift")
    add("")

    # -- Upcoming ---------------------------------------------------------
    add("## Upcoming — today and tomorrow")
    add("")
    if not a["upcoming"]:
        add("Nothing due today or tomorrow.")
    else:
        by_domain: dict = defaultdict(list)
        for row in a["upcoming"]:
            by_domain[row["domain"]].append(row)
        for domain in sorted(by_domain, key=lambda d: (d is None, d or "")):
            label = config["domains"].get(domain, {}).get("label") if domain else None
            add(f"**{label or domain or 'No domain parent'}**")
            add("")
            add("| When | Task | Project | Priority |")
            add("|---|---|---|---|")
            for row in by_domain[domain]:
                rec = " ↻" if row["recurring"] else ""
                add(f"| {esc(row['when'])} | {esc(row['content'])}{rec} | "
                    f"{esc(row['project'])} | {esc(row['priority'])} |")
            add("")
    add("")

    # -- Overdue ----------------------------------------------------------
    add("## Overdue")
    add("")
    if not a["overdue"]:
        add("Nothing overdue.")
    else:
        # A flat list of 40+ rows is not skimmable, so lead with where the
        # backlog is concentrated - that is usually the actual decision - and
        # keep the full oldest-first list below it for whoever wants detail.
        rollup: dict = {}
        for row in a["overdue"]:
            key = (row["domain"], row["project"])
            entry = rollup.setdefault(key, {"count": 0, "oldest": row["due"], "worst": 0})
            entry["count"] += 1
            entry["oldest"] = min(entry["oldest"], row["due"])
            entry["worst"] = max(entry["worst"], row["days_overdue"])
        add(f"{len(a['overdue'])} overdue tasks across {len(rollup)} projects.")
        add("")
        add("| Project | Domain | Overdue | Oldest | Worst |")
        add("|---|---|---|---|---|")
        for (domain, project), entry in sorted(
            rollup.items(), key=lambda kv: (-kv[1]["worst"], -kv[1]["count"])
        ):
            add(f"| {esc(project)} | {esc(domain)} | {entry['count']} | "
                f"{entry['oldest']} | {entry['worst']}d |")
        add("")
        add(f"<details><summary>All {len(a['overdue'])} overdue tasks, oldest first</summary>")
        add("")
        add("| Due | Late | Task | Project | Domain |")
        add("|---|---|---|---|---|")
        for row in a["overdue"]:
            add(f"| {row['due']} | {row['days_overdue']}d | {esc(row['content'])} | "
                f"{esc(row['project'])} | {esc(row['domain'])} |")
        add("")
        add("</details>")
    add("")

    # -- No next action ---------------------------------------------------
    add("## Projects with no next action")
    add("")
    add("The GTD rule in `99 Meta/Conventions.md`: every active Todoist project needs at "
        "least one task with a due date. These have none — each needs a next action, or a "
        "drop to `backlog` / `on-hold`.")
    add("")
    if not a["no_next_action"]:
        add("None — every active project has a due-dated task.")
    elif a["needs_task_fetch"]:
        add("> Second pass needed. These projects have no due-dated task, so nothing about "
            "them came back in the dated sweep. Fetch their tasks and re-run before proposing "
            "anything — proposals invented without looking at the project are worse than none:")
        add("")
        for row in a["needs_task_fetch"]:
            add(f"> - `{row['project']}` — `{row['todoist_id']}`")
        add("")
        add(PROPOSAL_MARKER)
    else:
        add("| Project | Domain | Open tasks | Note |")
        add("|---|---|---|---|")
        for row in a["no_next_action"]:
            add(f"| {esc(row['project'])} | {esc(row['domain'])} | {row['task_count']} | "
                f"{esc(row['note_path'])} |")
        add("")
        add(PROPOSAL_MARKER)
    add("")

    # -- Stalled ----------------------------------------------------------
    add(f"## Stalled — quiet for {a['stale_days']}+ days")
    add("")
    if not a["stalled"]:
        add(f"Nothing has been quiet for {a['stale_days']} days.")
    else:
        add("| Project | Domain | Last signal | Quiet | Open tasks | Note |")
        add("|---|---|---|---|---|---|")
        for row in a["stalled"]:
            quiet = f"{row['days_quiet']}d" if row["days_quiet"] is not None else "no signal"
            add(f"| {esc(row['project'])} | {esc(row['domain'])} | "
                f"{esc(row['last_signal'])} | {quiet} | {row['open_tasks']} | "
                f"{esc(row['note_path'])} |")
        add("")
        add("For each: reschedule the open tasks, break the project into smaller ones, or "
            "drop it to `backlog` / `on-hold`.")
    add("")

    # -- Drift ------------------------------------------------------------
    add("## Drift — Obsidian vs Todoist")
    add("")
    add("Todoist wins on conflict; the fix is always to correct the note.")
    add("")
    if not a["drift"]:
        add("No drift. Every linked note agrees with Todoist.")
    else:
        add("| Note | Field | Obsidian | Todoist | |")
        add("|---|---|---|---|---|")
        for row in a["drift"]:
            add(f"| {esc(row['note'])} | {row['field']} | {esc(row['obsidian'])} | "
                f"{esc(row['todoist'])} | {esc(row['detail'])} |")
    add("")
    if a["dangling_notes"]:
        add(f"**Dangling** — `todoist:` points at a project that no longer exists: "
            + ", ".join(f"`{p}`" for p in a["dangling_notes"]))
        add("")
    if a["unlinked_active_notes"]:
        add(f"**{len(a['unlinked_active_notes'])} active note(s) with no `todoist:` link** — "
            "these aren't projects until they're bound. Run `project-reconcile` for the full picture: "
            + ", ".join(f"`{p}`" for p in a["unlinked_active_notes"]))
        add("")

    # -- What this run could and couldn't see -----------------------------
    add("---")
    add("")
    notes: list[str] = []
    if a["one_off"]:
        notes.append(
            f"{len(a['one_off'])} `One-Off` bucket(s) skipped by rule — they are permanent "
            "buckets, so the GTD and stalled checks don't apply. Their tasks still appear "
            "above under upcoming and overdue."
        )
    if a["containers"]:
        notes.append(
            f"{len(a['containers'])} Todoist project(s) have sub-projects and were treated as "
            "grouping containers, not checked against the GTD rule: "
            + ", ".join(f"`{c['name']}`" for c in a["containers"])
        )
    if a["excluded"]:
        notes.append(
            "Excluded by `_shared/domains.json`: "
            + ", ".join(f"`{e['name']}` ({e['reason']})" for e in a["excluded"])
        )
    sources = a["signal_sources"]
    if "completed" not in sources or "activity" not in sources:
        missing = [s for s in ("completed", "activity") if s not in sources]
        notes.append(
            "Stalled detection ran on a partial signal — no "
            + " or ".join(missing)
            + " data was supplied, so 'quiet' may be overstated."
        )
    notes.append(
        "`status` is derived, not read: archived → `archived`, a due-dated task → `active`, "
        "otherwise `backlog`/`on-hold`. Todoist cannot tell `backlog` from `on-hold`, so "
        "neither is reported as drift against the other."
    )
    for note in notes:
        add(f"- {note}")

    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--remote", required=True, help="JSON file the agent wrote from its MCP calls")
    ap.add_argument("--vault", help="vault root (default: auto-detected)")
    ap.add_argument("--config", help="path to domains.json")
    ap.add_argument("--dir", dest="projects_dir", help="projects folder (default: 01 Projects)")
    ap.add_argument("--today", help="override today's date, YYYY-MM-DD")
    ap.add_argument("--stale-days", type=int, default=14,
                    help="days of silence before a project counts as stalled (default 14)")
    ap.add_argument("--out", help="write the markdown draft here instead of stdout")
    ap.add_argument("--out-json", help="also write the structured analysis here")
    args = ap.parse_args()

    markdown, analysis = build(args)

    if args.out_json:
        Path(args.out_json).write_text(
            json.dumps(analysis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    if args.out:
        Path(args.out).write_text(markdown, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
