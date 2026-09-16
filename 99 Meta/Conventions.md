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
| `area`       | —                    | Ongoing responsibility with no completion condition; lives in `02 Areas/`, and has **no** Todoist project *(see [[#Areas]])* |
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
| Google Drive         | `01 Projects/{Domain}/{short name}/`        | `01 Projects/Personal/Homelab/`    | Optional  |

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

### Folder-name index vs. `index.md`

The vault uses both, deliberately. The rule is whether you ever **link to the folder itself**:

| The folder is | Index file | Because |
|---|---|---|
| **A thing** — a project, an area | `{Folder}/{Folder}.md` | You write `[[Homelab]]`, `[[Career]]` |
| **A container** — a YT series, a vault section | `index.md` or `README.md` | You never link to the container by name |

So `01 Projects/Homelab/Homelab.md` and `02 Areas/Career/Career.md`, but
`09 YT/Pre-Commit/index.md` and `05 Foundary/README.md`.

**Why not `index.md` everywhere?** Obsidian resolves wikilinks by filename across the whole vault. Thirty notes named `index` makes `[[index]]` ambiguous, forces `[[Homelab/index]]` everywhere, and fills the quick switcher and graph with identical nodes. It would also break existing queries silently — [[Topic]] runs `contains(file.tags, this.file.name)`, and under `index.md` that resolves to the literal string `index`, so the query returns nothing rather than erroring.

**The cost of this choice**, worth naming: renaming a project means renaming the **folder and the note together**. Doing one and not the other is the single most common structural break, which is why [[Project Reconciliation]] checks for a directory with no matching index note.

### When to use task prefixes

**Use prefix when:**
- Creating tasks for "Today" or aggregate views
- Quick capturing to Inbox (makes sorting easier)
- Task might appear in filters/searches

**Skip prefix when:**
- Creating tasks directly inside the project
- Context is already clear

## Drive File Naming

> **The folder supplies the context; the filename supplies what makes this file different from its siblings.**

`Soccer/2025 Season/Roster` beats `Soccer/2025-soccer-season-roster-final-v2`. If the folder already says it, the filename shouldn't repeat it.

| Kind of file | Pattern | Example |
|---|---|---|
| Google-native doc | `Title Case`, **no extension** | `Materials` — not `Materials.xlsx` |
| Point-in-time document | `YYYY-MM-DD Subject` | `2026-04-06 Roof Detail.png` |
| Annual or periodic series | `Subject YYYY` | `Letter From Santa 2018`, `Taxes 2025` |
| Build or versioned artifact | `{project}-{stage}{n}.{ext}` | `wms-alpha4.apk` |
| Brand or design asset | `{brand}-{asset}.{ext}` | `learn-fast-youtube-banner.afdesign` |
| Manual | `{Brand} {Model} Manual.pdf` | `Hayward DV1000 Manual.pdf` |
| 3D model | `{Object} v{n}.{ext}` | `Fridge Handle Cover v2.stl` |
| Photo set | folder carries context; keep camera names | `2025-11 Fall Session/IMG_6440.CR2` |

**Never:**

- `Untitled*`, `Copy of *`, a trailing ` (1)`
- OS and scanner defaults — `Screenshot 2026-08-13 at 12.19.48 AM.png`, `SKM_C3320i23051903560.pdf`
- Vendor hash suffixes — `Upper-Lower-4x-udpkvj.pdf`, `gridplates-400x322-Standard-4ba4d.stl`
- Doubled extensions — `Xander.jpg.jpg`
- An extension on a Google-native file. There is no file to have one
- Leading, trailing, or doubled spaces — these are invisible and they break sorting

### Renaming existing files

Rename when a name carries **no information**, or when you're moving the file anyway. Don't rename for tidiness alone — a name that is merely inconsistent is not worth the risk of breaking a link or a bookmark.

Three habits, learned the hard way:

**A filename is not evidence of what a file is.** `strategy.rst` was a ten-page Keystone federation design document. `Introduction to Programming` was the DESN 210 syllabus. `Untitled presentation` was a lecture deck. Open it before you judge it, and certainly before you delete it.

**Verify duplicates by content, never by size.** Two files of identical size can be unrelated; two copies of one document in different formats will always differ. Read both.

**A convention that looks inconsistent may be encoding something.** `04 Archive/Taxes/` mixes `2019 Expenses for Taxes` with `Taxes 2025` — not carelessness, but two document types: worksheets and filings. Understand a pattern before normalising it away.

## Domains

Domains connect Obsidian projects to Todoist parents and Drive folders. This list is closed — a project's `domain` must be one of these seven:

| Domain | Obsidian `domain:` | Todoist Parent | Drive Folder |
|--------|-------------------|----------------|--------------|
| Personal | `personal` | Personal | `01 Projects/Personal/` |
| HPE (work) | `hpe` | HPE | `01 Projects/HPE/` |
| CWRU (teaching) | `cwru` | CWRU | `01 Projects/CWRU/` |
| Learn Fast (business) | `learn-fast` | Learn Fast | `01 Projects/Learn Fast/` |
| Preheat to 350 (business) | `preheat-350` | Preheat to 350 | `01 Projects/Preheat to 350/` |
| Paige Creations (business) | `paige-creations` | Paige Creations | `01 Projects/Paige Creations/` |
| Freelancing | `freelancing` | Freelancing | `01 Projects/Freelancing/` |

Adding a domain means adding all five: the `domain:` value, a Todoist parent project, a `One-Off` child under it, a `Someday / Maybe` child under it, and a `01 Projects/` subfolder.

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

### Drive structure

`01 Projects/{Domain}/{Project}/` holds project-scoped downloads. `02 Areas/{Subject}/` holds evergreen per-focus material. Same split as the vault, one tier shallower.

> **One home per subject.** A subject has exactly one folder. Lifecycle is expressed by a **subfolder inside it**, never by a copy in another tier.

```
02. Areas/Soccer/
  CFSC HSB Spring 26/
  11B ECNL-RL Yellow/
  Archive/            <- closed seasons live here, not in 04. Archive/Soccer/
```

`04 Archive/` is reserved for subjects that are **entirely** done, with no live component at all — `Shoreline`, `DjangoBookReview`, `Consulting`.

The legacy roots `5. Preheat to 350`, `6. Paige Stanek` and `7. Learn Fast` predate this scheme and still hold per-focus material. Nothing new goes into them.

## Someday / Maybe

**Every domain has its own `Someday / Maybe`**, a child of the domain parent exactly like `One-Off`: things you might do and haven't committed to.

> **Nothing in Someday / Maybe has a date.** A date is a commitment. If it has one, it belongs in a real project or a `One-Off`.

Like `One-Off` it's a permanent bucket — it never completes, so the GTD rule, the stalled check and the missing-note check all skip it by rule, and it gets no Obsidian note and no Drive folder.

Because the domain is carried by *where the item lives*, items need no domain prefix. The project-prefix rule in [[#When to use task prefixes]] still applies if an item clearly belongs to a named project.

| Domain | `Someday / Maybe` project ID |
|--------|------------------------------|
| `personal` | `6fRrh8F4mjQ5987P` |
| `hpe` | `6VJRvvFRxRxpMgj2` |
| `cwru` | `6hF3VX9HhphWqwmV` |
| `learn-fast` | `6hF3VX84FvRXJm86` |
| `preheat-350` | `6hF3VX73rc7QM28H` |
| `paige-creations` | `6hF3VX9h3gFjJ3WH` |
| `freelancing` | `6hF3VX938w7wvjrX` |

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
drive: https://drive.google.com/drive/folders/{drive-folder-id}
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

## Areas

> **An Area has no Todoist project.** Its `todoist:` field stays empty — that's what distinguishes it from a project note, where the URL is required.

Todoist is the canonical list of *projects*, and an Area isn't one. Giving an Area a Todoist project creates something that can never satisfy the GTD rule, so it either shows up as permanently stalled or has to be special-cased forever.

> **An Area may be empty, and that is fine.** `Career` sat with no material for months and was still a real area of responsibility. An empty Area is not dead scaffolding, and reconciliation must never report it as such.

The failure that *does* matter looks similar and isn't: a subject whose folder is empty **while its material lives somewhere else**. Drive's `02 Areas/Soccer/` was empty while soccer files sat in four other folders across three tiers. Empty-and-waiting is healthy; empty-and-scattered is the defect.

An Area is a **directory with an index note of the same name**, the same layout as a project:

```
02 Areas/
  Career/
    Career.md           <- index note, type: area, todoist: empty
    Improvements.md     <- support note
```

```yaml
---
title: Career
type: area
status: active     # active or archived — an Area is never backlog or on-hold
domain: hpe        # one of the seven
todoist:           # always empty
drive:             # optional, same as projects
tags: []
---
```

**So where do the tasks go?** An Area doesn't hold tasks, because it isn't in Todoist. Its work surfaces as one of two things:

| The work is | Goes to |
|---|---|
| A concrete push with an end state | A real Todoist project *(see [[#Creating a new project]])*. `Career` → the `Promotion` project |
| Upkeep with no end state | That domain's `One-Off` *(see [[#One-Off Tasks]])* |

The Area note is where the *thinking* lives — what you're aiming at, what you've learned, which projects have come out of it. Link them from the note.

Because Areas live outside `01 Projects/`, reconciliation never scans them, so an empty `todoist:` is never reported as an unlinked note. That's the point: nothing to check, nothing to drift.

## Clarify

One tree drains every inbox — `00 Inbox/`, the Todoist Inbox, and the mail and read-later queues in [[Tools Matrix]]. Processing an item means reaching one of the five outcomes below and then taking it out of the inbox.

> **Nothing goes back in.** An item you've looked at and left in place is an item you'll pay the same decision for next week.

### Is it actionable?

**No** — pick one and move on:

| It is | Goes to |
|---|---|
| Worth keeping | A note — `03 Resources/` for reference, `08 Topics/` for a hub, `05 Foundary/` if it's an idea worth forging |
| Something you might do someday | That domain's `Someday / Maybe` — no date, no note *(see [[#Someday / Maybe]])* |
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

## Labels

> **A label answers "when *could* I do this?" — never "whose is it?"** Domain is the project's job; a label that repeats it is a second source of truth that nothing can check.

That's why there are no `HPE` / `CWRU` / `Personal` labels. The domain parent already says it, and a task's domain is wherever the task lives.

| Label | Means |
|---|---|
| `call` | Needs a phone call |
| `Outdoors` | Needs to be outside, and probably dry |
| `waiting` | Not yours to do *(see [[#Waiting For]])* |

Name labels **without** the `@`. Todoist displays the `@` itself and filter syntax adds it, so a label literally named `@call` has to be queried as `@@call`.

Keep the list short. A context earns a label only when you'd actually filter by it — if you've never once wanted "everything I could do while outside", that's a tag, not a context. `Emmett` exists as a delegation label but has never been used; it's kept, not endorsed.

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
- **A `waiting` task never satisfies the GTD rule**, whatever date it carries. If a project's only dated task is one you're waiting on, it has no next action — add one you *can* do, or move it to `on-hold`. Waiting is not progress. This is enforced, not just advised: `/project-review` and `/project-reconcile` both discount `waiting` tasks when deciding whether a project has a next action, and reconcile says so in the finding.

The three Today filters end in `& !@waiting`, so a delegated task drops out of your daily views and shows up only in Waiting For. `/project-review` makes the same split — waiting tasks are pulled out of Upcoming and Overdue into their own section, oldest first. Review it weekly *(see the Sunday block in `99 Meta/Templates/Daily Note.md`)*.

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

### How deadlines get checked

The `!no date` sweep sees **due dates only**, so a deadline-only task counts as undated for the GTD rule. That's intended — a project whose only date is a deadline has no plan — but it means deadlines need their own path. Two exist:

| Where | What it does |
|---|---|
| **Deadlines** filter (`!no deadline`) | Favourited in Todoist. Every task carrying a deadline, whenever it falls |
| `/project-review` | A **Deadlines** section for the next 14 days, flagging any deadline with no due date as unplanned |

Neither turns a deadline into a next action. A project can legitimately show up under *no next action* while holding a deadline next week — that pairing is the urgent case, not a contradiction.

`/project-reconcile` has no deadline finding, so a deadline-only task is silent there.

## Examples

### Creating a new project

Todoist first, because Todoist decides what exists.

1. **Todoist** — create project `Kitchen Remodel` under the `Personal` parent.
2. **Todoist** — add a next action with a due date: `Kitchen Remodel: Get contractor quotes`.
3. **Obsidian** *(only if you have thinking to capture)* — create `01 Projects/Kitchen Remodel/Kitchen Remodel.md` from the `Project.md` template, mirror `status`/`domain`/`priority`, and paste the Todoist URL into `todoist:`.
4. **Drive** *(only if you'll download material)* — create `01 Projects/Personal/Kitchen Remodel/` and paste its URL into `drive:`.

Steps 3 and 4 are optional. Step 1 is not — a project that isn't in Todoist doesn't exist. If you do create the note, pasting the `todoist:` URL is the step that gets skipped; without it the note shows in the Dashboard's *Notes Needing a Todoist Link* pane.

### Moving to backlog

1. **Obsidian** — change `status: active` → `status: backlog`
2. **Todoist** — remove due dates, or move tasks to `Someday / Maybe` *(which takes no dates — see [[#Someday / Maybe]])*

The `todoist` and `drive` URLs stay — they're still correct, just no longer required.

### Archiving

1. **Obsidian** — set `status: archived`, move the project directory to `04 Archive/Projects/`
2. **Todoist** — archive the project
3. **Drive** — move the folder to `04 Archive/Projects/{Domain}/` — the same path as `01 Projects/{Domain}/`, one prefix changed
