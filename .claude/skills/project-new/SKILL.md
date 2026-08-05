---
name: project-new
description: Create a new project correctly across Todoist, the Obsidian vault, and Google Drive - Todoist project under the right domain parent first, then a due-dated next action, then optionally the Obsidian note from the Project template and a Drive folder, with both URLs pasted back into the note's frontmatter. Use this whenever the user wants to start, add, set up, or kick off a new project, says "I'm starting X" or "new project for X", wants to turn an idea, note, or inbox item into a real tracked project, or asks where a new project should live. Enforces the canonical short name, the seven-domain enum, the 01 Projects/{Name}/{Name}.md layout, and the GTD rule that an active project needs a due-dated next action.
---

# Create a new project

**Read this first:** `.claude/skills/_shared/REFERENCE.md` — the domain table
with Todoist parent and Drive folder IDs, and the agent/script split. The rules
live in `99 Meta/Conventions.md` (see *Examples → Creating a new project*); read
it if anything here is ambiguous.

## Order matters

Todoist first, because Todoist decides what exists. A project that isn't in
Todoist doesn't exist, so nothing else can be created until it does.

1. **Todoist project** under the domain parent
2. **Todoist next action** with a due date
3. **Obsidian note** — optional, ask
4. **Drive folder** — optional, ask
5. **Paste both URLs** back into the note's frontmatter

Steps 3 and 4 are genuinely optional and must not happen by default. Conventions
is explicit: create a note when there's thinking to capture, a Drive folder when
there's material to download. Creating empty ones for symmetry is how the vault
fills with dead directories.

## Before creating anything

Settle these first — every one of them is expensive to change afterwards,
because the name ends up in three systems and Drive folders can't be renamed.

- **Canonical short name.** One name, reused everywhere. Short: `Homelab`, not
  `Homelab Setup and Configuration`. No `HPE - ` prefix — the domain already
  says that.
- **Domain**, one of the seven. Ask if it isn't obvious; don't guess.
- **Is it actually a project?** Two ways the answer is no, and both are common:
  - *No completion condition* → it's an Area. `02 Areas/` with `type: area`.
    Say so rather than creating a project that can never satisfy the GTD rule.
  - *Too small to deserve a project* → it's a task, and it belongs in that
    domain's `One-Off` (IDs in REFERENCE.md). "Fix fence" and "Organize under
    desk cables" don't need a project, a note, and a Drive folder. Offer this
    first when the request sounds like a single errand — one
    `add-tasks` call with `projectId` set to the domain's One-Off is the whole
    job, and it keeps the project list meaningful.
- **Does it already exist?** Check `get-overview` for a Todoist project with
  that name and glance at `01 Projects/`. Duplicates across systems are the
  most common mess this skill can prevent.

Then validate the name and check for collisions before touching Todoist:

```bash
python3 .claude/skills/project-new/scripts/new_project_note.py \
  --check --name "Kitchen Remodel" --domain personal
```

`--check` writes nothing. It catches a bad domain, a bad status, a
case-colliding folder, and a missing template — all cheaper to hear now than
after a Todoist project exists.

## Creating

### 1. Todoist project

```
mcp__todoist__add-projects   name: "<Name>", parentId: "<domain parent from REFERENCE.md>"
```

Note the returned project ID; its URL is
`https://app.todoist.com/app/project/{id}`.

Directly under the domain parent — one level, never nested inside another
project. And the project's own tasks go in the project: a domain parent holds no
tasks directly.

### 2. Next action

An active project must have at least one task with a due date — that's the GTD
rule, and a project created without one is already in violation.

```
mcp__todoist__add-tasks   content: "<Name>: <first physical action>",
                          projectId: "<new id>", dueString: "<natural language>"
```

Make it a real first step, not a placeholder. Ask the user what it is if you
can't tell. `dueString` takes natural language (`"tomorrow"`, `"next Friday"`).
Priority is `p1`–`p4` as a string, and only if the user asked — an unset
priority stays unset.

### 3. Obsidian note — ask first

*"Want a note for this, or is Todoist enough for now?"*

```bash
python3 .claude/skills/project-new/scripts/new_project_note.py \
  --name "Kitchen Remodel" --domain personal --status active --priority 2 \
  --todoist "https://app.todoist.com/app/project/6ABC"
```

This renders `99 Meta/Templates/Project.md` — the template is the source of
truth for the note's shape, so it is read at runtime rather than copied here.
Omit `--priority` when the user hasn't set one. The script refuses to create a
note without `--todoist`, because that URL is what makes it a project note
rather than an idea.

### 4. Drive folder — ask first

*"Will you be downloading material for this? I can make a Drive folder."*

```
mcp__claude_ai_Google_Drive__create_file
    name: "<Name>", parentId: "<domain drive folder from REFERENCE.md>",
    mimeType: "application/vnd.google-apps.folder"
```

Nothing needs to go inside it — a Drive folder is a bucket, and needs no index
file, README, or manifest. Get the name right the first time: the connector
cannot rename or move folders afterwards.

### 5. Paste the URLs back

If the note was created before the Drive folder:

```bash
python3 .claude/skills/_shared/scripts/set_frontmatter.py \
  "01 Projects/Kitchen Remodel/Kitchen Remodel.md" \
  --set drive=https://drive.google.com/drive/folders/1XYZ
```

Pasting the URL is the step that gets skipped, and skipping it is what puts the
note in the Dashboard's *Notes Needing a Todoist Link* pane. Verify with
`scan_vault.py --summary` that both IDs resolved.

## Report back

Say what was created and what wasn't, with the URLs and the note path — so the
user can click through and confirm. If you skipped the note or the folder
because they said no, say that too; it's a choice they may want to revisit.

## Related

- Something already exists in one system but not the others → `project-reconcile`
- "What should I work on" or "does this have a next action" → `project-review`
