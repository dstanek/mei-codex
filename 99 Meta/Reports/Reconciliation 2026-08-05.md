---
type: meta
created: 2026-08-05
---
# Reconciliation Report — 2026-08-05

First pass under [[Project Reconciliation]]. **Nothing has been changed.** Every item below is a proposal awaiting approval.

Sources: 27 notes under `01 Projects/`, `get-overview` (34 Todoist projects), and Drive `1. Projects/` (`14Kt3GswyG0moflC5iLEG769Rov879PiA`).

## Summary

| | Count |
|---|---|
| Active Obsidian projects | 7 (2 are duplicates) |
| …with a Todoist link in frontmatter | **0** |
| …with a Drive link in frontmatter | **0** |
| …with a Todoist project that exists | 4 (unlinked, name-matched) |
| …with a Drive folder that exists | 1 (unlinked, name-matched) |
| …satisfying the GTD rule | **1 of 5** distinct active projects |
| Todoist projects with no domain parent | 7 |

No project in the vault carries a `todoist` or `drive` value, because the fields didn't exist until today. Every binding below is **proposed from a name match** and needs your confirmation — per the procedure, name matching may not assert a binding.

---

## 1. Active projects — proposed bindings

| # | Obsidian | Domain | Todoist | Drive | Proposed action |
|---|---|---|---|---|---|
| 1.1 | `Homelab/` | personal | `Personal › Homelab` `6fwMM9662W23qXCH` | ❌ | Confirm binding, backfill `todoist`; create `1. Projects/Personal/Homelab/` |
| 1.2 | `Learn AI/` | personal | `Personal › Learning › AI` `6fxHwJVqv4j6982q` | ❌ | **Name drift + nesting.** Pick a canonical name; move out from under `Learning` to sit directly under `Personal`; create Drive folder |
| 1.3 | `HPE - Python Linting Rules/` | hpe | ❌ none | ❌ | Create Todoist project under `HPE`; create `1. Projects/HPE/`; add a due-dated next action |
| 1.4 | `CWRU Spring 2026/Python Intro Course Ideas.md` | cwru | `CWRU › CWRU Spring 2026` `6fgpC4Ph5m7Xxmj8` | ❌ | **Granularity mismatch** — see §4.1. Not a clean binding |
| 1.5 | `YTChannel/` | learn-fast | `Learn Fast › YouTube Streaming` `6fHh2xqrrWrg7g8x` | `1. Projects/YTChannel` `1PrTZmsM453LSEKwjDebWdhPU9WdRXbcA` | **Name drift 3 ways.** Both counterparts exist; the URLs are in prose, not frontmatter. Pick a canonical name, then backfill both |

### 1.5 detail — the three names

| System | Current name |
|---|---|
| Obsidian | `YTChannel` |
| Todoist | `YouTube Streaming` |
| Drive | `YTChannel` |

Two of three say `YTChannel`. **Proposed canonical: `YTChannel`** — rename the Todoist project. Say the word if you'd rather go the other way.

---

## 2. Duplicates

| # | Finding | Proposed action |
|---|---|---|
| 2.1 | `YouTube Streaming/` and `YTChannel/` are near-identical folders, both `status: active` `learn-fast`. They differ in exactly one way: `YTChannel/Planning.md` has a `## Todoist` section with three project URLs; `YouTube Streaming/Planning.md` does not. `Resources.md`, `Things to investigate.md`, `Video Editing.md` are byte-identical. | **Keep `YTChannel/`** (strict superset, and it matches the Drive folder name). Delete `YouTube Streaming/` |
| 2.2 | `Python Intro Course/Python Intro Course Ideas.md` and `CWRU Spring 2026/Python Intro Course Ideas.md` are **byte-identical**. `Python Intro Course/` contains nothing else. | Delete `Python Intro Course/`; keep the copy under `CWRU Spring 2026/` pending §4.1 |

---

## 3. GTD rule — active projects need a due-dated task

| # | Project | Tasks | Due-dated | Status |
|---|---|---|---|---|
| 3.1 | `Homelab` | 18 | **0** | ❌ Violation |
| 3.2 | `Learn AI` → Todoist `AI` | 9 | **0** | ❌ Violation |
| 3.3 | `Python Intro Course Ideas` → `CWRU Spring 2026` | — | **0** | ❌ Violation |
| 3.4 | `HPE - Python Linting Rules` | — | — | ❌ No Todoist project at all |
| 3.5 | `YTChannel` → `YouTube Streaming` | — | 6 | ⚠️ Satisfies the rule, but **all six are overdue** (2026-07-15 … 2026-07-24) |

Per [[Conventions]], each of 3.1–3.4 needs either a next action with a due date or a drop to `backlog` / `on-hold`. 3.5 needs rescheduling.

---

## 4. Structural findings — Obsidian

| # | Finding | Proposed action |
|---|---|---|
| 4.1 | `CWRU Spring 2026/` holds **two distinct projects** (`Browser-Based Jupyter` backlog, `Python Intro Course Ideas` active) plus two frontmatter-less notes (`Spring Schedule.md`, `Token Usage.md`). It's a container, not a project. | **Needs your decision.** Either (a) split into two sibling project directories and move the two loose notes to whichever owns them, or (b) make `CWRU Spring 2026` itself the project and demote the two notes to support notes. Option (b) matches the existing Todoist project |
| 4.2 | 11 bare `.md` files sit directly in `01 Projects/` | Promote each to `{Name}/{Name}.md` |
| 4.3 | 6 folder-projects have an anchor note not named after the folder: `YTChannel/Planning.md`, `YouTube Streaming/Planning.md`, `wms/Features.md`, `stencil/Alternatives.md`, `Setup Home Assistant/Home Assistant.md`, `Python Intro Course/Python Intro Course Ideas.md` | Rename each to match its folder |
| 4.4 | 8 notes under `01 Projects/` have no frontmatter: `CWRU Spring 2026/{Spring Schedule, Token Usage}`, and `{YTChannel, YouTube Streaming}/{Resources, Things to investigate, Video Editing}` | Classify as support notes — no frontmatter needed once their parent folder has an index note. Confirm none is secretly a project |
| 4.5 | `01 Projects/Personal/Terraform Course/` is empty; `01 Projects/Personal/` contains only that empty dir | Delete both — leftovers from the abandoned domain-folder attempt |
| 4.6 | `HPE - ` filename prefixes (`HPE - Generate Documentation`, `HPE - Python Linting Rules`) duplicate `domain: hpe` | Drop the prefix: `Generate Documentation/`, `Python Linting Rules/` |

### Proposed final shape of `01 Projects/`

```
Archive Family Videos off Facebook/   Homelab/                  Water Leak Detection/
Closet Doors/                         Kubernetes Operator/      wms/
Garage Door Automation/               Laundry Basket Rack/      YTChannel/
Generate Documentation/               Learn AI/                 Raised Flower Beds/   (new, §5.2)
Home Assistant/                       Python Linting Rules/
Browser-Based Jupyter/                stencil/
Totem Keyboard/                       + whatever §4.1 resolves to
```

---

## 5. Drive

| # | Finding | Proposed action |
|---|---|---|
| 5.1 | `1. Projects/` has no domain subfolders | Create all seven: `Personal`, `HPE`, `CWRU`, `Learn Fast`, `Preheat to 350`, `Paige Creations`, `Freelancing` |
| 5.2 | **`Raised Flower Beds`** (`1_w-36wdFvtDdKB1UJSDLWGJDgVwYvHC8`) is a real project (your call) with no Obsidian note and no Todoist project | Create both, `domain: personal`; move the folder to `1. Projects/Personal/` |
| 5.3 | Four stale folders, untouched since ≤ May 2025: `Sawyer's Play`, `Productivity Setup`, `Xander's Training`, `Sawyer's Training` | Move to `4. Archive/` (`1S5YKDU-Xa9oc-lwnvSQOufX9nZmKcAmT`) |
| 5.4 | `YTChannel` (`1PrTZmsM453LSEKwjDebWdhPU9WdRXbcA`) sits at `1. Projects/` root | Move to `1. Projects/Learn Fast/` |
| 5.5 | Root-level `WMS` (`1M6Aa7YNV1dcI7QokybnxgeHAyBOszSmB`) matches `01 Projects/wms/` (backlog, personal) | Confirm binding. Case differs — pick `WMS` or `wms` as canonical. Since backlog, moving it under `1. Projects/Personal/` is optional |
| 5.6 | `4. Archive/CWRU-Python` (`1PJzkFymwEdTqsfMYgU6aYvpAztTrkYlZ`, 2018) | None — correctly archived. Informational |

> **Note on 5.1 and 5.3–5.4:** these are *moves*, and Drive moves aren't reversible by URL. Nothing here executes without your explicit go-ahead.

---

## 6. Todoist

### 6.1 Domain parents

| Domain | Current state | Proposed action |
|---|---|---|
| `personal` | `Personal` `6CrgJQx8x2Pj59Mq` | ✅ none |
| `hpe` | `HPE` `6VJV6WFQ8837mrgM` | ✅ none |
| `cwru` | `CWRU` `6fCMPq9f4CVMGmP7` | ✅ none |
| `learn-fast` | `Learn Fast` `6fgpCJHmFgJc7qx8` | ✅ none |
| `preheat-350` | `PT 350` `6fgpCGf5HC2WHrRv`, top-level | Rename → `Preheat to 350` (matches Drive `5. Preheat to 350`) |
| `paige-creations` | ❌ does not exist | Create as a top-level parent |
| `freelancing` | `Freelancing` `6fwPWr428M6qVxrV`, top-level | ✅ already correct — it *is* the domain parent |

### 6.2 Orphans — top-level projects with no domain parent

| # | Project | ID | Proposed action |
|---|---|---|---|
| 6.2.1 | `Career` | `6fh87g87cwJgW2fF` | Move under `HPE`. `02 Areas/5 Year Goals.md` links to it as "HPE › Career", so it was there before |
| 6.2.2 | `Promotion` | `6fHh374JxHjVGR8h` | Move under `HPE` — needs confirmation |
| 6.2.3 | `Zephyr` | `6fCMPG7fcRX7w99j` | Move under `HPE` — **guessing**, tell me the right domain |
| 6.2.4 | `Simple Chart Upgrades` | `6h5Mh8FC2xjcFP8q` | Domain unknown — tell me |
| 6.2.5 | `Team Setup Guide` | `6h9c2vqcC693fWWr` | Todoist's own onboarding sample (sections "Try it! ⭐️", "Todoist 101 📚"). Propose deleting |
| 6.2.6 | `PT 350` | `6fgpCGf5HC2WHrRv` | Becomes a domain parent — see §6.1 |
| 6.2.7 | `Freelancing` | `6fwPWr428M6qVxrV` | Becomes a domain parent — see §6.1 |

### 6.3 Misfiled

| # | Finding | Proposed action |
|---|---|---|
| 6.3.1 | `Personal › Jewelry Displays` `6h5fPCX4JpFF2fQ3` is jewelry work filed under Personal, while Drive has `6. Paige Stanek/Creations/` and `3D Modeling/PaigeStanekCreations` | Move under the new `Paige Creations` parent |
| 6.3.2 | `Personal › Learning › AI` is two levels deep; `Learn AI` should sit directly under its domain parent | Move `AI` up to `Personal`, or leave `Learning` as an intentional grouping — your call |

---

## 7. Data fixes — Obsidian

| # | File | Finding | Fix |
|---|---|---|---|
| 7.1 | `HPE - Generate Documentation.md` | `domain: HPE` breaks the lowercase enum | → `hpe` |
| 7.2 | `Closet Doors.md` | `type: [project]` is a YAML list, should be a string | → `type: project` |
| 7.3 | 20 of 22 project notes | No `priority` — this is why the Dashboard's *Projects To Update* pane matches nearly everything | Backfill during restructure |
| 7.4 | 15 of 22 project notes | No `title` or `created` | Backfill |
| 7.5 | `04 Archive/CFSC Team Manager.md` | `status: active` inside the archive | → `archived` |
| 7.6 | `04 Archive/` | `CFSC Team Manager.md` at root; `Travel - Disney 2025.md` in `04 Archive/Projects/` | Standardize on `04 Archive/Projects/`, as directories |

---

## 8. Informational — no action

Todoist projects with no Obsidian counterpart. **Allowed by the contract** — Obsidian is authoritative for existence, and Todoist may hold extras.

`Small shed`, `Basement Flooding`, `Replace Evernote`, `Get Hot Tub Working`, `Jewelry Displays`, `Repeat - the checklist app`, `Someday / Maybe`, `Goal Setting`, `Branding`, `Learning`, `Claude Code`, `Terraform Course`, `Landing page`, `Updated Python class`, `GenAI-Workflow`, `Potential Content`, `Adjunct Council`, `HPE › Someday/Maybe`

Several look like genuine projects (`Replace Evernote`, `Basement Flooding`, `Terraform Course`). If any should exist in Obsidian, say so and it moves out of this section.

---

## Decisions needed

Blocking, in rough priority order:

1. **§4.1** — how to resolve `CWRU Spring 2026/` (container vs. project)
2. **§1.5** — canonical name for YTChannel / YouTube Streaming
3. **§6.2.3–6.2.4** — domains for `Zephyr` and `Simple Chart Upgrades`
4. **§6.3.2** — keep the `Learning` grouping in Todoist, or flatten it
5. **§5.5** — canonical case for WMS / wms
6. **§2.1, §2.2, §6.2.5** — confirm the deletions

Everything else is mechanical and can proceed on a single go-ahead.
