---
type: meta
---
# Conventions

Standards for organizing notes, projects, and tasks across Todoist, Obsidian, and Google Drive.

> **Todoist is the canonical list of projects.** Obsidian holds my thinking about them; Drive holds material I've downloaded. Both are optional supporting material.

For checking that the three stay in sync, see [[Project Reconciliation]].

## Note Types

Notes use a `type` frontmatter field. Templates live in `99 Meta/Templates/`.

| Type         | Template             | Purpose                                                 |
| ------------ | -------------------- | ------------------------------------------------------- |
| `zettel`     | `Zettel.md`          | Atomic permanent ideas with links and source            |
| `literature` | `Literature Note.md` | Book/article notes: summary, takeaways, quotes          |
| `project`    | `Project.md`         | Directory with an index note; mirrored in Todoist and Drive |
| `area`       | —                    | Ongoing responsibility with no completion condition; lives in `02 Areas/` |
| `topic`      | `Topic.md`           | Reference hub; Dataview shows backlinks                 |
| `video-idea` | `Video Idea.md`      | YouTube content; auto-names file `Video Idea - {title}` |
| `meta`       | —                    | Vault config and conventions                            |

## Project Naming

Every project has one **canonical short name**, set in Todoist and reused everywhere else.

| Location             | Pattern                                     | Example                            | Required? |
| -------------------- | ------------------------------------------- | ---------------------------------- | --------- |
| Todoist project      | `{short name}` under `{Domain}` parent      | `Homelab` under `Personal`         | **Yes**   |
| Todoist task         | `{short name}: {task}` *(optional prefix)*  | `Homelab: Setup shelf`             | —         |
| Obsidian             | `01 Projects/{short name}/{short name}.md`  | `01 Projects/Homelab/Homelab.md`   | Optional  |
| Obsidian frontmatter | `domain: {domain}`                          | `domain: personal`                 | —         |
| Google Drive         | `1. Projects/{Domain}/{short name}/`        | `1. Projects/Personal/Homelab/`    | Optional  |

A project exists because it's in Todoist. Create an Obsidian note when you have thinking to capture, and a Drive folder when you have downloads to keep — not by default.

> **Drive folders need no index file.** They're buckets for downloads; nothing is required inside them.

### Project structure in Obsidian

A project is always a **directory**, never a loose file. The directory contains an index note named after the folder, which carries the project frontmatter:

```
01 Projects/
  Homelab/
    Homelab.md          <- index note, has project frontmatter
    Rack Layout.md      <- support note, no project frontmatter
    Network Diagram.md
```

Support notes inside a project folder need no `type: project` frontmatter — the index note is the single anchor.

> Do **not** create domain folders under `01 Projects/`. Domain lives in frontmatter, and Dataview handles the grouping. See [[Project Reconciliation]] for why the three systems are organized differently.

### When to use task prefixes

**Use prefix when:**
- Creating tasks for "Today" or aggregate views
- Quick capturing to Inbox (makes sorting easier)
- Task might appear in filters/searches

**Skip prefix when:**
- Creating tasks directly inside the project
- Context is already clear

## Domains

Domains connect Obsidian projects to Todoist parents and Drive folders. This list is closed — a project's `domain` must be one of these seven:

| Domain | Obsidian `domain:` | Todoist Parent | Drive Folder |
|--------|-------------------|----------------|--------------|
| Personal | `personal` | Personal | `1. Projects/Personal/` |
| HPE (work) | `hpe` | HPE | `1. Projects/HPE/` |
| CWRU (teaching) | `cwru` | CWRU | `1. Projects/CWRU/` |
| Learn Fast (business) | `learn-fast` | Learn Fast | `1. Projects/Learn Fast/` |
| Preheat to 350 (business) | `preheat-350` | Preheat to 350 | `1. Projects/Preheat to 350/` |
| Paige Creations (business) | `paige-creations` | Paige Creations | `1. Projects/Paige Creations/` |
| Freelancing | `freelancing` | Freelancing | `1. Projects/Freelancing/` |

Adding a domain means adding all four: the `domain:` value, a Todoist parent project, a `One-Off` child under it, and a `1. Projects/` subfolder.

## One-Off Tasks

> A domain parent project holds **no tasks directly**. Every task lives in a real project, or in that domain's `One-Off` project.

Each domain parent has a `One-Off` child for tasks that don't justify a project of their own — *Fix fence*, *Check on the GitHub Terraform management*, *Organize under desk cables*.

| Domain | One-Off project ID |
|--------|--------------------|
| `personal` | `6hCvCx7PMCr5jCvX` |
| `hpe` | `6hCvGfxQmqXjg29v` |
| `cwru` | `6hCvGgw4Wjm43Hgj` |
| `learn-fast` | `6hCvGmRjJQHxPc7q` |
| `preheat-350` | `6hCvGjV4X9wgCwHc` |
| `paige-creations` | `6hCvGw6r958JC9Wq` |
| `freelancing` | `6hCvGrP8JR9jjCPj` |

This keeps the domain parent a pure container, so "projects under this domain" is a clean list rather than a list mixed with loose tasks.

### What does *not* belong in One-Off

- **Tasks belonging to a real project.** If a task is prefixed `{Project}: {task}`, it belongs in that project.
- **Recurring tasks.** A repeating task isn't one-off. Keep those in the domain's `Recurring Tasks` section.

### One-Off is not a project

`One-Off` projects are permanent buckets. They never complete, so the GTD rule doesn't apply to them, they're never "stalled", and they get no Obsidian note and no Drive folder. Reconciliation skips them — same treatment as `Someday / Maybe`.

### Areas vs. Projects in Drive

Drive's numbered roots `5. Preheat to 350`, `6. Paige Stanek`, `7. Learn Fast`, and `8. Cabinet` are **Areas** — evergreen per-focus material (`Graphics`, `Videos`, `logos`, `shopify`). Project-scoped downloads go under `1. Projects/{Domain}/`, not into these.

## Project Frontmatter

Standard frontmatter for the project index note:

```yaml
---
title: Homelab
type: project
status: active     # active, backlog, on-hold, archived
domain: personal   # see Domains table
priority: 2
created: 2025-11-03 09:12
todoist: https://app.todoist.com/app/project/6fwMM9662W23qXCH
drive: https://drive.google.com/drive/folders/1PrTZmsM453LSEKwjDebWdhPU9WdRXbcA
tags: []
---
```

`todoist` is **required on every project note** — it's what makes the note a project rather than an idea. `drive` is optional; set it only when the project has downloaded material.

Both hold full URLs rather than bare IDs: Obsidian renders them clickable, and the ID is the last path segment when a tool needs it. These URLs — not folder paths or names — are what bind the three systems. An existing Drive folder stays valid wherever it sits; the path convention only governs where new folders get created.

`status` and `domain` exist here so the Dashboard's Dataview panes work — Dataview can't query Todoist.

- **`domain`** mirrors the project's Todoist parent. Todoist wins; a mismatch means the note is wrong.
- **`status`** has no equivalent field in Todoist, so it's *derived* from Todoist state:

| Todoist state | `status` |
|---|---|
| Archived | `archived` |
| Has at least one due-dated task | `active` |
| Has tasks, none due-dated | `backlog` or `on-hold` — your call |

Which means `status: active` with no due-dated task in Todoist is always a contradiction. That's the GTD rule restated, and it's what the reconciliation pass looks for.

### Status values

- `active` — Currently being worked on, must have a next action
- `backlog` — Defined but not started, no next action required
- `on-hold` — Paused, waiting on something external
- `archived` — Completed or abandoned, moved to `04 Archive/Projects/`

### Project or Area?

> A project has a **completion condition**. If you can't say what "done" looks like, it's an Area.

Ongoing pursuits — learning a subject, staying fit, managing a career — never complete, so the GTD rule can't apply to them. Filing them in `01 Projects/` produces permanently stalled projects that accumulate links instead of actions. Put them in `02 Areas/` with `type: area` instead.

## GTD Rule

> Every active Todoist project must have at least one task with a due date.

If an active project has no next action, either:
1. Add a next action, or
2. Change status to `backlog` or `on-hold`

The rule is about **Todoist**, since that's where projects live. Every project note in `01 Projects/` must also carry a `todoist` URL that resolves. See [[Project Reconciliation]] for how both get checked.

## Examples

### Creating a new project

Todoist first, because Todoist decides what exists.

1. **Todoist** — create project `Kitchen Remodel` under the `Personal` parent.
2. **Todoist** — add a next action with a due date: `Kitchen Remodel: Get contractor quotes`.
3. **Obsidian** *(only if you have thinking to capture)* — create `01 Projects/Kitchen Remodel/Kitchen Remodel.md` from the `Project.md` template, mirror `status`/`domain`/`priority`, and paste the Todoist URL into `todoist:`.
4. **Drive** *(only if you'll download material)* — create `1. Projects/Personal/Kitchen Remodel/` and paste its URL into `drive:`.

Steps 3 and 4 are optional. Step 1 is not — a project that isn't in Todoist doesn't exist. If you do create the note, pasting the `todoist:` URL is the step that gets skipped; without it the note shows in the Dashboard's *Notes Needing a Todoist Link* pane.

### Moving to backlog

1. **Obsidian** — change `status: active` → `status: backlog`
2. **Todoist** — remove due dates, or move tasks to Someday/Maybe

The `todoist` and `drive` URLs stay — they're still correct, just no longer required.

### Archiving

1. **Obsidian** — set `status: archived`, move the project directory to `04 Archive/Projects/`
2. **Todoist** — archive the project
3. **Drive** — move the folder to `4. Archive/`
