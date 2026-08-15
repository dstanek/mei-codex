# Shared reference for the `project-*` skills

Read this once at the start of any of `project-review`, `project-new`, or
`project-reconcile`. It holds the things all three need and nothing else.

> **Not a skill.** This directory has no `SKILL.md` on purpose — it is a library
> the three skills point at, so the domain table and the agent/script contract
> exist in exactly one place.

## The rules live in the vault, not here

These notes are the source of truth. Read the one you need rather than trusting a
summary — if they change, the skills must follow without being edited.

| Note | What it decides |
|---|---|
| `99 Meta/Conventions.md` | Naming, the `01 Projects/{Name}/{Name}.md` layout, frontmatter fields, the four statuses, the seven domains, the GTD rule |
| `99 Meta/Project Reconciliation.md` | The three-system contract, the invariants, the reconcile procedure, the finding taxonomy |
| `99 Meta/Templates/Project.md` | The shape of a new project note |
| `99 Meta/Reports/Reconciliation *.md` | What a finished report looks like |

The short version, enough to act on before reading them:

- **Todoist is canonical.** It decides which projects exist and whether they're
  active. A note pointing at a dead Todoist project is an error; a Todoist
  project with no note is not.
- **Obsidian and Drive are optional.** Create a note when there's thinking to
  capture, a Drive folder when there's material to download. Never by default.
- **An Area has no Todoist project**, and its `todoist:` stays empty — see *Areas*
  in Conventions.md. So "move this to `02 Areas/`" always means retiring the
  Todoist project too, after rehoming its tasks to a real project or a `One-Off`.
  Areas live outside `01 Projects/`, so nothing scans them.
- **Binding is by URL**, held in the note's frontmatter: `todoist:` (required on
  every project note) and `drive:` (optional). The ID is the last path segment.
  Name matching may only *propose* a binding for a human to confirm — never
  assert one.
- **Todoist wins on conflict.** When `status`/`domain` disagree, the note gets
  corrected, never Todoist.
- **`domain` mirrors; `status` is derived.** Todoist has no project status
  field, so `status` is computed from Todoist state, not read from it.

### Deriving `status`

| Todoist state | `status` |
|---|---|
| Archived | `archived` |
| Has at least one due-dated task | `active` |
| Has tasks, none due-dated | `backlog` or `on-hold` |

This makes `status` checkable rather than an unverifiable mirror: a note saying
`active` while Todoist has nothing due-dated is a contradiction, and it's the
GTD rule restated. Todoist can't tell `backlog` from `on-hold` — only a human
knows whether something is paused or merely unstarted — so neither is ever
reported as drift against the other. `vaultlib.derive_status()` and
`status_conflict()` implement this; use them rather than rolling the comparison
by hand.

## Domains

The seven-domain enum is closed. IDs live in machine-readable form in
`domains.json`, which is the only place they are written down — scripts read it,
and this table is generated from the same values.

| `domain:` | Todoist parent | `One-Off` child | `Someday / Maybe` child | Drive folder under `1. Projects/` |
|---|---|---|---|---|
| `personal` | `6CrgJQx8x2Pj59Mq` | `6hCvCx7PMCr5jCvX` | `6fRrh8F4mjQ5987P` | `1nXCFdV5odms0IZNcI-W65PlYASwa3iXR` |
| `hpe` | `6VJV6WFQ8837mrgM` | `6hCvGfxQmqXjg29v` | `6VJRvvFRxRxpMgj2` | `1iINWT9BIPwKq_6MF7NbwF-bHdKVPHHav` |
| `cwru` | `6fCMPq9f4CVMGmP7` | `6hCvGgw4Wjm43Hgj` | `6hF3VX9HhphWqwmV` | `1KGdSZJ4iKBoje5EMyk1YwminYdAvfsiE` |
| `learn-fast` | `6fgpCJHmFgJc7qx8` | `6hCvGmRjJQHxPc7q` | `6hF3VX84FvRXJm86` | `1ykSWMTDwrePdWy1LkvFptTNFlYpovWFP` |
| `preheat-350` | `6fgpCGf5HC2WHrRv` | `6hCvGjV4X9wgCwHc` | `6hF3VX73rc7QM28H` | `1yEzHGIOZs6qzHYT7KlhGblqOH9e2kzOZ` |
| `paige-creations` | `6hCqPPfMC67j8cpJ` | `6hCvGw6r958JC9Wq` | `6hF3VX9h3gFjJ3WH` | `18Omxpp8bK5qp6U1BTGekySrk8nnL1maS` |
| `freelancing` | `6fwPWr428M6qVxrV` | `6hCvGrP8JR9jjCPj` | `6hF3VX938w7wvjrX` | `19382M9SJrkcPflQxzSQqky8nHYTi5yhs` |

`1. Projects/` root is `14Kt3GswyG0moflC5iLEG769Rov879PiA`.
`4. Archive/Projects/` is `1PNRF-4Fk8jPOjcgxt6NPQktD7KSMS9NX`.

### One-Off

A domain parent holds **no tasks directly**. Every task lives in a real project
or in that domain's `One-Off` — see *One-Off Tasks* in Conventions.md. Two tasks
that look loose but aren't:

- A task prefixed `{Project}: {task}` belongs in that **named project**, not
  One-Off.
- A **recurring** task isn't one-off; it stays in the domain's
  `Recurring Tasks` section.

`One-Off` projects are permanent buckets. They never complete, so the GTD rule
and the stalled check don't apply, and they never get an Obsidian note or a
Drive folder. The scripts skip them automatically from `domains.json`.

Each domain's `Someday / Maybe` (`someday_project_id`) is the same kind of thing,
and sits under the domain parent just like `One-Off`. See *Someday / Maybe* in
Conventions.md. Items there carry no date — a date means it's a commitment, so it
belongs in a real project or a `One-Off` instead.

URLs are built as `https://app.todoist.com/app/project/{id}` and
`https://drive.google.com/drive/folders/{id}`.

## Scripts cannot call MCP tools

This is the constraint that shapes everything. MCP tools belong to the agent;
a `python3` subprocess has no access to them. So:

- **Scripts** own the local vault: walking `01 Projects/`, parsing frontmatter,
  checking structure, joining, sorting, formatting.
- **You** own the remote systems: every Todoist and Drive call, and every
  judgement call about what a project is *for*.

The handoff is a JSON file. You make the MCP calls, write the results to a temp
file, and pass its path to the script. A script that tries to reach Todoist
directly is broken.

### The remote JSON envelope

Every script that needs remote data takes `--remote <path>` pointing at this.
Only `overview` is required; each script says which of the rest it wants.

```json
{
  "overview":       { ...get-overview response, verbatim... },
  "tasks":          [ ...task objects, concatenated across find-tasks calls... ],
  "tasks_include_undated": false,
  "completed":      [ ...from find-completed-tasks... ],
  "activity":       [ ...from find-activity... ],
  "drive_folders":  [ {"id": "...", "title": "...", "parentId": "..."} ],
  "drive_scanned":  false
}
```

Paste tool responses in as they came back — the scripts read the field names
Todoist actually returns and tolerate the shape variations. Set
`tasks_include_undated` to `true` only when you collected the `no date` sweep as
well; the scripts use it to tell "this project is empty" apart from "I wasn't
given its undated tasks", which are very different findings.

Write the file with `python3 -c` or a heredoc rather than shelling out `echo`
with a giant JSON string — the task descriptions contain quotes, newlines, and
non-ASCII.

## MCP calls worth knowing

| Call | Use |
|---|---|
| `mcp__todoist__get-overview` (no args) | The whole project tree with IDs and `parentId`, in one call. Always start here |
| `mcp__todoist__find-tasks` `filter: "!no date"` | Every task with a due date, across all projects. Answers overdue, upcoming, and the GTD rule at once |
| `mcp__todoist__find-tasks` `filter: "no date"` | Every undated task. **Expensive** — descriptions are long. Only pull it when you actually need undated tasks |
| `mcp__todoist__find-tasks` `filter: "!no deadline"` | Every task with a **deadline**. Cheap — there are few. The `!no date` sweep does *not* see these; see *Deadlines* below |
| `mcp__todoist__find-tasks` `filter: "@waiting"` | Everything delegated or blocked on someone else. Cheap; see *Waiting For* below |
| `mcp__todoist__find-tasks` `projectId: <id>` | One project's tasks. Prefer this over the `no date` sweep when you only care about a handful of projects |
| `mcp__todoist__find-completed-tasks` `since`/`until` | Completions in a window — the strongest stalled signal |
| `mcp__todoist__find-activity` `objectType: "task"`, `dateFrom` | Adds, updates, reschedules. Events carry `parentProjectId` |
| `mcp__todoist__add-projects` / `add-tasks` | Creating. `add-tasks` takes `dueString` in natural language and priority as `p1`–`p4` strings |
| `mcp__todoist__reschedule-tasks` | **Always** for moving a due date. `update-tasks` replaces the whole due string and destroys recurrence |
| `mcp__claude_ai_Google_Drive__search_files` `parentId = '<id>'` | List a folder's children |
| `mcp__claude_ai_Google_Drive__create_file` with `mimeType: application/vnd.google-apps.folder` | Create a folder |

`find-tasks` paginates: keep calling with the returned `cursor` until
`hasMore` is false, or you will silently analyse a partial list.

### Deadlines

Todoist's `due` and `deadline` are different fields — *when I'll work on it* vs
*when the world needs it*. See *Due dates vs. deadlines* in Conventions.md.

`vaultlib.task_due_date()` reads `dueDate`/`dueDatetime`/`due` and **ignores
`deadlineDate` on purpose**: only a due date satisfies the GTD rule, because a
deadline is a constraint rather than a plan to act. `vaultlib.task_deadline()`
reads the deadline instead, and the two are never folded together.

So a deadline-only task counts as **undated** for the GTD check — it won't appear
in overdue or upcoming and won't make its project pass. That's intended, not a
bug: a project whose only date is a deadline has a delivery date and no plan.

`review.py` has a dedicated **Deadlines** lane that reports them anyway, sorted
by deadline with an `unplanned` flag for the ones carrying no due date
(`--deadline-days N`, default 14). `reconcile.py` does **not** — it has no
deadline finding, so a deadline-only task is silent there.

### Waiting For

A task labelled `waiting` is tracked, not done — the next move is someone
else's. See *Waiting For* in Conventions.md.

`vaultlib.is_waiting()` detects the label (tolerating a stray `@`), and
`vaultlib.actionable_due_date()` is `task_due_date()` with `waiting` tasks
returning None. **Use `actionable_due_date()` for anything that decides whether
a project has a next action** — the GTD check, the derived status, the stalled
check. Both scripts already do; `task_due_date()` remains for views that want
the raw date someone promised.

So a `waiting` task never makes its project pass, however it is dated. Reconcile
names the reason in the finding rather than reporting a bare "none due-dated" on
a project that visibly has a dated task.

`review.py` also pulls waiting tasks out of Upcoming and Overdue into their own
**Waiting For** section, longest-wait first, using `addedAt` as the age signal —
the same split the three Today filters make with `& !@waiting`.

> **Drive can create, but cannot move, rename, or delete.** Any relocation has
> to be done by hand in the Drive UI. Report it; don't attempt it, and don't
> work around it by creating a copy.

## The scripts

All take `--vault` (auto-detected otherwise) and `--config` (defaults to
`domains.json`). Run any of them with `--help` for the full surface.

| Script | Does |
|---|---|
| `_shared/scripts/scan_vault.py` | Walks `01 Projects/` → JSON. `--summary` for a readable dump |
| `_shared/scripts/set_frontmatter.py` | Sets frontmatter fields on one note, line-based, leaving the rest byte-identical |
| `_shared/scripts/vaultlib.py` | The library the others import — not run directly |
| `project-review/scripts/review.py` | Daily review draft + analysis JSON |
| `project-reconcile/scripts/reconcile.py` | Full reconciliation report |
| `project-new/scripts/new_project_note.py` | Renders the Project template into `01 Projects/{Name}/{Name}.md` |

## What gets skipped

Two kinds of Todoist project are exempt from the GTD and stalled checks, and
both are structural — there is no human-maintained exclusion list, because
*"does this ever complete?"* is not a judgement call:

1. **Holding pens** — every domain's `One-Off` bucket and its `Someday / Maybe`
   (`one_off_project_id` and `someday_project_id` in the domains table), so
   fourteen in all. `vaultlib.holding_pen_ids()` returns them with a reason
   string; use it rather than assembling the set by hand. Neither kind ever
   completes, so they also never get an Obsidian note or a Drive folder.
2. **Grouping containers** — any project that has sub-projects. Detected
   structurally and reported separately.

Every run prints what it skipped and why, so nothing disappears quietly. Tasks
inside skipped projects still show up under upcoming and overdue — the exemption
is from *project*-level checks, not from the task views.
