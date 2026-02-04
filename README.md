# mei-codex

David's Obsidian vault — a second brain for managing projects, goals, and knowledge.

[GitHub Repository](https://github.com/dstanek/mei-codex)

## About Me

1. Husband and father of 4
2. Principal Software Engineer at [HPE](https://www.hpe.com/) (full-time)
3. Python instructor at Case Western Reserve University
4. Building an education business (Learn Fast)
5. Team manager for a club soccer team

## Purpose

This vault is my second brain, combining [PARA](https://fortelabs.com/blog/para/) with [Zettelkasten](https://zettelkasten.de/introduction/) principles.

## Organization

| Folder | Purpose |
|--------|---------|
| 00 Inbox | Unprocessed inputs — I process these myself |
| 01 Projects | Active and backlog projects with domain tags |
| 02 Areas | Ongoing responsibilities and goals |
| 03 Resources | Reference materials |
| 04 Archive | Completed/inactive projects |
| 05 TCP Evidence | HPE promotion planning |
| 07 Daily | Daily notes (optional) |
| 08 Topics | Tag Notes — topic definitions with linked content |
| 09 YT | YouTube content planning |
| 99 Copilot | Prompt library |
| 99 Meta | Templates, conventions, dashboards |

## Projects

### Naming Convention

| Location | Pattern | Example |
|----------|---------|---------|
| Obsidian | `Project - {name}` | `Project - Homelab` |
| Todoist | `{name}` under domain | `Homelab` under `Personal` |

### Domains

Projects are tagged with a domain in frontmatter:

| Domain | Description | Todoist Parent |
|--------|-------------|----------------|
| `personal` | Personal projects | Personal |
| `hpe` | Work projects | HPE |
| `cwru` | Teaching projects | CWRU |
| `learn-fast` | Education business | Learn Fast |

### Required Frontmatter

```yaml
---
type: project
status: active    # active, backlog, on-hold, archived
domain: personal  # personal, hpe, cwru, learn-fast
---
```

### GTD Next Actions Rule

> **Every project with `status: active` must have at least one task with a due date in Todoist.**

If an active project has no next action:
1. Add a next action to Todoist, OR
2. Change status to `backlog` or `on-hold`

Use the **Project Dashboard** (`99 Meta/Project Dashboard.md`) to review active projects.

## Todoist Integration

Tasks link to this vault via naming convention:
- Task format: `{Project Name}: {task description}`
- Example: `Homelab: Setup shelf for nodes`

This makes it easy to find related tasks and keeps both systems in sync.

## Working with Emmett

Emmett is my AI assistant who helps maintain this vault.

### What Emmett Does

- Creates PRs for organizational improvements
- Monitors GTD compliance (active projects need next actions)
- Suggests structural improvements
- Executes tasks labeled with `Emmett` in Todoist

### What Emmett Doesn't Do

- Process the Inbox (I do that myself — it's how I learn)
- Auto-generate content notes (those should be my thoughts)

### How to Request Help

1. Add a task in Todoist with the `Emmett` label
2. Emmett checks every few hours and works on labeled tasks
3. Results are reported via Telegram

### Commit Convention

Emmett's commits use the 50/72 rule and are prefixed with `emmett:`.

## Key Files

| File | Purpose |
|------|---------|
| `99 Meta/Conventions.md` | Detailed naming and organizational rules |
| `99 Meta/Project Dashboard.md` | Dataview dashboard for GTD review |
| `99 Meta/Templates/` | Note templates |
| `02 Areas/5 Year Goals.md` | Long-term goals |
