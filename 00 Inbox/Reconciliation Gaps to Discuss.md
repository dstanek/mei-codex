---
title: Reconciliation Gaps to Discuss
type: meta
created: 2026-08-18 00:00
tags: [reconciliation]
---
# Reconciliation Gaps to Discuss

Captured during the [[Drive Reorg 2026-08-17]]. The reorg surfaced several
classes of problem that **no existing check would ever catch**. Worth a proper
design session rather than patching one at a time.

Governs: [[Project Reconciliation]], `/project-reconcile`, `/project-review`.

---

## 1. Areas are never scanned — and that stopped being safe

`Project Reconciliation.md` says plainly:

> Because Areas live outside `01 Projects/`, reconciliation never scans them, so
> an empty `todoist:` is never reported as an unlinked note. That's the point:
> nothing to check, nothing to drift.

That held when Areas were vault-only. It no longer does. Drive now has nine
Areas, and the reorg found:

- **Four of eight vault Areas had no index note** — `Financial`, `Weight loss`,
  `Learn Fast`, `DESN 210 Fall 2026`. No index note means no `type: area`
  frontmatter, which means those Areas were **invisible to every Dataview view
  in the vault**. Found by hand, not by any check.
- **Four Drive Areas have no vault counterpart** — `Lifting`, `Soccer`,
  `School`, `Open Source`.
- **Two name mismatches** existed across systems (`Weight loss`/`Diet`,
  `DESN 210 Fall 2026`/`Teaching`). One is now resolved; the class of problem is
  not.

**To decide:** does reconciliation grow an Areas pass? The minimum useful check
is *every directory in `02 Areas/` has an index note with `type: area`*.

## 2. An empty Area is legitimate — an empty *subject* is not

These look identical to a script and are opposites:

| | |
|---|---|
| `02 Areas/Career/` — empty for months, still a real responsibility | **Fine** |
| `02 Areas/Soccer/` — empty *while soccer material sat in four other folders* | **Defect** |

Now written into `Conventions.md`, but a checker needs to tell them apart or it
will cry wolf on the first and miss the second.

## 3. Drive folders with no project behind them

The reorg created `Roof Leak` and inherited `Raised Flower Beds` — Drive folders
with no Todoist project. Both are now fixed, but nothing detected them; the
2026-08-05 report caught `Raised Flower Beds` by eye and it then sat unresolved
for two weeks.

**To decide:** should a Drive folder under `01 Projects/{Domain}/` with no
matching `drive:` URL in any note be a reported finding?

## 4. Same-name, different-content files

Three live examples, each needing a human to open them:

- `3D Modeling/Outside Fridge Handle Cover.stl` — 16,684 B and 18,684 B, **same
  name**, plus `Cover2.stl` at root matching the first exactly
- `02 Areas/Learn Fast/Graphics/BannerFullSizeBackground.afphoto` — 37.8 MB and
  16.1 MB
- `04 Archive/Shoreline/Shoreline Program 2018 03_29_2018.docx` — two files
  21 KB apart, **31 MB total for one document**

Drive permits duplicate names in a folder; a filesystem would not. Cheap to
detect (same parent, same title), impossible to resolve automatically.

## 5. Deletions during a session

Twice during the reorg a file was deleted externally mid-pass — `Rubric` and
`sawyer.jpg` — surfacing as a permission error, then "entity not found". Harmless
here because everything was logged, but a longer automated run would need to
treat it as expected rather than as failure.

---

## Related, not reconciliation

- **`00 Inbox/` has never been used** since it was created 2026-03-12. Either it
  becomes the landing spot for unfiled material, or it goes. *(This note is
  currently the only thing in it.)*
- **`Spring Schedule.md`** in [[DESN 210 Fall 2026]] runs January to April, in a
  project named Fall 2026, with term starting now.
- **Two loose `.md` files in `02 Areas/`** — `5 Year Goals.md` and
  `Home Improvement.md` — violate *an Area is a directory with an index note*.
  Same class as gap 1, and equally unchecked.
