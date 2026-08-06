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
| `content-idea` | `Content Idea.md`  | Video/article/course ideas; lives in `09 YT/Ideas/`      |
| `meta`       | —                    | Vault config and conventions                            |

## Content Ideas

Every content idea is one note in `09 YT/Ideas/`, flat — no subfolders. `content-type` and `status` do the grouping, and Dataview assembles the views in [[Content Ideas]]. Same principle as projects: the folder is dumb, the frontmatter is smart.

```yaml
---
title: Setup VSCode for Python Development
type: content-idea
content-type: long video    # short video, long video, article, course
status: seed                # see lifecycle below
domain: learn-fast
source: "https://..."       # often the only thing filled in at capture
created: 2025-12-10 12:50
tags: []
---
```

Create ideas with **Templater: Create new note from template** → `Content Idea`. It prompts for title, content type, and source, then files the note into `09 YT/Ideas/` itself. It refuses blank titles and duplicates, deleting the stub note rather than leaving an `Untitled` behind.

> Use *Create new note from template*, **not** *Insert template*. This template renders a whole note — frontmatter and body — so inserting it into an open note prepends a second copy of both. The template now refuses to run on any note that isn't empty, but the right command avoids the situation entirely.

### Status lifecycle

Mirrors the pipeline in [[YouTube Streaming]] — brainstorm, pick the best, research, script.

| `status` | Meaning |
|---|---|
| `seed` | Captured. Often just a source link and a title. |
| `selected` | Picked out of the pile as worth doing |
| `researched` | Topic understood, outline exists |
| `scripted` | Script written — ready to graduate |
| `published` | Shipped |
| `dropped` | Abandoned; kept so it doesn't get re-captured |

`seed` vs. `researched` is the distinction that matters day to day, since an idea starts as a bare link and gets filled in over time.

### Graduating an idea

> An idea leaves `09 YT/Ideas/` when it reaches `scripted`.

Move it into its series folder — `09 YT/{Series}/` — and add a link under that folder's `index.md` (`### Shorts` or `### Other Videos`). Script structure lives in [[Video Script Guide]], not in the idea note. The idea note carries `## Source` / `## Notes` / `## Outline`; the outline is the handoff.

A series folder is created the first time two ideas share a subject. One-offs can stay in `09 YT/Ideas/` at `published`.

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

## Clarify

One tree drains every inbox — `00 Inbox/`, the Todoist Inbox, and the mail and read-later queues in [[Tools Matrix]]. Processing an item means reaching one of the five outcomes below and then taking it out of the inbox.

> **Nothing goes back in.** An item you've looked at and left in place is an item you'll pay the same decision for next week.

### Is it actionable?

**No** — pick one and move on:

| It is | Goes to |
|---|---|
| Worth keeping | A note — `03 Resources/` for reference, `08 Topics/` for a hub, `05 Foundary/` if it's an idea worth forging |
| Something you might do someday | `Someday / Maybe`. No due date, no note |
| Neither | **Delete it.** This is the outcome that keeps the other four honest |

**Yes** — then how big is it?

| Size | Goes to |
|---|---|
| Under two minutes | **Do it now**, and never write it down |
| Someone else's move, not yours | Keep the task, label it `waiting` *(see [[#Waiting For]])* |
| One action | That domain's `One-Off`, with a due date *(see [[#One-Off Tasks]])* |
| Several actions, and you can say what "done" looks like | A project *(see [[#Creating a new project]])* |
| Several actions, no completion condition | An Area — `02 Areas/` with `type: area` *(see [[#Project or Area?]])* |

Every actionable outcome needs a domain, and it must be one of the seven *(see [[#Domains]])*. If you can't pick one, the item isn't clear enough to be actionable yet — sharpen it or let it go to Someday.

Filing something to the wrong home is cheap to fix later. Leaving it in the inbox is not.

## Waiting For

Some tasks are real commitments where the next move belongs to someone else — a quote you asked for, a review you're blocked on, a package in transit. They aren't done, and they aren't yours to do.

> A task labelled `waiting` is one you are **tracking, not doing**.

| | |
|---|---|
| Label | `waiting` — filter syntax is `@waiting` |
| Filter | **Waiting For**, favourited so it's in the sidebar |
| Lives in | Its own project, exactly where it would otherwise sit. The label is the only change |

Two rules keep it honest:

- **Say who and when.** `Kitchen Remodel: Contractor quote` is untrackable. Put the person and the date you asked in the task — the whole value of the list is knowing when it's time to chase.
- **A `waiting` task never satisfies the GTD rule.** If a project's only task is one you're waiting on, it has no next action. Either add one you *can* do, or move it to `on-hold` — that's what the status is for. Waiting is not progress.

The three Today filters end in `& !@waiting`, so a delegated task drops out of your daily views and shows up only in Waiting For. Review it weekly *(see the Sunday block in `99 Meta/Templates/Daily Note.md`)*.

## GTD Rule

> Every active Todoist project must have at least one task with a due date.

If an active project has no next action, either:
1. Add a next action, or
2. Change status to `backlog` or `on-hold`

The rule is about **Todoist**, since that's where projects live. Every project note in `01 Projects/` must also carry a `todoist` URL that resolves. See [[Project Reconciliation]] for how both get checked.

### Due dates vs. deadlines

Todoist has two date fields, and they mean different things. Using one for both jobs is what makes a Today view stop being trustworthy.

| Field | Means | Set by |
|---|---|---|
| **Due** | *When I intend to work on this.* A plan, and mine to move | `dueString` — natural language (`"tomorrow"`, `"next Friday"`) |
| **Deadline** | *When this is due to the outside world.* A constraint, not mine to move | `deadlineDate` — ISO 8601 (`"2026-08-14"`) |

> Only **due** satisfies the GTD rule. A deadline is a fact about the world; a due date is a commitment to act.

That's deliberate. A project whose only date is a deadline has a delivery date and no plan for meeting it — exactly the state the GTD rule exists to catch. Give it a due date and it passes honestly.

The practical consequences:

- **Rescheduling a due date is free.** It's a plan meeting reality. Moving a *deadline* is a real event — usually a conversation with someone.
- **Don't put an external date in `due` just because it's a deadline.** Set `deadline` to the real date, then set `due` to the day you'll actually do the work. They're often weeks apart.
- **Most tasks need no deadline at all.** Set it only when something outside you cares about the date.
- Always move dates with `reschedule-tasks`. `update-tasks` replaces the whole due string and destroys recurrence.

### Deadlines are not yet in the automated checks

The review and reconcile sweeps filter on `!no date`, which sees **due dates only**. A task carrying a deadline and no due date is invisible to them — it counts as undated.

Until that's fixed, one filter catches them:

```
!no deadline
```

`Raised Flower Beds` shows why this matters. *Make sure the existing structure is level* has a deadline of 2026-08-07 and no due date, while *Add a second layer* is due 2026-08-09 — so the review proposes the second layer and never mentions the levelling that has to happen first.

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
