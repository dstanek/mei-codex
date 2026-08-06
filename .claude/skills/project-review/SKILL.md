---
name: project-review
description: Daily project and task review across Todoist and the Obsidian vault - what's due today and tomorrow grouped by domain, what's overdue oldest-first, which active projects violate the GTD rule by having no due-dated next action (with concrete proposed next actions), which projects have stalled, and where Obsidian frontmatter has drifted from Todoist. Use this whenever the user asks what's on their plate, what's due, what's overdue, what they should work on, for a daily or morning review or standup or briefing, to check project health or which projects need attention or a next action, or to catch stalled projects - and any time an agent runs a scheduled daily check over Todoist plus the vault. Read-only; it proposes but never writes.
---

# Daily project review

Produce one skimmable read for a human over coffee: what's due, what's late,
what has no next action, what has gone quiet, and where the vault disagrees with
Todoist.

**Read this first:** `.claude/skills/_shared/REFERENCE.md` — the domain table,
the agent/script split, the remote JSON envelope, and the MCP call list. The
rules themselves live in `99 Meta/Conventions.md`; don't restate them from
memory, and read that note if a judgement call turns on one.

## Read-only

This review changes nothing. Proposing next actions is the job; adding them is
not. If the user then says "add those", do it — but the report itself always
lands with nothing mutated, and says so.

## How to run it

Scripts can't call MCP tools, so you collect and the script computes.

### 1. Collect (cheap sweep)

```
mcp__todoist__get-overview                          (no arguments)
mcp__todoist__find-tasks   filter: "!no date"       (paginate on cursor)
mcp__todoist__find-tasks   filter: "!no deadline"   (cheap — there are few)
mcp__todoist__find-tasks   filter: "@waiting"       (cheap — delegated items)
mcp__todoist__find-completed-tasks  since: <today minus stale-days>
mcp__todoist__find-activity  objectType: "task", dateFrom: <today minus stale-days>
```

`!no date` is the whole point of the cheap sweep: one filter answers overdue,
upcoming, *and* which projects satisfy the GTD rule. Deliberately skip the
`no date` sweep here — undated task descriptions are long and there are hundreds
of them, and you only need a few of those projects.

`!no deadline` is a second, small sweep because the first one cannot see
deadlines — `!no date` matches on due dates only. The script has its own lane for
these; see *Deadlines* below.

Write it all to a temp file in the envelope from REFERENCE.md.

### 2. First pass

```bash
python3 .claude/skills/project-review/scripts/review.py \
  --remote /tmp/todoist.json --out-json /tmp/analysis.json
```

The draft goes to stdout. It has a `<!-- NEXT-ACTION-PROPOSALS -->` marker where
your proposals belong.

### 3. Second pass, for the projects with no next action

The draft lists projects that came back with no due-dated task. You have nothing
about them yet, so fetch just those:

```
mcp__todoist__find-tasks   projectId: <id>          (one per listed project)
```

Append those tasks to `tasks`, set `"tasks_include_undated": true`, and re-run.
Now the analysis JSON carries each project's existing tasks and its note path,
which is what you need to propose something real.

Skip step 3 only if the list is empty. If it's very long, say so and handle the
worst offenders rather than fetching thirty projects one at a time.

### 4. Write the report

Take the draft and replace the marker with your proposals. Present it in the
conversation — it's meant to be read, not filed. Offer to save it if the user
wants a copy.

## Proposing next actions

This is the part that can't be computed, and the reason the script stops and
hands over. For each project with no next action, give **2–3 candidates**, each
a concrete physical action with a suggested due date:

- Read the project's existing tasks from `analysis.json` — the next action is
  usually the smallest undated task already sitting there, or the obvious first
  step of the largest one.
- If it has an Obsidian note (`note_path` in the analysis), read it. The note is
  where the thinking lives; a proposal drawn from it will be far better than one
  guessed from task titles.
- Prefer the smallest thing that unblocks the rest. "Email the contractor for a
  quote" beats "plan the remodel".
- Follow the task-prefix rule in Conventions.md: prefix with the project name
  when the task will show up in aggregate views.
- When a project looks like it shouldn't be active at all — a holding pen, or
  something with no completion condition — say so and propose `backlog`,
  `on-hold`, or moving it to `02 Areas/` instead of inventing an action for it.
  Conventions.md is explicit that an ongoing pursuit is an Area, not a project.
  Spell out what the Area move actually costs: an Area has **no** Todoist
  project, so its tasks have to be rehomed first — the ones with an end state to
  a real project, the upkeep to that domain's `One-Off` — and only then is the
  original project archived. Propose the rehoming, don't just name the folder.

Format each as a short bullet list under the project name, with the domain and
note path alongside. Two good candidates beat three where the third is filler.

## Tone and shape

Prose plus tight tables. The script's output is already close; keep it that way
when you assemble the final version.

- Lead with anything genuinely urgent — something due today, a project that's
  been silent for months — in a sentence or two before the tables.
- Don't restate a table in prose underneath it.
- Never fill in a blank. If `priority` is unset, it's unset; the script prints
  `—` and so should you. Inventing a plausible value is the one failure mode
  that makes the whole report untrustworthy.
- Keep the script's closing footnotes about what the run couldn't see. They're
  the difference between "clean" and "I didn't look".

## Options

- `--stale-days N` — silence before a project counts as stalled. Default 14.
- `--deadline-days N` — how far ahead deadlines are reported. Default 14.
- `--today YYYY-MM-DD` — pin the date, for testing or backfilling.
- `--out FILE` — write the draft instead of printing it.

## Drift is a real check, not a mirror

`status` has no Todoist field — it's *derived* (archived → `archived`,
due-dated task → `active`, otherwise `backlog`/`on-hold`). So `status: active`
on a project with nothing due-dated is a genuine contradiction, and the script
reports it. `backlog` and `on-hold` are interchangeable against Todoist, and
neither is drift against the other. See REFERENCE.md for the table.

## Deadlines

`review.py` renders the **Deadlines** section itself from the `!no deadline`
sweep — you don't assemble it by hand. It sorts by deadline, shows what each is
planned for, and counts anything past the horizon. `--deadline-days N` moves the
horizon (default 14).

Two things to say out loud when reading it back:

- **Deadline-only tasks.** The section marks these `**nothing**` under *Planned
  for*, and leads with the count. A deadline with no due date is a delivery date
  with no day set aside to hit it; the remedy is a due date, so propose one.
- **A deadline never satisfies the GTD rule.** `vaultlib.task_deadline()` is
  deliberately separate from `task_due_date()`, so a project can appear under
  *no next action* while holding a deadline next week. That combination is the
  urgent case — say both in the same breath rather than leaving them in
  different sections.

## Waiting For

From the `@waiting` sweep, add a short section listing what's been waiting
longest. `addedAt` is the best available age signal, since the label carries no
timestamp of its own.

The check that earns its place: **a `waiting` task does not count as a next
action.** The scripts don't know the label, so a due-dated `waiting` task makes
its project look healthy when it isn't. When a project's only due-dated task is
one being waited on, say so explicitly and propose either an action the user can
take or `on-hold`.

Don't propose chasing something delegated two days ago. A week of silence is
worth mentioning; a month is worth leading with.

## What's exempt

Every domain's `One-Off` bucket and its `Someday / Maybe` are skipped by rule —
permanent buckets that never complete, so the GTD and stalled checks don't apply.
Their tasks still appear under upcoming and overdue, which is where they matter.

That's the whole exemption list, and it's structural. If a run surfaces
something else that looks like a holding pen, the answer isn't to suppress it —
it's that the project is probably an Area (no completion condition), so propose
moving it to `02 Areas/`. Conventions.md is explicit about that test.
