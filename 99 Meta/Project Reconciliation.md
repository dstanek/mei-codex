---
type: meta
created: 2026-08-18 10:20
tags: []
---
# Project Reconciliation

How to check that projects line up across Todoist, Obsidian, and Google Drive — and what to do when they don't.

For naming, domains, and frontmatter, see [[Conventions]].

## The Three-System Contract

| System | Owns | Holds |
|--------|------|-------|
| **Todoist** | **The canonical list of projects.** Existence, status, next actions | Tasks |
| **Obsidian** | My thinking about a project | Notes and ideas I *write* |
| **Google Drive** | — | Material I *download* |

> **Todoist is authoritative.** It decides what projects exist and whether they're active. Obsidian and Drive are supporting material, and both are optional — plenty of projects never need either.

The consequence that matters: **an Obsidian project note pointing at a Todoist project that no longer exists is an error.** A Todoist project with no Obsidian note is not.

## Why the Three Trees Differ

PARA is a *lifecycle* taxonomy (project / area / resource / archive). Domain is *orthogonal* to it. Encoding both in one folder tree forces a bad choice: domain-first duplicates PARA once per domain and fragments Areas; lifecycle-first dumps every domain into one bucket.

Because an Obsidian project note carries an explicit `todoist:` URL, **binding is by link, not by path** — so the trees don't need to match. Each system groups by the dimension it is actually good at:

| System | Native strength | Groups by |
|--------|-----------------|-----------|
| Todoist | Parent-project nesting; no project-level metadata | **Domain.** One parent project per domain |
| Obsidian | Frontmatter + Dataview — real facets | **Lifecycle.** Flat `01 Projects/`; domain lives in `domain:` |
| Drive | Folders only — no query, no metadata | **Domain.** `01 Projects/{Domain}/` |

Do not add domain folders to `01 Projects/`. Dataview already gives you per-domain views, and the Dashboard uses them.

Drive's legacy roots `5. Preheat to 350`, `6. Paige Stanek` and `7. Learn Fast` predate the current scheme and hold evergreen per-focus material. Nothing new goes into them: project-scoped downloads belong under `01 Projects/{Domain}/`, evergreen material under `02 Areas/{Subject}/`. See *Drive structure* in [[Conventions]] for the one-home-per-subject rule.

> **Drive folders need no index file.** A Drive folder is a bucket for downloads. Nothing is required to be in it, and it needs no note, README, or manifest.

## Invariants

> Every Todoist project sits directly under the parent matching its domain. Only the domain parents themselves live at top level.

> A domain parent holds **no tasks directly** — every task belongs to a real project, or to that domain's `One-Off` project. *(see [[Conventions#One-Off Tasks]])*

> Every Todoist project with an active status has at least one task with a due date. *(the GTD rule from [[Conventions]])*

> Every project note in `01 Projects/` has a `todoist:` URL that resolves to a live Todoist project.

> Every project in `01 Projects/` is a **directory** containing an index note of the same name.

`drive:` is optional everywhere — set it when the project has downloaded material, leave it empty otherwise.

### On mirrored fields

`status` and `domain` appear in Obsidian frontmatter so the Dashboard's Dataview panes work — Dataview can't reach Todoist.

`domain` mirrors the Todoist parent, and Todoist wins on conflict. `status` has no Todoist equivalent, so it's derived: archived → `archived`, has a due-dated task → `active`, otherwise `backlog`/`on-hold`. See [[Conventions#Project Frontmatter]].

Reconciliation reports drift and syncs Obsidian to match Todoist — never the reverse.

## The Procedure

Run this end to end. It reads only. It never mutates anything.

### 1. Collect the canonical side — Todoist

```
mcp__todoist__get-overview     (no arguments)
```

One call returns the entire project tree with IDs, names, and `parentId`. This is the list of projects that exist.

For the GTD check, per project:

```
mcp__todoist__find-tasks  filter: "##<Project Name> & !no date"
```

### 2. Collect the Obsidian side

For every directory in `01 Projects/`, read its index note (`{Folder}/{Folder}.md`) and record `status`, `domain`, `todoist`, `drive`.

Flag any directory with no index note, and any loose `.md` file sitting directly in `01 Projects/` — both are structural violations.

### 3. Collect the Drive side

`01 Projects/` is folder ID `14Kt3GswyG0moflC5iLEG769Rov879PiA`.

```
search_files: parentId = '14Kt3GswyG0moflC5iLEG769Rov879PiA'
```

That returns the per-domain subfolders. Then one query per domain subfolder.

> The Drive connector can create, move, rename, and trash. `create_file` makes folders, `update_file` takes a `title` (rename) and a `parentId` (move — the existing parent is *replaced*), and `trash_file` sends to trash, recoverable for 30 days.
>
> **This pass still doesn't do any of it.** Reconciliation reports and stops — that rule is about the pass being read-only, not about a tool limitation. A folder move leaves no visible trace once it's done, so relocations get proposed here and executed only after review, with each one logged old-path → new-path against the file ID.

### 4. Join

Match on the frontmatter URLs — the ID is the last path segment:

- `https://app.todoist.com/app/project/{id}`
- `https://drive.google.com/drive/folders/{id}`

> Name matching may only **propose** a binding for a human to confirm. It must never assert one. Names drift; IDs don't.

### 5. Classify

| Finding | Meaning | Remedy |
|---------|---------|--------|
| **Dangling note** | Obsidian note's `todoist:` points at a project that no longer exists | Archive the note, or repoint it |
| **Unlinked note** | Obsidian project note with no `todoist:` at all | Bind it, or move it out of `01 Projects/` — it's an idea, not a project |
| Status drift | Obsidian `status`/`domain` disagrees with Todoist | Sync Obsidian to match Todoist |
| No next action | Active Todoist project with no due-dated task | Add one, or change its status |
| Orphan parent | Todoist project at top level that isn't a domain parent | Move under the right domain parent |
| **Loose task** | Task sitting directly in a domain parent | Move to the owning project, or to that domain's `One-Off` |
| Stalled project | Active Todoist project whose tasks are all long overdue or untouched | Reschedule, or drop out of active |
| Name drift | Bound, but names differ across systems | Pick the canonical name; rename the others |
| Structural | Loose file in `01 Projects/`, or a directory with no index note | Fix to match [[Conventions]] |
| Missing note / folder | Todoist project with no Obsidian note or Drive folder | **Informational only** — both are optional |

### 6. Write the report

Save to `99 Meta/Reports/Reconciliation YYYY-MM-DD.md`, one row per finding with a proposed action.

> **Stop here.** The pass reports; it does not fix. Apply changes only after the report is reviewed.

## Cadence

Run during the Sunday weekly review, alongside the existing *"Update projects and ensure each has a next action"* step in the daily note's Clarify & Update block.

A clean run — zero actionable findings — is the goal state. If the run is never clean, the invariants are wrong or the process isn't being followed; fix that rather than tolerating a permanently noisy report.

## Example: Creating a New Project

Todoist first, because Todoist decides what exists.

1. **Todoist** — create the project under its domain parent. Add a next action with a due date: `Kitchen Remodel: Get contractor quotes`.
2. **Obsidian** *(optional)* — if you have thinking to capture, create `01 Projects/Kitchen Remodel/Kitchen Remodel.md` from the `Project.md` template and paste the Todoist URL into `todoist:`.
3. **Drive** *(optional)* — if you'll be downloading material, create `01 Projects/{Domain}/Kitchen Remodel/` and paste its URL into `drive:`.

Steps 2 and 3 are genuinely optional. Step 1 is not — a project that isn't in Todoist doesn't exist.
