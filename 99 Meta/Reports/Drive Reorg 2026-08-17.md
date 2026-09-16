---
type: meta
---
# Drive Reorg — 2026-08-17

Deep audit of Google Drive organization (phase 1: folders) and naming (phase 2), going
a layer below the 2026-08-05 [[Reconciliation 2026-08-05|reconciliation]], which fixed
only the top-level skeleton.

Coverage: ~292 folders, all of `00.`–`04.`, the legacy roots, and My Drive root, mapped
to full depth. `02.`/`03.`/`04.` alone came to 46 folders and 215 files.

> **Nothing in Drive has been changed.** Phase 0 (vault doc corrections) and Batch A
> (sharing audit) are complete and recorded below. Everything under *Proposed batches*
> awaits approval. The **Change log** at the bottom is empty.

**Out of scope by request:** `5. Preheat to 350` and `6. Paige Stanek`. Nothing proposed
here touches them. They are mentioned twice below only where they explain a duplicate
elsewhere.

---

## Headline

Drive has a correct, nearly empty filing system, and separately a root folder holding
**90 loose files** spanning 2012–2026 that does the filing system's actual job.

`01. Projects/` holds **10 files** across 7 domain folders, 5 of them empty; all seven
were batch-created on 2026-08-05 in a **12-second window** (19:38:26–19:38:37) and five
were never touched again. `00. Inbox/` — the folder whose entire job is catching unfiled
things — has been empty since it was created in March 2026.

The lifecycle tiers have also stopped meaning much. `02. Areas/Soccer` and
`02. Areas/Career` are empty shells; `04. Archive/Lifting` was both larger and *more
recent* than the `02. Areas/Lifting` that supposedly replaced it; and `04. Archive/Force`
held a soccer how-to opened in April 2026.

> **Correction.** An earlier draft called `04. Archive/Taxes` the most active folder in
> the Drive, on the strength of five documents created or edited on 2026-08-17. That
> reading was wrong: those edits were the user preparing for *this* reorg, so the
> timestamps measure my own process, not a live workflow. **Taxes stays in
> `04. Archive/`** by the user's decision. Recorded here because it's the kind of error
> worth not repeating — `modifiedTime` is not evidence of liveness when someone has just
> been tidying.

> The operative sorting rule across all three tiers is **topic, not lifecycle**. So
> neither "is this still live?" nor "where does a new file go?" can be answered from the
> path — which is the whole point of having tiers.

| | |
|---|---|
| Folders owned | ~292 |
| Loose files at My Drive root | **90** |
| Files in all of `01. Projects/` | **10** |
| Empty domain folders under `01. Projects/` | 5 of 7 |
| Files in `00. Inbox/` | **0** |
| Project/Area notes carrying a `drive:` URL | 2 of 21 |
| Files with an ISO `YYYY-MM-DD` prefix | **0 of ~305** |

---

## Phase 0 — vault doc corrections (DONE)

| File | Change |
|---|---|
| `99 Meta/Project Reconciliation.md` | Replaced the false "connector cannot move, rename, or delete" claim with what the tools actually do, and stated that reconciliation stays read-only by *rule*, not tool limitation |
| `99 Meta/Project Reconciliation.md` | `1. Projects/` → `01. Projects/` (3 places) |
| `99 Meta/Conventions.md` | `1. Projects/` → `01. Projects/` (12 places), `4. Archive/` → `04. Archive/` |
| `99 Meta/Conventions.md` | Frontmatter example leaked the real `YouTube Streaming` folder ID as `Homelab`'s `drive:` — replaced with `{drive-folder-id}` |
| `99 Meta/Templates/Project.md` | `1. Projects/` → `01. Projects/` in the GTD reminder |
| `.claude/skills/_shared/REFERENCE.md` | `1. Projects/` → `01. Projects/`, `4. Archive/Projects/` → `04. Archive/Projects/` |

`domains.json` needed **no** changes — all seven Drive folder IDs verified live and
correctly placed. Dated reports were left alone; they record what was true when written.

**The connector's real capabilities:** `create_file` creates files and folders;
`update_file` renames via `title` and moves via `parentId` (replacing the existing
parent); `trash_file` trashes, recoverable 30 days; `copy_file` copies.

## Batch A — sharing audit (DONE, read-only)

Checked because a reorg moves sensitive material around, and "Archive" invites
low-scrutiny sharing.

| Checked | Result |
|---|---|
| 8 identity/household files at root — 4× driver's license, `GasBill.pdf`, `Citizens_united.pdf`, `PropertySurvey.pdf`, `SKM_C3320i23051903560.pdf` | ✅ owner only |
| `04. Archive/Taxes` — 14 files, household financial + identity detail | ✅ owner only |
| `03. References/CFSC HSB Spring 26` — roster exports carrying **minors' full names, birthdates, registration IDs** | ✅ owner only |
| `04. Archive/Soccer` — same kind of roster printout | ✅ owner only |
| `03. References/Case Final Project Share` | ✅ owner only |

**Nothing is exposed.** No link sharing, no additional users anywhere. Worth re-checking
after any reorg, since folder-level shares are what leak this material.

> ⚠️ One ownership note: the folder `03. References/Case Final Project Share` is yours,
> but the **files inside it are owned by `das311@case.edu`** — a student. They can't be
> renamed or trashed by you, only unshared. Treat that subtree as read-only.

---

## Finding 1 — the root is the real inbox

90 loose files, 2012–2026, never filed. Grouped by where they belong:

| Group | Count | Examples (verbatim) |
|---|---|---|
| 3D print models | 9 | `Hook.3mf`, `hooks.step`, `hooks.stl`, `cyl.3mf`, `dress_cookie_cutter.stp`, `Paige Coin2.3mf`, `Paige Coin3.3mf`, `shapr3d_export_2025-09-26_10h51m.3mf`, `Outside Fridge Handle Cover2.stl` |
| Learn Fast brand assets | 7 | `am.afphoto`, `am-gear.afphoto`, `am.png`, `am-gear-192x192.png`, `am-500x451.png`, `faq.png`, `YouTubeLearnFastBanner.afdesign` |
| Identity & household records | 8 | `license-front.jpg`, `license-back.jpg`, `LicenseFront.pdf`, `LicenseBack.pdf`, `GasBill.pdf`, `Citizens_united.pdf`, `PropertySurvey.pdf`, `SKM_C3320i23051903560.pdf` |
| Kids' school | 4 | `MHS Honor Roll -1st Quarter 2025-2026 .docx`, `MHS Honor Roll -3rd Quarter 2025-2026 .docx`, `MHS Cast Lists 25-26`, `SAWYER STANEK Conference Form` |
| CWRU / teaching / hiring | 8 | `Introduction to Programming`, `Rubric`, `CWRU Rec of Me`, `David Stanek LoC.docx`, `Skillshare Class Outline Template`, `ListComprehensionsAndGenerators`, `Developing OpenStack`, `Dev Test` |
| Soccer / CFSC | 2 | `U13 through 15 Personal Workout Program CFSC 2024`, `Force Team Manager Duties` |
| Finance | 5 | `Finance`, `Tickets`, `Sadie Budget`, `Copy of Family Budget Planner - Generic`, `Household_Budget_Worksheet_Downloadable-6.xls` |
| Freelance mural job (2024-06) | 3 | `Mosman Mural Contract `, `Mural Contract `, `exhibit1.JPG` |
| Appliance manuals | 2 | `samsung-fridge.pdf`, `briggs-stratton-4a23a68885da13beb63920e7f44c23f8.pdf` |
| AI-newsletter freebies | 4 | the four `Copy of HubSpot …` sheets |
| Fossils, 2012–2019 | ~15 | `strategy.rst`, `report.csv`, `Open_Government.mobi`, `Letter From Santa`, `Letter From Santa 2019`, `Final Orchard Program`, `Lifehacker Daily Personal Inventory [Daily Personal Inventory]`, `Ideal Protein Food`, `Electronics Inventory`, `The Zen of Python.mm` |
| Misc / unclear | ~10 | `Edited Stuart_abstract final`, `zoom-roof.png`, `full-size-roof.png`, `sawyer.jpg`, `kpop png`, `IMG_20250530_183352.jpg`, `Shipping Label.pdf`, `The ultimate Docker  Container Book.pdf`, `Xander.jpg.jpg`, `Untitled spreadsheet` |

### What the opaque ones actually are

Read directly, since the titles say nothing:

| File | Actually |
|---|---|
| `Untitled spreadsheet` | A Venmo/checks income ledger — ~$6,546 in against $355 expenses. A side-hustle or team-collection tally |
| `Finance` | A mortgage refinance model: current loan vs 30-yr vs 15-yr, HELOC interest, $194,194 TCO delta |
| `Tickets` | An event ticket roster — Fri/Sat/Sun names, headcounts 17/2/3, $181.80 total |
| `Rubric` | A grading rubric for a student programming project, Expert-5 → Attempted-1 |
| `Dev Test` | A hiring take-home you authored — binary-subtree and spiral-print problems |
| `Edited Stuart_abstract final` | **Someone else's paper.** A Kent State architecture abstract on the exhibition *Rude Forms Among Us*, by William Stuart, 2025-12-09 |
| `tmp/1.png`–`9.png` | One 9-page image set, all sharing source timestamp 2026-01-13T19:47:00Z — a single scan dumped whole |

### True duplicates at root

| Files | Evidence |
|---|---|
| `image2vector.svg` × 2 | Identical title, identical size (385,058 bytes) |
| `am.png` / `am-500x451.png` | Identical size (168,096 bytes) |
| `Untitled Diagram.html` × 2 | Same name, different content (2,982 vs 1,253 bytes) |
| `resume`, `resume.doc`, `Copy of resume` | Three resumes, 2012 |
| `Developer Take Home Test - Rackspace.docx` × 2 | One Google Doc, one `.docx` |
| `RecTemplate.docx`, `Copy of RecTemplate.docx` | Both 294,942 bytes |
| MHS honor roll 2024-2025 | One `.docx` **plus two shortcuts**, one prefixed `Copy of … (1)` |
| Driver's license | Same document twice in two formats (`*-front/back.jpg` and `License*.pdf`) |
| `hooks.stl` / `hooks.step` / `Hook.3mf` | Same object, three formats, inconsistent case |

---

## Finding 2 — Soccer / Lifting / Diet: three different problems

My plan assumed these might be redundant copies. **They are not.** Verified: **zero title
collisions across any of the seven folders — no byte-identical pair exists.** A merge
would not collapse a single file. Each subject needs a different fix.

### Soccer — scattered across **six** folders in three tiers

| Location | State |
|---|---|
| `02. Areas/Soccer` | **EMPTY.** Created 2024-01-27, never written to |
| `03. References/Soccer` | 1 file, and it's a **shortcut** — a bookmark masquerading as a folder |
| `03. References/CFSC HSB Spring 26` | **LIVE, 2026** — current season compliance forms + roster exports |
| `04. Archive/Soccer` | 3 files, 2017 schedules + a 2023 roster card. Genuinely dead |
| `04. Archive/Force` | **LIVE, 2025** — `Team Manager Playmetrics Direct Pay HOWTO`, opened 2026-04 |
| `8. Cabinet/11B ECNL-RL Yellow/` | **LIVE, 2026** — current team, `Player Headshots/` |

The designated home is empty and the two live pieces are in Archive and References. Fix
is **delete + relocate**, not merge.

### Lifting — a failed split where **Archive won**

`04. Archive/Lifting` has 24 files, newest 2024-01. `02. Areas/Lifting` has 6, newest
2023-09. The archive is 4× larger *and more recent* than the area that replaced it, and
holds all the real training logs and program spreadsheets.

What's left in the "area" isn't even lifting: `Wonder Slim Inventory` and `Nutrition Plan`
are diet, and `Screenshot (Dec 8, 2021 00:57:09)` is a "how to do more pull-ups"
social-media graphic. There is no active/historical boundary — 2022 and 2024 logs sit in
Archive while a 2021 nutrition sheet sits in Areas.

A **fourth** lifting pile exists: `02. Areas/Lifting/Plans/` (5 folders, 12 files, all
loaded 2024-01-27) holds vendor programs of the same kind as
`03. References/BLS Bonus - Legion/Workout Routines/` — different vendors, so not the
same files, but the same category split across two tiers for no reason.

### Diet — a **legitimate** split; leave the boundary alone

`02. Areas/Diet` is live and coherent (9 files, `Weight Loss 2025` edited 2025-04, weight
tracking only). `04. Archive/Diet` is one 2015 macro sheet. Clean boundary, ten years
apart, no overlap. **This is the one that's working.**

Two strays to fix regardless: a `Diet` spreadsheet (2200-cal meal plan) is stranded in
`04. Archive/Lifting`, and `Areas/Diet` has internal sprawl — 4 parallel `BWS_Data*.csv`
exports and 4 parallel weight trackers (`Weight Tracking`, `Weight Loss 2025`,
`Body Weight Tracking (David)`, `(Tracy)`).

---

## Finding 3 — the tiers are inverted

**Live work sitting in `04. Archive`:**

| Item | Evidence |
|---|---|
| ~~`Taxes`~~ | ~~5 documents edited today~~ — **withdrawn.** Those edits were reorg prep, not a live workflow. `Taxes` **stays in `04. Archive/`**, user's decision. The folder is a completed annual series that happens to get referenced, not active work |
| `Force` | `Team Manager Playmetrics Direct Pay HOWTO`, edited 2025-06, **opened 2026-04** — months before this reorg, so this one is genuine. Moved to Soccer in Batch B |
| `Lifting` | Newer than its Areas counterpart (see above) |
| `Projects` | Created 2026-08-05 — material moved *into* Archive twelve days ago. Holds `Sawyer's Training/` and `Xander's Training/`, one spreadsheet each: two folders wrapping one file apiece |

**Archive material sitting in `02. Areas` / `03. References`:**

| Item | Evidence |
|---|---|
| `02. Areas/Talks` | Nothing since 2017 |
| `02. Areas/Career` | **EMPTY**, created 2026-06 |
| `03. References/End68` | Nothing since 2017 — defunct nonprofit's letterhead, poster, deck |
| `03. References/BLS Bonus - Legion` | Entire 7-folder / 23-file subtree frozen at its 2019-10-05 bulk-import timestamp; deepest folders last *viewed* in 2019 |
| `03. References/Case Final Project Share` | Dead since Nov 2024. 3-level single-child chain, files owned by a student |

**Correctly filed, no action:** `03. References/Manuals` (actively added through 2025 —
the one folder unambiguously right for its tier), `03. References/Family` (birth
certificates), `04. Archive/Diet`, `HPE`, `Electrical Issues`, `Disney`,
`DjangoBookReview`, `CWRU-Python`, `Shoreline`, `O'Reilly Book Proposal`, `Consulting`
(2008–2010, the oldest content in the Drive).

Also: **`Taxes 2022` is missing** from an otherwise unbroken 2012–2025 run. And
`04. Archive/Vacations` holds one Cape Coral file while `04. Archive/Disney` holds 8 of
the same activity — vacations are split for no reason.

---

## Finding 4 — the legacy roots

| Root | State | Read |
|---|---|---|
| `7. Learn Fast` | `Graphics/`, `Videos/`, `Ideas/` — all created 2025-08-20, **never touched again** | **Fossil.** Scaffolding built and abandoned the same day. Third home for one project |
| `8. Cabinet` | One subfolder: `11B ECNL-RL Yellow/Player Headshots/`, 2026-02 | **Misnamed and live.** Not a cabinet — the current soccer team |
| `3D Modeling` | `My Models/`, `Downloaded Models/`, `GridFinity/` + 6 loose files, active to 2026-03 | **Live and useful. Keep** |
| `3D Modeling/PreheatTo350`<br>`3D Modeling/PaigeStanekCreations` | Both **empty**, created 2026-07-31 | **No conflict** with the out-of-scope roots — empty placeholders, not duplicates |
| `Colab Notebooks` | 15 × `Untitled*.ipynb` + 2 `Copy of …` | Exhaust |
| `Classes` | `fall_2024/ClassMaterialRef/extras_jeopardy/`, with 12 scattered copies of `extras_jeopardy` | Fossil, 2024 |
| `tmp` | 9 files, `1.png`–`9.png` — one scan set | Scratch folder that became permanent |
| `untitled folder` | **EMPTY.** Created 2026-03-29T01:08:20 — **18 seconds** before `am-gear.afphoto` landed at root | Pure accident, mid-Affinity-export |
| `Saved from Chrome`, `Epson Connect`, `Google Earth`, `Recordings`, `BasementVideos` | App-generated | Can't be removed safely; ignore |

`3D Modeling` repeats the root's own problem: some models in subfolders, six loose at top
level, including **two different files both named `Outside Fridge Handle Cover.stl`**
(16,684 vs 18,684 bytes) plus a third, `Outside Fridge Handle Cover2.stl`, at root.

### Out-of-scope roots hold the content their in-scope counterparts lack

Reported for context only — no action proposed:

- `01. Projects/Preheat to 350` is **empty**; `5. Preheat to 350` has 10 populated
  subfolders (`3d-printing`, `printables`, `images`, `purchased_art`, `cookie-cutters`,
  `caricature`, `labels`, `logos`, `business-cards`, `shopify`), active into 2026-04.
- `01. Projects/Paige Creations` is **empty**; the real material is under
  `6. Paige Stanek/`. The same venture carries **three names** across the Drive:
  "Paige Creations", "Paige Stanek", "Creations".

---

## Finding 5 — naming

No convention exists, and four collide by file type. Across ~305 files, **not one carries
an ISO `YYYY-MM-DD` prefix.**

| Convention | Count | Verbatim examples |
|---|---|---|
| Title Case with spaces (dominant for Google-native) | ~140 | `Force Team Manager Duties`, `Weight Loss 2025`, `Disney Dining Plans`, `Consulting Invoice Template` |
| Vendor `Hyphen-Case` downloads | ~40 | `Lean-Bulking-Meal-Plan-190-210-Pound-Man.pdf`, `BLS-5-Day-Workout-Routine.pdf`, `Hayward-Perflex-EC-50-DE-Above-Ground-Filter.pdf` |
| lowercase-kebab (dominant for uploaded assets) | ~25 | `am-gear-192x192.png`, `full-size-roof.png`, `wms-alpha4.apk`, `learn-fast-a.webp` |
| snake_case | ~30 | `BWS_Data_Tracy.csv`, `birth_sawyer.pdf`, `Full_Body_0.xlsx`, `Questionnaire_Chapter1`–`6.docx` |
| PascalCase / no separators | 10 | `ListComprehensionsAndGenerators`, `PropertySurvey.pdf`, `LicenseFront.pdf`, `GasBill.pdf` |
| Opaque publisher/SKU codes | 16 | `B14981_01_KR.docx`–`B14981_09.docx`, `978-1-83898-195-2_Reviewer Bio_David Stanek.docx`, `1629452 - User Guide, PowerForce Helix Pet, 3332.pdf` |
| **Vendor hash suffix, never renamed** | 8 | `Upper-Lower-4x-udpkvj.pdf`, `Full-Body-5x-rpoaxz.pdf`, `Powerbuilding-System_4X-v7kmza.pdf`, `Get-Ready-Manual-9qopa0.pdf` |
| Machine exports with random IDs | 7 | `strong3125100635546213796.csv`, `clevelandforcehsbblack20260409T175603139Z.pdf` |
| Tool/camera/scanner defaults | 8 | `IMG_20250530_183352.jpg`, `SKM_C3320i23051903560.pdf`, `Screenshot (Dec 8, 2021 00:57:09)` *(no extension)* |
| `Copy of ` prefix | 14 | `Copy of resume`, `Copy of End 68 Hours of Hunger Poster`, `Copy of WickApply Specification` |
| Pure integer | 9 | `1.png` … `9.png` |
| Year as **prefix** | 13 | `2012 Expenses for Taxes` … `2019 Expenses for Taxes`, `2017 Fundraisers` |
| Year as **suffix** | 14 | `Taxes 2020`–`2025`, `Weight Training 2018`, `Schedule Fall 2017` |

> Year-prefix and year-suffix **coexist inside the same folder** — `Taxes 2025` sits
> beside `2019 Expenses for Taxes`. That single folder can't be sorted chronologically.

**Zero-information names** — the only ones worth renaming:

| Pattern | Count | Where |
|---|---|---|
| `Untitled0-14.ipynb` | 15 | `Colab Notebooks` |
| `Copy of …` | 14 | root, `04. Archive`, `Colab Notebooks` |
| `Untitled Diagram.html` | 2 | root |
| `Untitled spreadsheet` | 1 | root |
| `Untitled presentation` | 1 | `04. Archive/CWRU-Python` — actually a DESN210 lecture deck, 2019-01-24 |
| `Untitled drawing` | 1 | `04. Archive/Shoreline` |
| `untitled folder` | 1 | root |

**Other defects:**

- **Typos frozen into filenames:** `Wine-Coler-User-Guide.pdf` (Cooler),
  `Hypertropy-Tracking-0.xlsx` (Hypertrophy), `Shoreline Singers Pittsburg Contract.docx`
  (a correctly-spelled twin exists), `Teach MeDependency Injection` (missing space)
- **Extension baked into a Google-native title** (there is no file to have an extension):
  `shoreline invoice jan 2018.docx`, `OReilly_Proposal_Form_Python.doc`,
  `Shoreline Financial Record.xlsx`, and 3 more
- Double extensions: `Headshot-small.png.png`, `Xander.jpg.jpg`
- Trailing space before extension: both `MHS Honor Roll -…-… .docx`
- Trailing space in title: `Mosman Mural Contract `, `Mural Contract `
- Double internal space: `The ultimate Docker  Container Book.pdf`,
  `CFSC COMPETITIVE  MANAGER'S INFORMATION & PROCEDURES`
- ALL CAPS: `SAWYER STANEK Conference Form`
- Numbered sequences in **three** incompatible spellings, both 0- and 1-based:
  spaced (`FantasyIQ Invoice 001`), concatenated (`CitySkoopInvoice001`), hyphenated
  (`Upper-Lower-Tracking-1.xlsx`, `Hypertropy-Tracking-0.xlsx`)
- Unexpanded acronyms with no glossary: `BLS`, `HSB`, `PF`, `CFSC`, `BWS`, `orm`
- `04. Archive/Shoreline` holds **31 MB of one document** — two `Shoreline Program 2018
  03_29_2018.docx` at 15,688,415 and 15,667,436 bytes, uploaded a day apart
- `wms-alpha1/2/3.apk` are all exactly 185,705,680 bytes — likely three uploads of one
  build (`wms-alpha4.apk` differs at 191,159,393)
- **4 files are Drive shortcuts, not content**, and may point at dead targets:
  `CFSC COMPETITIVE  MANAGER'S…`, `Final Project Intro Spring 2020`,
  `Shoreline Parent Member Contact Info 2015.xlsx`, and the MHS honor-roll pair

### `03. References/Manuals` — the worst 12 files in the Drive

Five conventions in twelve files, and inconsistent brand capitalisation *within the same
vendor*:

```
Hayward-Perflex-EC-50-DE-Above-Ground-Filter.pdf   Hayward-  (Title)
Hayward-Pump-ISSP1591_RevH_ae35.pdf                Hayward-  + SKU + hash
hayward-dv1000-manual.pdf                          hayward-  (lower)
Bambu Lab Quick Start Guide for AMS lite.pdf       "Start"
Bambu Lab Quick start guide - A1-EN.pdf            "start"
1629452 - User Guide, PowerForce Helix Pet, 3332.pdf   raw SKU dump
Cleanslate_Manual_EngFren_digital_R0.pdf           snake_Case_R0
Wine-Coler-User-Guide.pdf                          typo
```

### Proposed convention

To be added to `99 Meta/Conventions.md`:

| Kind of file | Pattern | Example |
|---|---|---|
| Google-native doc | `Title Case`, **no extension**, no type word | `Materials` — not `materials sheet`, not `Record.xlsx` |
| Point-in-time document | `YYYY-MM-DD Subject` | `2026-04-12 Roof Estimate` |
| Annual/periodic series | `Subject YYYY` — **suffix, pick one and stick to it** | `Taxes 2025`, `Taxes 2022` |
| Build / versioned artifact | `{project}-{stage}{n}.{ext}` | `wms-alpha4.apk` *(already right)* |
| Brand / design asset | `{brand}-{asset}-{variant}.{ext}` | `learn-fast-logo.svg` |
| Manual | `{Brand} {Model} Manual.pdf` | `Hayward DV1000 Manual.pdf` |
| 3D model | `{Object} v{n}.{ext}` | `Fridge Handle Cover v2.stl` |
| Data export | `{source} YYYY-MM-DD.{ext}` | `strong 2022-01-31.csv` |
| Photo set | folder carries context; keep camera names | `2025-11 Fall Session/IMG_6440.CR2` |

Banned: `Untitled*`, `Copy of *`, trailing ` (1)`, OS/scanner defaults, vendor hash
suffixes, double extensions, extensions on Google-native files, leading/trailing/double
spaces.

> **Rule of thumb:** the folder supplies the context; the filename supplies what makes
> this file different from its siblings. `Soccer/2025 Season/Roster` beats
> `Soccer/2025-soccer-season-roster-final-v2`.

### One convention question to settle

Drive and the vault disagree on their own top-level naming:

| | Drive | Vault |
|---|---|---|
| Separator | `01. Projects` (period) | `01 Projects` (no period) |
| Third tier | `03. References` | `03 Resources/` |

Worth aligning, since both are meant to be the same mental model.

---

## Proposed batches

Each is separately approvable and separately reversible.

### Batch B — Soccer, Lifting, Diet (moves only, no renames — lowest risk)

**Soccer** → single home at `02. Areas/Soccer/` (currently the empty shell):
```
02. Areas/Soccer/
  2026 CFSC HSB Black/    <- from 03. References/CFSC HSB Spring 26
  11B ECNL-RL Yellow/     <- from 8. Cabinet
  Team Manager/           <- Playmetrics HOWTO, from 04. Archive/Force
  Club Info/              <- the shortcut from 03. References/Soccer
  Archive/                <- 3 files from 04. Archive/Soccer
```
Then `8. Cabinet`, `04. Archive/Force` and `03. References/Soccer` are empty → trash.

**Lifting** → single home at `02. Areas/Lifting/`, Archive's 24 files becoming
`02. Areas/Lifting/Archive/`. Move `Wonder Slim Inventory`, `Nutrition Plan` and the
stranded `Diet` sheet out to Diet. Consider folding
`03. References/BLS Bonus - Legion/` in as `Lifting/Programs/BLS/` alongside `Plans/`.

**Diet** → **leave the tier boundary alone**; it works. Only take in the three strays.

### Batch C — un-invert the tiers

Reduced to three moves after user decisions:

- `02. Areas/Talks` → `04. Archive/` (nothing since 2017)
- `04. Archive/Vacations` → merge into `04. Archive/Disney`
- Collapse `04. Archive/Projects/{Sawyer,Xander}'s Training/` into one folder

**Held back by user decision:**

| Item | Decision |
|---|---|
| `04. Archive/Taxes` | **Stays.** The same-day edits were reorg prep — see the correction above |
| `03. References/End68` | **Stays in References.** Not archived despite being dormant since 2017 |
| `02. Areas/Career` | **Stays, empty.** A valid Area that hasn't been filled in yet |
| `03. References/Family`, `Manuals` | Stay — correct for their tier |

> **Convention clarification worth adding to `Conventions.md`:** an Area may legitimately
> be **empty**. `02. Areas/Career` is a real area of responsibility that simply has no
> downloaded material yet, so future audits must not report an empty Area folder as dead
> scaffolding. This is the Drive analogue of the existing rule that an Area needs no
> Todoist project. Contrast `02. Areas/Soccer`, which was empty *while its material sat in
> four other folders* — that was a genuine defect, and Batch B fixed it.

> Because Taxes isn't moving, Batch D needs a separate home for the ~8 identity and
> household records at root (driver's license ×4, `GasBill.pdf`, `Citizens_united.pdf`,
> `PropertySurvey.pdf`, `SKM_C3320i23051903560.pdf`). Proposal: a new
> `03. References/Household/` — they're lookup material with no completion date, which is
> exactly that tier's job. Needs a nod before D runs.

### Batch D — drain the root (largest: 90 files)

Move into the Finding 1 groups. Anything ambiguous goes to `00. Inbox/`, finally giving
it a job. Trash the confirmed duplicates: one `image2vector.svg`, `am-500x451.png`,
`Copy of RecTemplate.docx`, the duplicate honor-roll shortcut, one
`Shoreline Program 2018 03_29_2018.docx` (recovers 15 MB).

### Batch E — naming

Apply the convention to zero-information names only, reading each file first. Report
empty `Untitled*.ipynb` for trashing rather than inventing names. Fix the whitespace and
double-extension defects on anything being moved anyway.

### Batch F — backfill `drive:` URLs

Currently 2 of 21 notes. Paste URLs into frontmatter so binding stops relying on names.

---

## Open questions

1. **`7. Learn Fast`** — abandoned empty shell, and the third home for one project
   (`01. Projects/Learn Fast/`, `02 Areas/Learn Fast/`). Trash, or start using?
2. **`00. Inbox/`** — never used once. Batch D gives it a job. Keep or drop?
3. **`Classes`** — 2024 fossil with 12 scattered `extras_jeopardy` copies. Archive whole?
4. **Empty `Untitled*.ipynb`** and the suspected duplicate `wms-alpha1/2/3.apk` — trash?
5. **`Edited Stuart_abstract final`** is William Stuart's paper; **`Syllabus (psy 6720,
   7720)_Fall 2025`** is a psychology syllabus. Whose, and do they stay?
6. **`03. References/Case Final Project Share`** — files owned by `das311@case.edu`. Can
   only be unshared, not moved. Unshare it?
7. **Drive vs vault naming** — align on `NN. Name`/`NN Name` and
   `References`/`Resources`?
8. **`Taxes 2022`** is missing. Lost, or never created?

---

## Change log

Appended as batches execute. `File ID` is the durable key — it survives moves and
renames, so any row reverses by feeding `update_file` the *Before* value.

| # | Batch | Action | File ID | Before | After |
|---|---|---|---|---|---|
| 1 | B | move | `1jfKcYiO8CyoSb-5liTJbmiNnoc1gHaBK` | `03. References/CFSC HSB Spring 26` | `02. Areas/Soccer/CFSC HSB Spring 26` |
| 2 | B | move | `1xzIrS7RhgeUkU8BASY803TaM6PiL4Z3v` | `8. Cabinet/11B ECNL-RL Yellow` | `02. Areas/Soccer/11B ECNL-RL Yellow` |
| 3 | B | move | `1nMFrQFxvdbYEacHtkZGP5RxsQlKbxSK1` | `04. Archive/Force` | `02. Areas/Soccer/Force` |
| 4 | B | move | `1QhX3dA9y19-6Hq02QRJxvT_8aArGXH8w` | `03. References/Soccer/CFSC COMPETITIVE  MANAGER'S INFORMATION & PROCEDURES` | `02. Areas/Soccer/` *(same title)* |
| 5 | B | move + rename | `18LQiy9ehbhmohTa-bywcpjT9QQ99I1zl` | `04. Archive/Soccer` | `02. Areas/Soccer/Archive` |
| 6 | B | move + rename | `1fCERgUEWBjBD3UnxJvJgR0qwfGVgJM5a` | `04. Archive/Lifting` | `02. Areas/Lifting/Archive` |
| 7 | B | move | `1nA0l-MMTAvLAIY8S53omH0OrjWaPd7W7RPh2QO3dQ2I` | `02. Areas/Lifting/Wonder Slim Inventory` | `02. Areas/Diet/Wonder Slim Inventory` |
| 8 | B | move | `1IlmDAn7mhCnXZYxTJMfqBVRy5kWGSYV1O_zcK2xO-RE` | `02. Areas/Lifting/Nutrition Plan` | `02. Areas/Diet/Nutrition Plan` |
| 9 | B | move + rename | `1Hov477pR28OgYm9PQIoR-w75j4LHYZ49QqHscf5BJog` | `04. Archive/Lifting/Diet` | `02. Areas/Diet/Meal Plan 210 lb 2200 cal` |
| 10 | B | move | `1KJXqdvnigJo1jLdbzhPaMk51_sIJIV3c` | `03. References/BLS Bonus - Legion` | `02. Areas/Lifting/BLS Bonus - Legion` |
| 11 | B | **trash** | `11ufZ9ET6QKQI55a7OidUvoVJt6nQ_eOq` | `03. References/Soccer` *(verified empty first)* | Drive trash — recoverable to 2026-09-16 |
| 12 | B | delete | `15NMI0AxlW4025vkj_RuE6-Et1oMaNI2J` | `8. Cabinet` *(empty after row 2)* | **Deleted by the user by hand**, not by this pass. Declined as a tool call, then removed manually |
| 13 | C | rename | `1Xe3YRZIwyxsHziRX2G0pp7Q37L0h8z2N` | `04. Archive/Projects/Sawyer's Training` | `04. Archive/Projects/Boys Weight Training` |
| 14 | C | rename | `1wS_4j4owu3ufL7AsKsaczdqohF4gRTXY_VlUPs-CFWk` | `Sawyer's Weight Training` | `Sawyer` |
| 15 | C | move + rename | `1g-4cFNh30zZQE-ufg2IPdquYpUI7jpwEclgGCW-DJ2Y` | `04. Archive/Projects/Xander's Training/Xander's Weight Training` | `04. Archive/Projects/Boys Weight Training/Xander` |
| 16 | C | **trash** | `1tOoyl9qPQRIqtKZ82wFCy_NkY06P-AhX` | `04. Archive/Projects/Xander's Training` *(verified empty first)* | Drive trash — recoverable to 2026-09-16 |
| 17 | C | move | `0B44Fs9T9UrbhMXNXcWo1eU9EVjg` | `02. Areas/Talks` | `04. Archive/Talks` |
| 18 | C | move | `18MbFm-_xKAFSaxWqehs5m3WMwS0fJ2Dt` | `04. Archive/Disney` | `04. Archive/Vacations/Disney` |
| 19 | D1 | mkdir | `1Pw0Gfb5uhgZELt_i71-JJHiszviPaSq3` | — | `02. Areas/Open Source` |
| 20 | D1 | mkdir | `1b1-C5X43rdbjF_iQyrk6jkPfNrJEYiNd` | — | `02. Areas/Open Source/am` |
| 21 | D1 | move | `1UBuHMmpmZ4UHMYWBQAI9Mzuhp5szdzti` | `am.afphoto` *(root)* | `02. Areas/Open Source/am/am.afphoto` |
| 22 | D1 | move | `1FoCrwjXAeC1HHXnUo5gSk082oiKmx87Y` | `am-gear.afphoto` *(root)* | `02. Areas/Open Source/am/am-gear.afphoto` |
| 23 | D1 | move | `1UPtRLA9OMVukaA8XVSXztJ4qLiP3N9Iq` | `am.png` *(root)* | `02. Areas/Open Source/am/am.png` |
| 24 | D1 | move | `1mrSvKXUEGmjqhprFa-MdYcuMJvP5qMza` | `am-gear-192x192.png` *(root)* | `02. Areas/Open Source/am/am-gear-192x192.png` |
| 25 | D1 | **trash** | `11LhTbpUmGTUvaG_-8hRevP_hdo0mNwYi` | `am-500x451.png` *(root)* — byte-identical to `am.png`, both 168,096 | Drive trash — recoverable to 2026-09-16 |
| 26 | D2 | move + rename | `1kqvCwMob-QVsRh1dVXd93SyifSq3VJUufbEIG60VHFg` | `resume` *(root)* | `02. Areas/Career/Resume 2012` |
| 27 | D2 | move + rename | `1HWzf7NomUgBtZwuSM1WvM4oZy8poBmGvKiR6gfNPo18ovtLf-UzDnEnQumwv` | `resume.doc` *(root)* | `02. Areas/Career/Resume 2012.doc` |
| 28 | D2 | move | `1maBoDrh7ZTlKaGwwGhT2slCbs0UoRSDVwMpC29-UKi0` | `CWRU Rec of Me` *(root)* | `02. Areas/Career/CWRU Rec of Me` |
| 29 | D2 | move | `1JhMhWCUceOGl7Xt1GOm8ld0GGWiLCcFR` | `David Stanek LoC.docx` *(root)* | `02. Areas/Career/David Stanek LoC.docx` |
| 30 | D2 | move + rename | `1svOTv1hsrzYM_rpakVxC8sphbyqrQDeV` | `RecTemplate.docx` *(root)* | `02. Areas/Career/Recommendation Letter Template.docx` |
| 31 | D2 | **trash** | `1gaUE1e88xyGRAR9hZUrnfocOmRnno0OSr3Ec4sCxJWg` | `Copy of resume` *(root)* — third copy of the 2012 resume | Drive trash — recoverable to 2026-09-16 |
| 32 | D2 | **trash** | `1v9JmMcBBVA4Sw7FgMsQLkrB1yD6DqzFe` | `Copy of RecTemplate.docx` *(root)* — **verified** identical text to row 29, not to the template | Drive trash — recoverable to 2026-09-16 |

| 33 | D2 | rename | `1JhMhWCUceOGl7Xt1GOm8ld0GGWiLCcFR` | `02. Areas/Career/David Stanek LoC.docx` | `02. Areas/Career/2021-10-08 Recommendation Letter - Lyytinen.docx` |

| 34 | D2 | **trash** | `1maBoDrh7ZTlKaGwwGhT2slCbs0UoRSDVwMpC29-UKi0` | `02. Areas/Career/CWRU Rec of Me` — read first; a superseded draft with placeholder headings (`Opening`, `Body about…`) and a sentence cut off mid-word | Drive trash — recoverable to 2026-09-16 |
| 35 | D3 | *(user)* | 6 files | 4 license files, `GasBill.pdf`, `Citizens_united.pdf` *(root)* | **Deleted by the user by hand.** Verified gone |
| 36 | D3 | mkdir | `1e6VwPS6a8WzwsgYXQKb0vACR5ACi_YC3` | — | `03. References/Household` |
| 37 | D3 | move + rename | `1u_i3q9R4BBpEaoFhZ70KS8LWlAQKGAbY` | `PropertySurvey.pdf` *(root)* | `03. References/Household/Property Survey.pdf` |
| 38 | D3 | move + rename | `1deo2_vKzMKAVD-vfaRiXV5rRtl72TAJ7` | `SKM_C3320i23051903560.pdf` *(root)* | `04. Archive/Electrical Issues/Streb Electric Rewire Letter.pdf` |

| 39 | D4 | mkdir | `13Etb92Q_zMjatNY_Pt-k8L8FZ2IJLMmV` | — | `02. Areas/Financial` |
| 40 | D4 | move + rename | `1ht014TmdQp5-ctT_xqxyCando4FMjm6mvNGCQONg7RU` | `Finance` *(root)* | `02. Areas/Financial/Mortgage Refinance Analysis` |
| 41 | D4 | move | `1b13oWsjQ5e8nhnb3feAucKFMptr0ochZYQoUAQV8EzM` | `Sadie Budget` *(root)* | `02. Areas/Financial/Sadie Budget` |
| 42 | D4 | move + rename | `18UGmZp_Iwx7SfqngosoIo0yepKd3P1XinsBzr3yrTiM` | `Copy of Family Budget Planner - Generic` *(root)* | `02. Areas/Financial/Family Budget Planner Template` |
| 43 | D4 | move + rename | `0B44Fs9T9UrbhOUg5Y0hvZGhNbzA` | `Household_Budget_Worksheet_Downloadable-6.xls` *(root)* | `02. Areas/Financial/Household Budget Worksheet.xls` |

| 44 | D5 | mkdir | `1y62lbMcnSH2Hom2BJvxBZuz6RM9jR-PZ` | — | `02. Areas/School` |
| 45 | D5 | mkdir | `1Z-FH_UnB9DQI0GD9moqy-R38W94mITHa` | — | `02. Areas/School/Sawyer` |
| 46 | D5 | mkdir | `1r9RK0RvbcdjDwA-0urwGWGYXDJlVk092` | — | `02. Areas/School/Honor Rolls` |
| 47 | D5 | move + rename | `1o5G0_tt9tJSLBm0GHg3hZBRWZ4IDXcalRntVg2UHdgo` | `SAWYER STANEK Conference Form` *(root)* | `02. Areas/School/Sawyer/Conference Form 2021` |
| 48 | D5 | move + rename | `1NTKilKbKpgk1hBb5to5cEesao8ZP1GWj` | `MHS Honor Roll -1st Quarter 2025-2026 .docx` *(root)* | `02. Areas/School/Honor Rolls/MHS Honor Roll 2025-2026 Q1.docx` |
| 49 | D5 | move + rename | `1M6avC30gojuirOzja3MM53Bvq7G4ITJP` | `MHS Honor Roll -3rd Quarter 2025-2026 .docx` *(root)* | `02. Areas/School/Honor Rolls/MHS Honor Roll 2025-2026 Q3.docx` |
| 50 | D5 | move + rename | `11fKHp1iAtkj6G-Nz4b6XPF5z1uMsWU8FSMuqh1J2zbU` | `MHS Cast Lists 25-26` *(root)* | `02. Areas/School/MHS Cast Lists 2025-2026` |
| 51 | D5 | **trash** | `1w_EK6ly5h76HamkslYcKcRKq2U6IyOc9` | `MHS Honor Roll -3rdQuarter 2024-2025 (1).docx` *(root)* — a shortcut, target alive and still shared | Drive trash — recoverable to 2026-09-16 |
| 52 | D5 | **trash** | `1QBaZaua2NxvcbpUkJFG3KLq0duHnJXNU` | `Copy of MHS Honor Roll -3rdQuarter 2024-2025 (1).docx` *(root)* — second shortcut to the same file | Drive trash — recoverable to 2026-09-16 |

| 53 | D6 | move + rename | `174akrYq_lANrz33pnMIZMyNiebvUB2Ki` | `samsung-fridge.pdf` *(root)* | `03. References/Manuals/Samsung Fridge Manual.pdf` |
| 54 | D6 | move + rename | `1Q_J0evZTe5L6TBLRtdY_kYs4HU-6Cdtp` | `briggs-stratton-4a23a68885da13beb63920e7f44c23f8.pdf` *(root)* | `03. References/Manuals/Briggs Stratton Manual.pdf` |
| 55 | D6 | move | `1tslKh3_LkoRTf4ceet6p-hZxY4TElgoSToMRDnQtytI` | `U13 through 15 Personal Workout Program CFSC 2024` *(root)* | `02. Areas/Soccer/` *(same title)* |
| 56 | D6 | **trash** | `1UU8RrM772zgv7bHMdqPzx0Zmc6NTt8ku3vIIzHLN2Mk` | `Force Team Manager Duties` *(root)* — user no longer a team manager | Drive trash — recoverable to 2026-09-16 |
| 57 | D6 | rename | `1RKRTqm2rhXYeyZc75pwgp_tTlMn_WCv7` | `hayward-dv1000-manual.pdf` | `Hayward DV1000 Manual.pdf` |
| 58 | D6 | rename | `1H_N91J7xcwi6NWoGfu1MvNlcP_nG7bgh` | `Hayward-Perflex-EC-50-DE-Above-Ground-Filter.pdf` | `Hayward Perflex EC-50 DE Filter Manual.pdf` |
| 59 | D6 | rename | `14cqZRTVILOOuWy9hT6PdkDCdOOWV8OVx` | `Hayward-Pump-ISSP1591_RevH_ae35.pdf` | `Hayward Pump ISSP1591 Manual.pdf` |
| 60 | D6 | rename | `15wgLtxzvcM35U4medFIRJ3wfSQrNQa-i` | `worx-battery-charger-WA3881M.pdf` | `Worx WA3881M Battery Charger Manual.pdf` |
| 61 | D6 | rename | `1hts0RafDSBNPwE41cIu3qc9HM-yORNgK` | `worx-nail-gun-wx840l.pdf` | `Worx WX840L Nail Gun Manual.pdf` |
| 62 | D6 | rename | `16GUc5Q77BKPS9qxzsrjzNKdbBv41Ig8u` | `LG-Washing-Machine.pdf` | `LG Washing Machine Manual.pdf` |
| 63 | D6 | rename | `1i-hW-INr65tq8J-fz0sIqrLjRZ1L8fAD` | `Wine-Coler-User-Guide.pdf` | `Wine Cooler Manual.pdf` *(typo fixed)* |
| 64 | D6 | rename | `1zYNJVo2I-5dBlp0tJ_7cxr9YfrTCRRpl` | `EverbiltSubmersiblePump.pdf` | `Everbilt Submersible Pump Manual.pdf` |
| 65 | D6 | rename | `1YKmUWVGd1lQyFo3b_qv2jIQQfNcKV47B` | `Cleanslate_Manual_EngFren_digital_R0.pdf` | `Cleanslate Manual.pdf` |
| 66 | D6 | rename | `18vzyNemXWiPNTWsqu0fmXupv8pOCm0f8` | `1629452 - User Guide, PowerForce Helix Pet, 3332.pdf` | `PowerForce Helix Pet Manual.pdf` |
| 67 | D6 | rename | `1t6r0PYZn076f4KL3LfZasxo4qUo0cIua` | `Bambu Lab Quick Start Guide for AMS lite.pdf` | `Bambu Lab AMS Lite Quick Start Guide.pdf` |
| 68 | D6 | rename | `1HztM03tP-qgYiBIx94oPK98iD46lhh_X` | `Bambu Lab Quick start guide - A1-EN.pdf` | `Bambu Lab A1 Quick Start Guide.pdf` |

| 69 | D6 | **trash** | `1i9-KS4xKh27yFGoKqSXTNf9Ci5wqT6mexIcwOI4GIe8` | `02. Areas/Soccer/Force/Team Manager Playmetrics Direct Pay HOWTO` — role ended | Drive trash — recoverable to 2026-09-16 |

| 70 | D6 | **trash** | `1nMFrQFxvdbYEacHtkZGP5RxsQlKbxSK1` | `02. Areas/Soccer/Force` *(verified empty first)* | Drive trash — recoverable to 2026-09-16 |

| 71 | D8 | mkdir | `1QwY5OPQkV9Tpu4AT90acVJTm97ZNrrLN` | — | `04. Archive/Projects/Paige Creations` |
| 72 | D8 | mkdir | `1XDiQG9JfGwB0u7DU3cC6U8klb25tRtv3` | — | `04. Archive/Projects/Paige Creations/Mosman Mural` |
| 73 | D8 | move + rename | `1MMGEolIphqA85irAjSICy7PHi_w3mXq7VYPjQW3lccg` | `Mosman Mural Contract ` *(root, trailing space)* | `04. Archive/Projects/Paige Creations/Mosman Mural/Mosman Mural Contract` |
| 74 | D8 | move + rename | `1uF1QWLbOpYlWCqNmlmJ2p4aAfmzEQ2HF` | `exhibit1.JPG` *(root)* | `04. Archive/Projects/Paige Creations/Mosman Mural/Exhibit 1 - Mural Sketch.jpg` |
| 75 | D8 | **trash** | `1QhX3dA9y19-6Hq02QRJxvT_8aArGXH8w` | `02. Areas/Soccer/CFSC COMPETITIVE  MANAGER'S INFORMATION & PROCEDURES` — shortcut to a club-owned file; team-manager role ended | Drive trash — recoverable to 2026-09-16 |

| 76 | D9 | mkdir | `1qMiSwl461_GC6XRD6bbSLmaPdDI2zLd-` | — | `02. Areas/Teaching` |
| 77 | D9 | move + rename | `1CuJcoffEdsmo1RUiyFwvSnH2EDYWmv0uc8XPpaKkyiY` | `Introduction to Programming` *(root)* | `02. Areas/Teaching/DESN 210 Syllabus` |
| 78 | D9 | move + rename | `14kDkpSnqvwaUNJ_xgUjXEemd6Z_JBdi9` | `ListComprehensionsAndGenerators` *(root)* | `02. Areas/Teaching/List Comprehensions and Generators` |
| 79 | D9 | rename | `1PJzkFymwEdTqsfMYgU6aYvpAztTrkYlZ` | `04. Archive/CWRU-Python` | `04. Archive/Teaching 2018-2021` |
| 80 | D9 | rename | `1GKrX9w5tmZ9iMllQPme9nJJqPzSmG5zSxZ4CF72O-TM` | `.../Teaching 2018-2021/Untitled presentation` | `.../Teaching 2018-2021/DESN 210 Conditionals Lecture 2019` |
| 81 | D9 | move | `1ZlBhHAQDftU4SBByOS_G63PLVU7i3XVttcNfi4mQhQo` | `Developing OpenStack` *(root)* | `04. Archive/Talks/` *(same title)* |
| 82 | D9 | **trash** | `1_U2HtzADHr6uNRerYJQlRU9XK-ILql7bVy9hnHbqi60` | `Syllabus (psy 6720, 7720)_Fall 2025` *(root)* — another instructor's course at another university | Drive trash — recoverable to 2026-09-17 |
| 83 | D9 | **trash** | `1EfOK8S2q6CTggWiR7CsdKKxYC3aAk-Bet_siAe-Kmy0` | `Skillshare Class Outline Template` *(root)* — blank vendor boilerplate, never filled in | Drive trash — recoverable to 2026-09-17 |
| — | D9 | *(gone)* | `1LUAUjf6KWUw31sndZpu0FRacwgzA30ubNDg_M3e6eVI` | `Rubric` *(root)* | **Deleted externally** before it could be moved — the API reported "entity not found" |

| 84 | D10 | **trash** | `0B44Fs9T9UrbhLUhWNjdBR1pjS0k` | `report.csv` *(root)* — 3-line Launchpad bug-status export, Oct 2015 | Drive trash — recoverable to 2026-09-17 |
| 85 | D10 | **trash** | `1ntj_NtGxFfBRcjtAbDXRN-RFlQ523k1cCzamM9l3VjM` | `Lifehacker Daily Personal Inventory [Daily Personal Inventory]` *(root)* — 2012 Google Form from a blog post | Drive trash — recoverable to 2026-09-17 |
| 86 | D10 | **trash** | `1dBb2wvM0znyoQiSaLB0_t20C6Yw0CqlhAYMwnoYT-Lc` | `Developer Take Home Test - Rackspace.docx` *(root, Google Doc conversion)* — **both copies read and confirmed identical** before deleting | Drive trash — recoverable to 2026-09-17 |
| 87 | D10 | mkdir | `1grU58dXcy4Q05LnbaiTIsvdIhZxEqu2H` | — | `04. Archive/OpenStack` |
| 88 | D10 | move + rename | `0B44Fs9T9UrbhTnY4VS1aWnpkUFp4czhFRVNBRzhoRnRmX2Zr` | `strategy.rst` *(root)* | `04. Archive/OpenStack/Keystone Federation Mapping Design.rst` |

| 89 | D11 | move | `1YQ2vdiDTHn7j2wPQ3NHUbvK9OVQ2ap_Z3CCvasK93K8` | `Ideal Protein Food` *(root)* | `02. Areas/Diet/` *(same title)* |
| 90 | D11 | move | `1jFZOY8ORULIgAxyoNU-lIjpk6denwUHD5IfG3ZsSXUE` | `Electronics Inventory` *(root)* | `03. References/Household/` *(same title)* |
| 91 | D11 | mkdir | `1dmJyPMBHof98GYZPglhp79qmwnSoPvs2` | — | `02. Areas/Branding` |
| 92 | D11 | move + rename | `1aEemk097SpYCRUcPif9N8VfpavZ2cIUN` | `YouTubeLearnFastBanner.afdesign` *(root)* | `02. Areas/Branding/learn-fast-youtube-banner.afdesign` |
| 93 | D11 | **trash** | `1qEFtJwDJVusHQo0n2q8pIbxGhFOE1qxV` | `Shipping Label.pdf` *(root)* — spent 2025 label | Drive trash — recoverable to 2026-09-17 |
| 94 | D11 | mkdir | `1ejR431OXVcGeUqw1xil3qAxjGbZAl172` | — | `01. Projects/Personal/Roof Leak` |
| 95 | D11 | move + rename | `1zgnIhrsLCp5AOFj0GCFiIYYhAMmnZz6D` | `full-size-roof.png` *(root)* | `01. Projects/Personal/Roof Leak/2026-04-06 Roof Full Size.png` |
| 96 | D11 | move + rename | `1UaNKB9XlcHAi0vDr_0TjISKGxiDL1qKQ` | `zoom-roof.png` *(root)* | `01. Projects/Personal/Roof Leak/2026-04-06 Roof Detail.png` |
| 97 | D11 | move + rename | `1eCYTU1gnIWKEwdi1ETw5iJlQr5c-qqTV` | `faq.png` *(root)* | `02. Areas/Teaching/DESN Canvas FAQ.png` |

| 98 | D11 | **trash** | `1Guj8XCX3mPRmt-GoTYNEaFryqa3CdFo` | `The Zen of Python.mm` *(root)* — shortcut; the 2010 mindmap it points at is owned by the user and untouched | Drive trash — recoverable to 2026-09-17 |
| 99 | D11 | **trash** | `1umFcqFCdgsjB2_xREILD1tMOix9kzloS` | `kpop png` *(root)* — shortcut to a folder owned by a third party; their content untouched | Drive trash — recoverable to 2026-09-17 |
| 100 | D11 | **trash** | `1zsCB6ZD69Z51C2fYVCx98xEtZUQotqwI` | `Saved from Chrome/kpophunter.zip` *(2026-03-28 copy)* — byte-identical to the 2026-03-11 original, both 17,630,909 | Drive trash — recoverable to 2026-09-17. **~17.6 MB reclaimed** |

| 101 | D11 | move + rename | `1wdH9WpInc4rCZoUWGC3jDquNoy3Gn_r6UR4ch2G8T0E` | `Letter From Santa` *(root, created 2018-12-25)* | `03. References/Family/Letter From Santa 2018` |
| 102 | D11 | move | `1WW-6Igo_Kk0l0bCXkbi5qCvrj_yj23HQQ80dgZW_6IQ` | `Letter From Santa 2019` *(root)* | `03. References/Family/` *(same title)* |

| 103 | D11 | mkdir | `17YaQuijN5QPSdW4LuXkOUMajTCV1J6DN` | — | `03. References/Family/Photos` |
| 104 | D11 | move | `15UF37Y7ShCcIvnpFxolcq4zN__5sLU7M` | `Xander.jpg` *(root)* | `03. References/Family/Photos/` *(same title)* |
| 105 | D11 | move | `1SlTK6ARWHbm4Rss4Td47Z_jTxubSf51N` | `IMG_20250530_183352.jpg` *(root)* | `03. References/Family/Photos/` *(same title, see note)* |
| — | D11 | *(gone)* | `10czZKAmBAIk0uzcMyYXHdrB34dvrpO_P` | `sawyer.jpg` *(root)* | **Deleted externally** before it could be moved — second occurrence of this, after `Rubric` |

**Photos went *inside* `Family/`, not beside it.** A sibling `Family Photos/` would have split one
subject across two folders — the exact defect batch B spent eleven operations undoing for Soccer.

`IMG_20250530_183352.jpg` was **deliberately not renamed**. Reading it returned no extractable
text, as expected for a photograph, so its subject is unknown. A date-only name like
`2025-05-30 Photo.jpg` would carry *less* information than the camera string, which at least
still correlates with the original on the device. Naming it needs someone who can see it.

| 106 | D11 | move + rename | `1xCYh0xkuJI-INkt2trNfdc2iuA5HB92Hojm0HOtBuG4` | `Untitled spreadsheet` *(root)* | `04. Archive/Taxes/2025 Expenses for Taxes` |
| 107 | D11 | mkdir | `1MW27QKemTuk6yUPydbQmSbGFdqWakteV` | — | `02. Areas/School/Archive` |
| 108 | D11 | move + rename | `1RIcu631lMuNBo6KZBg_DkwHaYocs0Y-hDCQtCyugPFE` | `Final Orchard Program` *(root)* | `02. Areas/School/Archive/Orchard Hollow PTA Program 2022` |
| 109 | D11 | mkdir | `13jtkG90PMywF9E1Rh1lp2mBRxbviaRS4` | — | `03. References/Books` |
| 110 | D11 | move + rename | `1O80q_wz6rW1CyXqk1rpitrJYgLFCR93d` | `The ultimate Docker  Container Book.pdf` *(root, double space)* | `03. References/Books/The Ultimate Docker Container Book.pdf` |
| 111 | D11 | move + rename | `0B44Fs9T9UrbhVG1BSWxPVDJoV2M` | `Open_Government.mobi` *(root)* | `03. References/Books/Open Government.mobi` |

### A correction to Finding 5 — the Taxes folder

This report criticised `04. Archive/Taxes/` for mixing year-prefix (`2019 Expenses for Taxes`)
and year-suffix (`Taxes 2025`) naming inside one folder, and claimed it "can't be sorted
chronologically".

That reading now looks wrong. The two patterns appear to track two **document types**, not two
eras of carelessness: `Taxes YYYY` are the filing and prep documents — `Taxes 2025` is a letter
to the family accountant — while `YYYY Expenses for Taxes` are the expense worksheets that feed
them. The user identified the root-level `Untitled spreadsheet` as his 2025 expense calculation
and asked for the folder's existing pattern, which places it as `2025 Expenses for Taxes`,
sitting correctly *beside* `Taxes 2025` rather than competing with it.

A convention that looks inconsistent from outside may be encoding a distinction the observer
cannot see. Worth remembering before "normalising" anything.

### Why the Docker book did not become a project folder

The user was setting up a book manager and wondered whether the book belonged in that future
project. It went to a new `03. References/Books/` instead, for three reasons: it rehomes
`Open_Government.mobi` at the same time; `References/Books/` is the natural *import source* for
a book manager rather than build material for one; and creating
`01. Projects/Personal/Book Manager/` before the project exists in Todoist would repeat the
exact anti-pattern this reorg exists to fix.

That matters because this pass has already created one such folder — `Roof Leak` — with no
Todoist project behind it. **One is a pragmatic exception; two is a relapse.** Both need Todoist
entries or they are the same empty scaffolding the audit opened by criticising.

| 112 | F | mkdir | `1MKDX5LpF8Bpeidkz39H-bSkQgbStrDOn` | — | `02. Areas/Learn Fast` |
| 113 | F | move | `1o_9UAhfUvXoeZ0kxyk2gPwodKn6nYgH2` | `7. Learn Fast/Graphics` | `02. Areas/Learn Fast/Graphics` |
| 114 | F | move | `1XLtZnubaP23sWrCvnqYNfvkfpVxtpK2B` | `7. Learn Fast/Videos` *(empty)* | `02. Areas/Learn Fast/Videos` |
| 115 | F | move | `1O0Sc-zHJZiduH4Lg9rJr6gOdN3kR8i7L` | `7. Learn Fast/Ideas` *(empty)* | `02. Areas/Learn Fast/Ideas` |
| 116 | F | **trash** | `1r4MimWdJiI5qrIht89b2Sjt9fQCYF0_1` | `7. Learn Fast` *(verified empty first)* | Drive trash — recoverable to 2026-09-17 |
| 117 | F | move | `1aEemk097SpYCRUcPif9N8VfpavZ2cIUN` | `02. Areas/Branding/learn-fast-youtube-banner.afdesign` | `02. Areas/Learn Fast/Graphics/` |
| 118 | F | move | `1OPfqKMXZCSYdgdiCqftgeXDwIN9LWBAV` | `01. Projects/Learn Fast/YouTube Streaming/learn-fast-a.webp` | `02. Areas/Learn Fast/Graphics/` |
| 119 | F | move + rename | `1xXDq9qxGYCp5gKY1SgJv8kHrWHP-vuXE` | `01. Projects/Learn Fast/YouTube Streaming/learn_fast_logo.svg` | `02. Areas/Learn Fast/Graphics/learn-fast-logo.svg` |

| 120 | F | rename | `1YCMPwJkf92JDffLTNwqvfxmt4rAr1WfQ` | `00. Inbox` | `00 Inbox` |
| 121 | F | rename | `14Kt3GswyG0moflC5iLEG769Rov879PiA` | `01. Projects` | `01 Projects` |
| 122 | F | rename | `1DlzW6BMKL5QG73qwXPutl41jw5X9s__g` | `02. Areas` | `02 Areas` |
| 123 | F | rename | `1s4HZwVfZ0IIB25Tw3qu3QHxG_CCUJgJy` | `03. References` | `03 References` |
| 124 | F | rename | `1S5YKDU-Xa9oc-lwnvSQOufX9nZmKcAmT` | `04. Archive` | `04 Archive` |

| 125 | F | rename | `1s4HZwVfZ0IIB25Tw3qu3QHxG_CCUJgJy` | `03 References` | `03 Resources` — matches the vault's PARA wording |
| 126 | F | rename | `1Bd6vHJi6wGdvdQfsBUw5VLpG6tD67NBs` | `02 Areas/Diet` | `02 Areas/Weight loss` |
| 127 | F | rename | `1eDYwFL_p6sPn7Nk7GJDcIGVLL1a8qK0-` | `04 Archive/Diet` | `04 Archive/Weight loss` |

### Open questions closed

| Question | Resolution |
|---|---|
| `03 References` vs the vault's `03 Resources` | **Resources.** It is the PARA word; Drive was the outlier. Propagated through every doc |
| `Weight loss` vs `Diet` | **Weight loss.** Both the Area *and* its archive counterpart renamed, so the subject carries one name across both systems |
| `5. Preheat to 350`, `6. Paige Stanek` | **Left alone**, by explicit decision. The root is knowingly inconsistent rather than accidentally so |
| `Roof Leak` and `Raised Flower Beds` had no Todoist project | **Created**, both under the `Personal` parent, each with a next action and an Obsidian note |

`Roof Leak` got a due-dated task (`2026-08-19`) and `status: active`; **`Raised
Flower Beds` deliberately got an *undated* task**, so it derives as `backlog`.
Dating it would have manufactured a fake-active project to satisfy the GTD rule —
which is the letter of the convention against its purpose.

That also closes finding 5.2 from [[Reconciliation 2026-08-05]], which flagged
`Raised Flower Beds` as a real project with neither a note nor a Todoist entry.
It had sat open for two weeks.

### Reconciliation gaps captured for a design session

The reorg kept surfacing problems that **no existing check would catch**. Rather
than patch them one at a time, they are collected in
[[Reconciliation Gaps to Discuss]] — five classes, including the big one: the
Areas blind spot that hid four missing index notes, which in turn made four Areas
invisible to every Dataview view in the vault.

### Drive root aligned with the vault

The `NN. Name` / `NN Name` split between Drive and the vault — raised in Finding 5 as an open
question — is resolved in the vault's favour. Drive's five roots dropped the period.

**Folder IDs do not change on rename**, so all seven `drive:` bindings written minutes earlier
survived untouched. That is the payoff of binding by URL rather than by path, and this is the
first time in the reorg it has actually been tested.

The rename was then propagated through **32 references across 9 documents** — `Conventions.md`,
`Project Reconciliation.md`, `Templates/Project.md`, `REFERENCE.md`, the four new Area index
notes, and the 3D model inventory. Not doing so would have recreated precisely the drift this
audit opened by finding: prose describing folders that no longer exist under those names.
`domains.json` needed nothing — it stores Drive IDs, never paths.

Two loose ends this creates:

- **`03 References` vs the vault's `03 Resources`.** Only the separator was changed, because
  that is what was asked. The two tiers still carry different *words* for the same idea.
- **`5. Preheat to 350` and `6. Paige Stanek`** keep their periods and single digits, being out
  of scope. The root is now internally inconsistent by explicit decision rather than by neglect.

### Batch F — bindings, and what the backfill exposed

The backfill was expected to be a clerical job: paste `drive:` URLs into notes. It was two
URLs' worth of work and surfaced two structural problems instead.

**Four of eight Areas had no index note.** `Financial`, `Weight loss`, `Learn Fast` and
`DESN 210 Fall 2026` were folders of support notes with no anchor — a direct violation of
*"An Area is a directory with an index note of the same name"* in `Conventions.md`. Because
the Dashboard's Dataview panes query `type: area` in frontmatter, and no index note means no
frontmatter, **those four Areas were invisible to every view in the vault.** All four notes
were written; bindings went from 2 to 7.

**Nothing would ever have caught this.** `Project Reconciliation.md` states plainly:
*"Because Areas live outside `01 Projects/`, reconciliation never scans them."* That was safe
when Areas were vault-only. This reorg gave Drive nine Areas, four of which have no vault
counterpart (`Lifting`, `Soccer`, `School`, `Open Source`), plus two name mismatches. The
reconciliation pass is now blind to a whole category it did not previously need to see.

**Learn Fast consolidated from three locations to one.** The name had been spread across a
legacy root (`7. Learn Fast/`, scaffolded 2025-08-20 and abandoned the same day), the
`Branding` Area, and — as brand assets misfiled inside a *project* — `01. Projects/Learn
Fast/YouTube Streaming/`. That last one was flagged in Finding 5 of this report on day one and
is now resolved. `01. Projects/Learn Fast/` correctly remains as the **domain** folder.

`02. Areas/Branding/` is now empty, which is correct: its note describes personal presence —
GitHub, LinkedIn — not the education business. Per the newly written convention, an empty Area
is not a defect.

> **Left for the user:** `02. Areas/Learn Fast/Graphics/` holds two different files both named
> `BannerFullSizeBackground.afphoto`, 37.8 MB and 16.1 MB. Same pattern as the fridge handle —
> needs opening, not guessing.

### Batch D group 11 — stragglers

The user had already cleaned several of these by hand: both double extensions fixed
(`Headshot-small.png.png` → `Headshot-small.png`, `Xander.jpg.jpg` → `Xander.jpg`), one of
the two identical `image2vector.svg` files removed, and `Tickets`, the four
`Copy of HubSpot …` sheets, `Copy of Bigger Leaner Stronger …` and
`Edited Stuart_abstract final` all deleted.

**`01. Projects/Personal/Roof Leak/` is the first genuinely new project folder this reorg has
created**, and it exposes a gap. Per `Conventions.md` a project exists because it is in
Todoist — this one is not, so strictly it is a Drive folder without a project behind it. It
also must not be confused with `01 Projects/Water Leak Detection/`, which is an unrelated
`backlog` ESPHome/ESP32 sensor build for *detecting future* leaks, not repairing a current
one. Two similar names, two different concerns.

The roof images were renamed to the `YYYY-MM-DD Subject` pattern because they are
point-in-time evidence of a specific day's damage, and `full-size` / `zoom` described the
crop rather than the subject.

**Shortcuts resolved** (both targets alive, so neither is broken — only redundant):

| Shortcut | Target |
|---|---|
| `The Zen of Python.mm` | A 2010 FreeMind mindmap **the user owns**, held in an unmapped folder. The root shortcut duplicates a file already in Drive |
| `kpop png` | A folder owned by **`muhammadirfan43890@gmail.com`**, shared 2026-03-14. Third-party content |

> Incidental find: `Saved from Chrome/` holds `kpophunter.zip` **twice**, both exactly
> 17,630,909 bytes — 35 MB of the same download.

`faq.png` turned out to be a course asset the user made and reuses every semester for the
DESN Canvas setup, so it went to `02. Areas/Teaching/` rather than to `am`, which is where
its 5.8 KB size and January timestamp had suggested.

### Batch D group 10 result — and a fourth correction

**`strategy.rst` was on the disposal shortlist and should not have been.** Reading it showed a
substantial 2014 **Keystone federation-mapping design document** the user authored: a critique
of the contributed OpenStack federated mapper (indexed substitutions that shift when a rule is
edited, no conditional logic, no way to split `user@domain`, `not_any_of` inverting when regex
is enabled), a requirements list drawn from real RADIUS deployments, and a weighed comparison
of an embedded scripting language against enhanced rule mapping — including the sandboxing
tradeoff of running admin-supplied scripts inside a privileged process.

That is authored professional work. It was shortlisted purely because `strategy.rst` is an
uninformative filename. **A file's name is not evidence of its value** — the same failure mode
as correction #3, arrived at from the opposite direction: there I nearly deleted something
believing a false duplicate claim, here I nearly deleted something because its name said
nothing at all.

`report.csv` genuinely was junk — three lines of Launchpad bug counts for `keystone` and
`python-keystoneclient`, mostly zeroes.

The Rackspace take-home existed twice, as a 2013-05 `.docx` and a 2013-11 Google Doc
conversion. **Both were read in full and confirmed identical** — six problems, same wording —
before either was touched. The original `.docx` was kept.

**Left for the user, deliberately not disposed:**

| File | Why it needs a human |
|---|---|
| `Dev Test` | A hiring take-home the user authored. Its two named problems (spiral print, binary subtree) are #5 and #6 of the Rackspace test, and it was created the same day as the Google Doc conversion — so it is likely a **third copy** of the same material, but that was not verified |
| `ForTheLoveOfCakePromoCard` | A 2012 promo card for what may be Preheat to 350's ancestor. Sentimental value the filing system cannot assess |
| `Open_Government.mobi` | A 15.9 MB purchased ebook. Deleting a purchase is a different decision from deleting clutter |
| `Ideal Protein Food` | Reclassified out of disposal — it is diet material and belongs in `02. Areas/Diet/` |

### Batch D group 9 result — teaching separated from not-teaching

Reading these before moving them mattered: three of the six were not what their titles said.

| File | Actually |
|---|---|
| `Introduction to Programming` | **The DESN 210 syllabus.** "Introduction to Programming for Business Applications" — Python for non-technical business majors, *Automate the Boring Stuff* required, 12-week schedule, 40% coding / 30% group final project. The course still being taught, filed at root under a generic name |
| `Syllabus (psy 6720, 7720)_Fall 2025` | **Someone else's course.** Graduate Seminar in Social Psychology at the **University of Toledo**, instructor Jason Rose. Different person, institution and field |
| `Skillshare Class Outline Template` | **Blank Skillshare boilerplate** — their fill-in form, still carrying "Step 1: Make a Copy" instructions and teacher-handbook links. Never filled in |
| `ListComprehensionsAndGenerators` | Created 2019 but **last modified 2025-09-19**, mid-semester. Live teaching material, not an artifact |

`04. Archive/CWRU-Python/` was renamed **`Teaching 2018-2021`** because it held five files spanning *three* course codes — a DESN 210 lecture deck, a `307 Syllabus (Spring 2019)`, and a `Case Presentation` — none of which the old name described.

Drive's teaching home is `02. Areas/Teaching/` rather than mirroring the vault's `DESN 210 Fall 2026`, deliberately: a term-stamped folder needs renaming every semester, and the vault's copy has **already drifted** — it contains a `Spring Schedule.md` running January to April inside a folder named *Fall 2026*.

`Developing OpenStack` (2017 conference talk) joined `04. Archive/Talks/`, which batch C had just moved out of Areas.

> **Note on `Rubric`.** It was read during the audit (a grading rubric for a student programming project, Expert-5 → Attempted-1) and queued for `02. Areas/Teaching/`. By the time the move ran it had been deleted outside this session — the API first returned a permission error, then "entity not found". Nothing was lost by this pass; recorded so the row count reconciles.

### Batch D group 8 result — archive path convention set

The Mosman mural was a completed June 2024 commission (artist **Paige Stanek**, clients Jim
and Jennifer Mosman, $2,060), so it was archived rather than filed as a live project.

**This established the archive path convention:** a project at
`01. Projects/{Domain}/{Name}/` retires to `04. Archive/Projects/{Domain}/{Name}/` — same
path, one prefix changed. `04. Archive/Projects/` already existed as `archive_projects_id`
in `domains.json`, so this only makes the destination unambiguous and matches the
"move the folder to `04. Archive/`" step already in `Conventions.md`.

Renames fixed two real defects: the contract's title ended in a **trailing space**, and
`exhibit1.JPG` had an uppercase extension and a name that didn't reveal it is the mural
sketch the contract's *Exhibit 1* clause refers to.

> **Inconsistency to resolve:** `04. Archive/Projects/Boys Weight Training/` sits directly
> under `Projects/` with no domain layer, while Paige Creations now has one. For the
> convention to hold it should become `04. Archive/Projects/Personal/Boys Weight Training/`.
> One move, not yet approved.

**Left at root deliberately:** `Mural Contract ` — the blank template the signed contract
was made from. It is a reusable business asset, not part of a completed job, and burying it
in an archived folder would hide it exactly when it is next needed. Where Paige's reusable
business material belongs is a `6. Paige Stanek/` question, which is out of scope.

`02. Areas/Soccer/` is now free of team-manager material entirely — the duties doc, the
Playmetrics HOWTO, its `Force/` folder, and the club procedures shortcut have all gone.

### Batch D group 7 — deferred, inventoried instead

The user called the model cleanup "a much more involved cleanup process" and asked for a
list instead. Correct call: it is not a filing job. Full snapshot written to
**`03 Resources/3D Model Inventory.md`** — 28 files across 4 locations, with sizes, and the
specific problems that need a human who knows what the objects are.

The blockers, in short:

- **Three fridge-handle files, two names.** `3D Modeling/` holds two *different* files both
  called `Outside Fridge Handle Cover.stl` (16,684 and 18,684 bytes), and root holds
  `Outside Fridge Handle Cover2.stl` at 16,684 bytes — the same size as the first. So
  "Cover2" is likely a copy, not a version, and the 18,684-byte file is the real revision.
  Only opening them settles it.
- **`My Models/` holds exactly one file** (`martini.scad`) while 14 model files sit loose at
  root and in `3D Modeling/` top level. The authored-vs-downloaded split is worth keeping —
  a Printables download is replaceable, your own `.scad` is not — but it isn't being used.
- **Source, export and sliced output are mixed.** `hooks.step`, `hooks.stl` and
  `Shoerackpeg.gcode.3mf` are three different kinds of artefact; sliced files are
  disposable, CAD sources are not.
- **Two archives never unpacked** (`.zip`, `.rar`), so their contents are invisible to
  search.
- **`dress_cookie_cutter.stp` is 182 MB** — larger than every other model combined.

`3D Modeling/PreheatTo350/` and `/PaigeStanekCreations/` are still empty and are the
obvious destinations for the cookie-cutter and Paige Coin files when that cleanup happens.

> `02. Areas/Soccer/Force/` is now **empty** — the Playmetrics HOWTO was its only file.
> Batch B moved that folder out of Archive precisely because the document looked live; the
> user has since confirmed the team-manager role ended. The empty folder needs a decision.

### Batch D group 6 result — Manuals normalised

`03. References/Manuals/` was the worst-named folder in the Drive: five conventions across
twelve files, with brand capitalisation inconsistent *within the same vendor*. All fourteen
files (twelve existing plus two arriving from root) now follow one pattern:

**`{Brand} {Model} {DocType}.pdf`**

```
Bambu Lab A1 Quick Start Guide.pdf        Hayward Pump ISSP1591 Manual.pdf
Bambu Lab AMS Lite Quick Start Guide.pdf  LG Washing Machine Manual.pdf
Briggs Stratton Manual.pdf                PowerForce Helix Pet Manual.pdf
Cleanslate Manual.pdf                     Samsung Fridge Manual.pdf
Everbilt Submersible Pump Manual.pdf      Wine Cooler Manual.pdf
Hayward DV1000 Manual.pdf                 Worx WA3881M Battery Charger Manual.pdf
Hayward Perflex EC-50 DE Filter Manual.pdf  Worx WX840L Nail Gun Manual.pdf
```

What the normalisation removed: a 32-character download hash, a raw vendor SKU dump
(`1629452 - … , 3332`), revision cruft (`_RevH_ae35`, `_digital_R0`), a language marker
(`EngFren`), three separate capitalisations of *Hayward*, two of *Bambu Lab*'s "start", and
the frozen typo `Coler` → **Cooler**.

`DocType` is retained rather than forced to "Manual" because the two Bambu Lab files really
are quick-start guides, not full manuals — a distinction worth keeping when you're looking
for one or the other.

`Force Team Manager Duties` was trashed rather than filed: the user is no longer a team
manager.

### Batch D group 5 result

Resolving the two shortcuts changed the shape of this group. Both pointed at
`MHS Honor Roll -3rdQuarter 2024-2025 (1).docx` owned by **`heissb@mentorschools.org`** —
alive and still in *Shared with me*, so they were redundant rather than broken, and both
were trashed. No content was lost: the target is still shared.

More importantly, the honor rolls turned out to be **school-wide documents**, not records
about one child. Mentor Schools mass-distributes them — a series runs back to 2020-2021 in
*Shared with me* from `heissb@` and `coughlin@mentorschools.org`, each naming every student
on the honor roll. `MHS Cast Lists` is the same kind of thing.

So "one directory per child" was applied only where the content is per-child. Of the four
files exactly one was: the conference form. Filing a school-wide honor roll under
`Sawyer/` would have asserted something the document does not say. `Xander/` and any
siblings get created when there is material for them — the same reasoning the user gave for
keeping `02. Areas/Career` empty.

The renames fixed five defects: the trailing space before `.docx`, the stray hyphen in
`-1st Quarter`, two incompatible year formats (`25-26` vs `2025-2026`), the ALL-CAPS name,
and quarter-before-year ordering that prevented chronological sort.

> Note: the two owned honor-roll `.docx` files are downloaded copies of the shared
> originals — byte-identical sizes (34,353 and 31,995). They were kept, since a share can
> disappear when its owner deletes it, but the user may prefer to rely on *Shared with me*
> and drop them.

### Batch D group 4 result

`02. Areas/Financial/` created to mirror the vault's existing `02 Areas/Financial`, and
populated with four files from root.

`Finance` became **`Mortgage Refinance Analysis`** — it was read first, and it is a model
comparing the current loan against 30-year and 15-year refinances with HELOC interest and
repayment, landing on a $194,194 total-cost-of-ownership difference. "Finance" conveyed
none of that; the new name is findable.

Both budget files dropped their download artefacts: `Copy of ` and the
`_Downloadable-6` suffix a vendor site attached. Both are blank templates, so `Template`
now says so.

**Deliberately not moved:** `Tickets`. This report grouped it under Finance, but reading it
showed an event roster — names across Friday/Saturday/Sunday, headcounts 17/2/3, and a
$181.80 total. That is a single past event, not an ongoing financial responsibility. It
needs either an event home or disposal, pending the user identifying it.

### Batch D group 3 result

Reading the scanner-named PDF moved it out of this group entirely. `SKM_C3320i23051903560.pdf`
is a **Streb Electric contractor letter** — a hidden kitchen-ceiling junction box with all
wires melted together that never tripped the breaker, a charred panel, ungrounded
cloth-cased wiring, and a full-rewire recommendation addressed to the home insurer. Two
documents from that same matter were already sitting in `04. Archive/Electrical Issues/`,
so it joined them and took their plain-Title-Case naming rather than a date the letter
does not carry.

The two `rm` lines originally drafted for the license JPGs were **withdrawn before
approval**. A JPG and a PDF of the same document have unrelated file sizes, so "superseded
by the PDF" was an assumption, not a finding — and correction #3 above is precisely why
that class of inference must not be applied to identity documents. The user then deleted
all six identity files himself, which settled it.

> **Presentation change adopted here.** The approval dialog renders raw Drive IDs, which
> are meaningless to a human reviewer. From this point every mutating call is preceded by
> the single shell command it represents (`mv "old" "new"`), one command per call. IDs stay
> in this log, where they are the durable key for reversal, and out of the approval path.

`02. Areas/Open Source/am/` created and populated with the four `am` logo assets — `am` is
an open-source project the user maintains, so it gets its own Area rather than being
lumped under Learn Fast as this report originally guessed.

`02. Areas/Career/` was an empty placeholder and is now populated from root: two 2012
resumes, the CWRU recommendation, the Lyytinen letter, and the blank template. Root is
down 11 files.

> **Correction to Finding 1.** This report listed `RecTemplate.docx` and
> `Copy of RecTemplate.docx` as duplicates "both 294,942 bytes". Wrong — `RecTemplate.docx`
> is 15,592 bytes (a genuinely blank template) and the 294,942-byte twin of
> `Copy of RecTemplate.docx` is **`David Stanek LoC.docx`**. Both were read before the
> trash and confirmed to be the same 2021-10-08 recommendation letter from Kalle Lyytinen
> at Weatherhead. The trash was correct but the stated reason was not, and had the sizes
> lined up the other way, trashing on that reasoning would have destroyed the only copy of
> a real letter. **Verify duplicate claims by content, not by a remembered size.**

### Batch B result

Soccer went from six locations to one. `02. Areas/Soccer/` now holds `CFSC HSB Spring 26`,
`11B ECNL-RL Yellow`, `Force`, `Archive/`, and the club-info shortcut — verified.
`02. Areas/Lifting/` now holds its own 4 remaining files plus `Archive/` (24 files),
`Plans/`, and `BLS Bonus - Legion/`. `02. Areas/Diet/` gained the three strays and its
tier boundary with `04. Archive/Diet` was deliberately left intact.

**Reversal:** feed each row's *Before* path back to `update_file` against the same File
ID. Row 11 restores from Drive trash.

`8. Cabinet` is gone — the user deleted it by hand once Batch B had emptied it. Root is
now down one legacy folder.

### Batch C result

Six operations. `04. Archive/Projects/Boys Weight Training/` now holds `Sawyer` and
`Xander`, replacing two folders that each wrapped one spreadsheet with three redundant
words in the path. Both sheets are **rolling logs**, not year-scoped — checked before
naming — so the filenames carry only the distinguishing part. Both were set up in May 2024
with exercises and dates but **every weight and rep cell left blank**, which confirms
Archive as the right tier.

`Talks` moved to Archive. `Disney` became `04. Archive/Vacations/Disney/`.

> Note the merge direction is the inverse of what this report originally proposed. It
> said move the one Cape Coral file into `Disney`; instead `Disney` moved *into*
> `Vacations`. `Vacations` is the category and `Disney` is a subset of it — one operation
> instead of two, and the resulting hierarchy is the honest one.
