---
type: meta
---
# Project Reconciliation

How to check that active projects line up across Obsidian, Todoist, and Google Drive — and what to do when they don't.

For naming, domains, and frontmatter, see [[Conventions]].

## The Three-System Contract

| System | Owns | Holds |
|--------|------|-------|
| **Obsidian** | Existence, canonical name, `status`, `domain` | Support material I *write* |
| **Todoist** | Tasks and next actions | Nothing else |
| **Google Drive** | — | Support material I *download* |

> **Obsidian is authoritative.** Every active Obsidian project must have a Todoist project and a Drive folder. The reverse is not required — Todoist and Drive may hold things that never became Obsidian projects, and that is not a violation.

## Why the Three Trees Differ

PARA is a *lifecycle* taxonomy (project / area / resource / archive). Domain is *orthogonal* to it. Encoding both in one folder tree forces a bad choice: domain-first duplicates PARA once per domain and fragments Areas; lifecycle-first dumps every domain into one bucket.

Because a project note carries explicit `todoist:` and `drive:` URLs, **binding is by link, not by path** — so the trees don't need to match. Each system groups by the dimension it is actually good at:

| System | Native strength | Groups by |
|--------|-----------------|-----------|
| Obsidian | Frontmatter + Dataview — real facets | **Lifecycle.** Flat `01 Projects/`; domain lives in `domain:` |
| Todoist | Parent-project nesting only; no project-level metadata | **Domain.** One parent project per domain |
| Drive | Folders only — no query, no metadata | **Domain.** `1. Projects/{Domain}/` |

Do not add domain folders to `01 Projects/`. Dataview already gives you per-domain views, and the Dashboard uses them.

Drive's roots `5. Preheat to 350`, `6. Paige Stanek`, `7. Learn Fast`, and `8. Cabinet` are **Areas**, not Projects — they hold evergreen per-focus material (`Graphics`, `Videos`, `logos`, `shopify`). Project-scoped downloads belong under `1. Projects/{Domain}/`.

## Invariants

> Every project in `01 Projects/` with `status: active` has both a `todoist` URL and a `drive` URL in its index note's frontmatter.

> Every project with `status: active` has at least one task with a due date in Todoist. *(the GTD rule from [[Conventions]])*

> A project's Todoist project sits directly under the parent matching its `domain`, and its Drive folder sits directly under `1. Projects/{Domain}/`.

> Every project in `01 Projects/` is a **directory** containing an index note of the same name.

The first invariant is checkable from the Dashboard — the **Projects Needing Reconciliation** pane should always be empty.

## The Procedure

Run this end to end. It reads only. It never mutates anything.

### 1. Collect the Obsidian side

For every directory in `01 Projects/`, read its index note (`{Folder}/{Folder}.md`) and record `status`, `domain`, `todoist`, `drive`.

Flag any directory with no index note, and any loose `.md` file sitting directly in `01 Projects/` — both are structural violations.

### 2. Collect the Todoist side

```
mcp__todoist__get-overview     (no arguments)
```

One call returns the entire project tree with IDs, names, and `parentId`. Nothing else is needed.

### 3. Collect the Drive side

`1. Projects/` is folder ID `14Kt3GswyG0moflC5iLEG769Rov879PiA`.

```
search_files: parentId = '14Kt3GswyG0moflC5iLEG769Rov879PiA'
```

That returns the per-domain subfolders. Then one query per domain subfolder to get its projects.

### 4. Join

Match on the frontmatter URLs first — the ID is the last path segment of each URL:

- `https://app.todoist.com/app/project/{id}`
- `https://drive.google.com/drive/folders/{id}`

> Name matching may only **propose** a binding for a human to confirm. It must never assert one. Names drift; IDs don't.

### 5. Classify

| Finding | Meaning | Remedy |
|---------|---------|--------|
| Missing Todoist project | Active project, no `todoist` and no name match | Create it under the domain parent; add a next action |
| Missing Drive folder | Active project, no `drive` and no name match | Create `1. Projects/{Domain}/{Name}/` |
| Unlinked, name matches | Counterpart exists but frontmatter is empty | Confirm, then backfill the URL |
| Name drift | Bound, but names differ across systems | Pick the canonical name; rename the other two |
| Wrong domain parent | Todoist project not under its domain parent, or Drive folder not under `1. Projects/{Domain}/` | Move it |
| Duplicate Obsidian project | Two notes claim the same project | Merge; keep one |
| No next action | Active project with no due-dated Todoist task | Add one, or drop to `backlog` / `on-hold` |
| Malformed frontmatter | Missing/invalid `type`, `status`, `domain`, `priority` | Fix to match [[Conventions]] |
| Orphan Todoist/Drive item | Exists there, not in Obsidian | **Informational only** — allowed by the contract |

### 6. Write the report

Save to `99 Meta/Reports/Reconciliation YYYY-MM-DD.md`, one row per finding with a proposed action.

> **Stop here.** The pass reports; it does not fix. Apply changes only after the report is reviewed.

## Cadence

Run during the Sunday weekly review, alongside the existing *"Update projects and ensure each has a next action"* step in the daily note's Clarify & Update block.

A clean run — zero actionable findings — is the goal state. If the run is never clean, the invariants are wrong or the process isn't being followed; fix that rather than tolerating a permanently noisy report.

## Example: Creating a New Project

Doing this correctly means the next reconciliation pass finds nothing.

1. **Obsidian** — create `01 Projects/Kitchen Remodel/Kitchen Remodel.md` from the `Project.md` template. Set `status: active`, `domain: personal`, `priority`.
2. **Todoist** — create project `Kitchen Remodel` under the `Personal` parent. Add a next action with a due date: `Kitchen Remodel: Get contractor quotes`.
3. **Drive** — create folder `1. Projects/Personal/Kitchen Remodel/`.
4. **Back in Obsidian** — paste both URLs into `todoist:` and `drive:`.

Step 4 is the one that gets skipped. Without it the project is unreconcilable, and it will show up in the Dashboard pane until it's done.
