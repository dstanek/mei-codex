---
type: meta
---
# Conventions

Standards for organizing notes, projects, and tasks across Obsidian and Todoist.

## Note Types

Notes use a `type` frontmatter field. Templates live in `99 Meta/Templates/`.

| Type         | Template             | Purpose                                                 |
| ------------ | -------------------- | ------------------------------------------------------- |
| `zettel`     | `Zettel.md`          | Atomic permanent ideas with links and source            |
| `literature` | `Literature Note.md` | Book/article notes: summary, takeaways, quotes          |
| `project`    | `Project.md`         | Has `status` and `domain` fields; tracked in Todoist    |
| `topic`      | `Topic.md`           | Reference hub; Dataview shows backlinks                 |
| `video-idea` | `Video Idea.md`      | YouTube content; auto-names file `Video Idea - {title}` |
| `meta`       | —                    | Vault config and conventions                            |

## Project Naming

| Location             | Pattern                                | Example                    |
| -------------------- | -------------------------------------- | -------------------------- |
| Obsidian             | `Project - {short name}`               | `Project - Homelab`        |
| Obsidian frontmatter | `domain: {domain}`                     | `domain: personal`         |
| Todoist project      | `{short name}` under `{Domain}` parent | `Homelab` under `Personal` |
| Todoist task         | `{short name}: {task}` *(optional)*    | `Homelab: Setup shelf`     |

### When to use task prefixes

**Use prefix when:**
- Creating tasks for "Today" or aggregate views
- Quick capturing to Inbox (makes sorting easier)
- Task might appear in filters/searches

**Skip prefix when:**
- Creating tasks directly inside the project
- Context is already clear

## Domains

Domains connect Obsidian projects to Todoist areas:

| Domain | Obsidian `domain:` | Todoist Parent |
|--------|-------------------|----------------|
| Personal | `personal` | Personal |
| HPE (work) | `hpe` | HPE |
| CWRU (teaching) | `cwru` | CWRU |
| Learn Fast (business) | `learn-fast` | Learn Fast |

## Project Frontmatter

Standard frontmatter for projects:

```yaml
---
type: project
status: active    # active, backlog, on-hold, archived
domain: personal  # personal, hpe, cwru, learn-fast
---
```

### Status values

- `active` — Currently being worked on, must have a next action
- `backlog` — Defined but not started, no next action required
- `on-hold` — Paused, waiting on something external
- `archived` — Completed or abandoned, moved to `04 Archive/`

## GTD Rule

> Every project with `status: active` must have at least one task with a due date in Todoist.

If an active project has no next action, either:
1. Add a next action, or
2. Change status to `backlog` or `on-hold`

## Examples

### Creating a new project

1. In Obsidian: Create `01 Projects/Project - Kitchen Remodel.md`
2. Add frontmatter: `type: project`, `status: active`, `domain: personal`
3. In Todoist: Create project `Kitchen Remodel` under `Personal`
4. Add first task: `Kitchen Remodel: Get contractor quotes` with due date

### Moving to backlog

1. In Obsidian: Change `status: active` → `status: backlog`
2. In Todoist: Remove due dates or move tasks to Someday/Maybe
