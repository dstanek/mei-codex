# Readwise → Obsidian Foundry Workflow

## Architecture

Use each system for a distinct purpose:

* **Readwise Reader** = source intake, reading, and highlighting
* **Readwise → Obsidian sync** = machine-managed source notes
* **Obsidian Foundry** = processed knowledge written in my own words

The key distinction is:

> Readwise stores sources and highlights.
> The Foundry stores my understanding.

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

Reader is the source and annotation system.

### Obsidian Readwise Imports

Treat synced Readwise notes as:

* source material
* quotations/highlights
* provenance
* an inbox of material waiting to be processed

These files should generally remain machine-managed.

Avoid manually reorganizing, renaming, or heavily editing them because future Readwise syncs may append new highlights or recreate expected files.

### Foundry

The Foundry contains knowledge that has been deliberately processed.

Foundry notes should:

* be written in my own words
* represent concepts, conclusions, patterns, or useful ideas
* link back to relevant source notes
* combine information from multiple sources when appropriate
* continue evolving over time

A Foundry note is not necessarily a summary of one source.

One source may create multiple Foundry notes, and multiple sources may contribute to one Foundry note.

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
Create or update Foundry note(s)
    ↓
Link Foundry note back to source
    ↓
Mark source note as processed
```

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

3. **Do not promote a Readwise-imported note directly into the Foundry.**
   Create or update a separate Foundry note instead.

4. **Keep imported Readwise notes as source records.**
   They preserve highlights, quotations, and provenance.

5. **Keep machine-managed Readwise files relatively untouched.**
   Avoid unnecessary moves, renames, and manual restructuring.

6. **Foundry notes must contain processed thinking.**
   Copying highlights alone does not qualify.

7. **Foundry notes should link to their sources.**

8. **One source does not imply one Foundry note.**
   A source may produce zero, one, or many ideas.

9. **Multiple sources may support the same Foundry note.**

10. **The Foundry is organized around ideas, not documents.**

---

## Source Processing State

A Readwise source note may optionally record whether it has been processed.

Example:

```yaml
---
source: readwise
status: processed
processed: 2026-09-17
foundry:
  - "[[Agent Communication Patterns]]"
  - "[[Nostr for Agent Messaging]]"
---
```

This makes it possible to identify:

> Readwise source notes that have synced into Obsidian but have not yet been distilled.

---

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
Foundry
```

The boundary is intentional:

* **Before the boundary:** what someone else said
* **After the boundary:** what I understand, believe, or want to remember

