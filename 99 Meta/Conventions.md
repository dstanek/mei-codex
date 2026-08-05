---
type: meta
---
# Conventions

Standards for organizing notes, projects, and tasks across Obsidian, Todoist, and Google Drive.

For checking that the three stay in sync, see [[Project Reconciliation]].

## Note Types

Notes use a `type` frontmatter field. Templates live in `99 Meta/Templates/`.

| Type         | Template             | Purpose                                                 |
| ------------ | -------------------- | ------------------------------------------------------- |
| `zettel`     | `Zettel.md`          | Atomic permanent ideas with links and source            |
| `literature` | `Literature Note.md` | Book/article notes: summary, takeaways, quotes          |
| `project`    | `Project.md`         | Directory with an index note; mirrored in Todoist and Drive |
| `topic`      | `Topic.md`           | Reference hub; Dataview shows backlinks                 |
| `video-idea` | `Video Idea.md`      | YouTube content; auto-names file `Video Idea - {title}` |
| `meta`       | —                    | Vault config and conventions                            |

## Project Naming

Every project has one **canonical short name** used in all three systems.

| Location             | Pattern                                     | Example                            |
| -------------------- | ------------------------------------------- | ---------------------------------- |
| Obsidian             | `01 Projects/{short name}/{short name}.md`  | `01 Projects/Homelab/Homelab.md`   |
| Obsidian frontmatter | `domain: {domain}`                          | `domain: personal`                 |
| Todoist project      | `{short name}` under `{Domain}` parent      | `Homelab` under `Personal`         |
| Todoist task         | `{short name}: {task}` *(optional)*         | `Homelab: Setup shelf`             |
| Google Drive         | `1. Projects/{Domain}/{short name}/`        | `1. Projects/Personal/Homelab/`    |

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

Adding a domain means adding all three: the `domain:` value, a Todoist parent project, and a `1. Projects/` subfolder.

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

`todoist` and `drive` are **required when `status: active`** and optional otherwise. They hold full URLs rather than bare IDs: Obsidian renders them clickable, and the ID is the last path segment when a tool needs it.

These URLs — not folder paths or names — are what bind the three systems. An existing Drive folder stays valid wherever it sits; the path convention only governs where new folders get created.

### Status values

- `active` — Currently being worked on, must have a next action
- `backlog` — Defined but not started, no next action required
- `on-hold` — Paused, waiting on something external
- `archived` — Completed or abandoned, moved to `04 Archive/Projects/`

## GTD Rule

> Every project with `status: active` must have at least one task with a due date in Todoist.

If an active project has no next action, either:
1. Add a next action, or
2. Change status to `backlog` or `on-hold`

Active projects must also carry `todoist` and `drive` URLs. See [[Project Reconciliation]] for how both rules get checked.

## Examples

### Creating a new project

1. **Obsidian** — create `01 Projects/Kitchen Remodel/Kitchen Remodel.md` from the `Project.md` template. Set `status: active`, `domain: personal`, `priority`.
2. **Todoist** — create project `Kitchen Remodel` under the `Personal` parent.
3. **Todoist** — add a next action with a due date: `Kitchen Remodel: Get contractor quotes`.
4. **Drive** — create folder `1. Projects/Personal/Kitchen Remodel/`.
5. **Obsidian** — paste both URLs into `todoist:` and `drive:`.

Step 5 is the one that gets skipped. Without it the project can't be reconciled, and it stays in the Dashboard's *Projects Needing Reconciliation* pane until it's done.

### Moving to backlog

1. **Obsidian** — change `status: active` → `status: backlog`
2. **Todoist** — remove due dates, or move tasks to Someday/Maybe

The `todoist` and `drive` URLs stay — they're still correct, just no longer required.

### Archiving

1. **Obsidian** — set `status: archived`, move the project directory to `04 Archive/Projects/`
2. **Todoist** — archive the project
3. **Drive** — move the folder to `4. Archive/`
