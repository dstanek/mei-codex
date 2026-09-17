---
type: meta
---
# Note Intake Process

How an external source becomes knowledge in the Foundary: Readwise Reader → the Readwise sync in `12 Readwise/` → my own-words notes in `05 Foundary/`.

## Architecture

Use each system for a distinct purpose:

* **Readwise Reader** = source intake, reading, and highlighting
* **Readwise → Obsidian sync** = machine-managed source notes
* **The Foundary** (`05 Foundary/`) = processed knowledge written in my own words

The key distinction is:

> Readwise stores sources and highlights.
> The Foundary stores my understanding.

Do not treat Readwise-imported notes as finished knowledge.

---

## What Belongs Where

### Readwise Reader

Use Reader for:

* articles
* YouTube videos
* GitHub repositories
* other external source material
* highlighting while reading
* lightweight source/workflow tags

Reader is the source and annotation system. Articles found in my email arrive here too: the communications assistant saves them to the Reader Inbox tagged `from-email`, following `99 Staff/Interests.md`.

### Readwise imports (`12 Readwise/`)

Treat synced Readwise notes as:

* source material
* quotations/highlights
* provenance
* an inbox of material waiting to be processed

These files should generally remain machine-managed.

Avoid manually reorganizing, renaming, or heavily editing them because future Readwise syncs may append new highlights or recreate expected files.

### The Foundary (`05 Foundary/`)

The Foundary contains knowledge that has been deliberately processed.

Foundary notes should:

* be written in my own words
* represent concepts, conclusions, patterns, or useful ideas
* link back to relevant source notes
* combine information from multiple sources when appropriate
* continue evolving over time

A Foundary note is a `zettel`, created from `99 Meta/Templates/Zettel.md`, and linked to a hub in `08 Topics/` so the idea is findable later.

A Foundary note is not necessarily a summary of one source.

One source may create multiple Foundary notes, and multiple sources may contribute to one Foundary note.

---

## Workflow

```text
Capture source
    ↓
Read in Reader
    ↓
Highlight useful material
    ↓
Archive source in Reader
    ↓
Highlights sync to Obsidian
    ↓
Review imported source note
    ↓
Distill useful ideas into my own words
    ↓
Create or update Foundary note(s)
    ↓
Link Foundary note back to source
    ↓
Mark source note as processed
```

### Sources that never reach Reader

A conversation, a talk, a thing I worked out myself: write the Foundary note directly, with the source inline (a link, a name, a date). No source note is required, and its absence is not a gap to be filled.

### Reader lifecycle

```text
Inbox → Read / Highlight → Archive
```

Archive means:

> I am finished actively processing this source for now.

It does not mean the source is no longer useful.

---

## Rules

1. **Archive Reader items after reading and highlighting them.**

2. **Use Reader tags sparingly.**
   Tags should mainly support the reading workflow, such as:

   * `research`
   * `reference`
   * `project/foo`
   * `needs-review`

   Do not recreate the full Obsidian knowledge taxonomy in Reader.

3. **Do not promote a Readwise-imported note directly into the Foundary.**
   Create or update a separate Foundary note instead.

4. **Keep imported Readwise notes as source records.**
   They preserve highlights, quotations, and provenance.

5. **Keep machine-managed Readwise files relatively untouched.**
   Avoid unnecessary moves, renames, and manual restructuring.

6. **Foundary notes must contain processed thinking.**
   Copying highlights alone does not qualify.

7. **Foundary notes should link to their sources.**

8. **One source does not imply one Foundary note.**
   A source may produce zero, one, or many ideas.

9. **Multiple sources may support the same Foundary note.**

10. **The Foundary is organized around ideas, not documents.**

---

## Finding unprocessed sources

A source is processed when a Foundary note links to it. That is rule 7 doing double duty: the backlink is the record, so nothing has to be marked by hand, and nothing can drift out of date.

Do not record processing state in the frontmatter of a synced note. The Readwise sync rewrites those files when new highlights arrive, so the marker is silently lost.

What has synced but not yet been distilled:

```dataview
LIST FROM "12 Readwise" WHERE length(file.inlinks) = 0
```

## For agents

This note is law for the staff as well as for me. In addition to the rules above:

* Never create or edit a Foundary note on my behalf. Distillation is the part that makes it mine; a generated note is one I would rewrite anyway.
* Never edit, move, rename or delete anything in `12 Readwise/`. The sync owns those files and re-creates the ones you move.
* Listing what is unprocessed, or what a source note contains, is always welcome.
* Filing a finished note I wrote, fixing its frontmatter, or linking it to the right topic is the librarian's job and is welcome.

## Mental Model

```text
External Source
      ↓
Reader
      ↓
Highlights
      ↓
Readwise Import
      ↓
Thinking / Distillation
      ↓
Foundary
```

The boundary is intentional:

* **Before the boundary:** what someone else said
* **After the boundary:** what I understand, believe, or want to remember

