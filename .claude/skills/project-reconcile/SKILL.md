---
name: project-reconcile
description: Reconcile projects across Todoist, the Obsidian vault, and Google Drive, then write a dated report to 99 Meta/Reports/ and stop. Finds dangling notes whose todoist link is dead, unlinked notes with no todoist URL, status and domain drift between Obsidian and Todoist, active projects with no due-dated next action, orphan Todoist projects not under a domain parent, loose tasks sitting directly in a domain parent instead of a project or its One-Off, stalled projects, name drift across systems, and structural violations in 01 Projects/. Use this whenever the user wants to check whether the three systems are in sync, asks if anything is out of sync or missing or orphaned or duplicated, mentions reconciliation or an audit or a weekly or Sunday review of projects, wonders whether a note or Drive folder still matches Todoist, or wants to clean up or tidy the project structure. Strictly read-only - it reports and stops, and never fixes anything.
---

# Reconcile the three systems

Implements the procedure in `99 Meta/Project Reconciliation.md`. **Read that
note before running** — it defines the invariants, the finding taxonomy, and
what each remedy is. This skill is the mechanics; that note is the meaning.

Also read `.claude/skills/_shared/REFERENCE.md` for the domain IDs, the
agent/script split, and the remote JSON envelope.

## Read-only, and it stops

The pass reports; it does not fix. It writes exactly one file — the report — and
then stops. Do not apply anything, not even the items marked mechanical, until
the user has read the report and said go. If they then say go, that's a separate
piece of work; come back to the report and work down it.

## Procedure

Steps 1 and 3 are yours because scripts can't reach MCP. Steps 2, 4, 5 and 6 are
the script's.

### 1. Todoist

```
mcp__todoist__get-overview                          (no arguments)
mcp__todoist__find-tasks   filter: "!no date"       (paginate on cursor)
mcp__todoist__find-tasks   filter: "no date"        (paginate on cursor)
mcp__todoist__find-completed-tasks  since: <today minus stale-days>
mcp__todoist__find-activity  objectType: "task", dateFrom: <today minus stale-days>
```

Unlike the daily review, this pass **does** want the `no date` sweep. It's
expensive, but without it the report can't tell an empty project from one whose
tasks are all undated, and those need different remedies. Set
`"tasks_include_undated": true` in the envelope once you've collected it.

Project Reconciliation.md gives the GTD check as a per-project
`filter: "##<Project Name> & !no date"`. The two sweeps above answer the same
question for every project at once; fall back to the per-project form only if a
sweep fails or a name is ambiguous.

### 2. Drive

```
mcp__claude_ai_Google_Drive__search_files   query: "parentId = '14Kt3GswyG0moflC5iLEG769Rov879PiA'"
```

Then one query per domain subfolder — you can `or` several `parentId` clauses
into a single query. Collect `{id, title, parentId}` for every folder into
`drive_folders`, and set `"drive_scanned": true`.

If Drive is unavailable, carry on without it. The report will say Drive wasn't
scanned rather than implying it was clean — but say so to the user too, since a
partial pass shouldn't be mistaken for a clean one.

### 3. Run it

```bash
python3 .claude/skills/project-reconcile/scripts/reconcile.py --remote /tmp/remote.json
```

This walks `01 Projects/`, joins everything by URL, classifies against the table
in Project Reconciliation.md, and writes
`99 Meta/Reports/Reconciliation YYYY-MM-DD.md` in the shape of the existing
reports. Use `--stdout` to preview without writing, `--stale-days N` to change
the stalled threshold, `--out PATH` for a different destination.

Re-running on the same day overwrites that day's report. Check whether one
already exists before running and mention it if so.

### 4. Hand it over

Summarise in the conversation: the counts, the two or three findings that
actually matter, and anything genuinely blocking. Link the report path. Don't
paste the whole report back — it's a file, and the point of writing it is that
it can be read at leisure.

Then stop.

## Binding by URL, never by name

The report's proposed bindings come from name matches, and every one is labelled
*proposed*. Names drift; IDs don't. Never write a `todoist:` or `drive:` URL
into a note because the names looked the same — surface it as a question and let
the user confirm. This is the rule most likely to be quietly broken while
"being helpful", and breaking it silently binds a note to the wrong project.

## What the report can't decide for itself

Add a short **Decisions needed** section when the run turns up things only the
user can settle, in rough priority order. Look for:

- **Ambiguous bindings** — a name match that could plausibly be two projects, or
  a note and project whose names differ enough that either could be canonical.
- **Container-or-project** — a directory holding several distinct projects, or a
  Todoist project acting as a grouping bucket. Lay out the options; don't pick.
- **Orphan domains** — a top-level Todoist project whose domain isn't inferable.
  Ask; don't guess and don't leave it unmentioned.
- **Deletions and Drive moves** — always the user's call. Drive moves in
  particular have to be done by hand, and aren't reversible by URL.

Say what you'd choose and why, then leave the choice with them.

## Loose tasks

A domain parent holds no tasks directly — §6 of the report. The finding splits
into three kinds, because they have three different remedies and collapsing them
would give one wrong instruction for dozens of rows:

- **Prefixed `{Project}: {task}`** → belongs in that named project, *not*
  One-Off. The script matches the prefix against real project names and names
  the target.
- **Recurring** → stays in the domain's `Recurring Tasks` section. A repeating
  task is by definition not one-off. Listed only so the count reconciles; never
  propose moving these.
- **Everything else** → that domain's `One-Off`, grouped with a sample.

If the user says go, `mcp__todoist__update-tasks` with a `projectId` moves a
task. Don't use it to touch dates — `reschedule-tasks` exists because
`update-tasks` destroys recurrence.

## Interpretation notes

All are in the report's footnotes; repeat them if a finding surprises the user.

- **`status` is derived, not read.** Archived → `archived`, a due-dated task →
  `active`, otherwise `backlog`/`on-hold`. That makes `status: active` with
  nothing due-dated a reportable contradiction — the GTD rule restated. Todoist
  can't distinguish `backlog` from `on-hold`, so neither is drift against the
  other.
- **`One-Off` buckets are skipped by rule** in the GTD, stalled, and
  missing-note sections. They never complete and never get a note or folder, so
  they aren't missing one.
- **Holding pens** are skipped only because they're in
  `excluded_todoist_project_ids`. Offer to add a new one; don't edit the file
  unless the user agrees. A clean run is the goal state — a permanently noisy
  report means the invariants or the process need fixing, not tolerating.

## Related

- Daily "what's on my plate" → `project-review`
- Creating something the report says is missing → `project-new`
