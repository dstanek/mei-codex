---
title: Content Ideas
type: meta
---

# Content Ideas

Every content idea lives as its own note in `09 YT/Ideas/`, flat. Create one with **Templater: Create new note from template** → `Content Idea` (*not* Insert template) — it prompts for a title, content type, and source link, then files itself.

An idea graduates out of `09 YT/Ideas/` once it hits `scripted`: move it into the matching `09 YT/{Series}/` folder and link it from that folder's `index.md`. See [[Video Script Guide]] for the script structure.

## In flight

```dataview
TABLE content-type AS "Type", status AS "Status", source AS "Source"
FROM "09 YT/Ideas"
WHERE type = "content-idea" AND status != "published" AND status != "dropped"
SORT status ASC, file.name ASC
```

## Needs a source or a next step

Seeds that are still just a title — nothing captured to work from yet.

```dataview
TABLE content-type AS "Type", created AS "Captured"
FROM "09 YT/Ideas"
WHERE type = "content-idea" AND status = "seed" AND (!source OR source = "")
SORT created ASC
```

## Ready to produce

Scripted and waiting to graduate into a series folder.

```dataview
TABLE content-type AS "Type", file.mtime AS "Updated"
FROM "09 YT/Ideas"
WHERE type = "content-idea" AND status = "scripted"
SORT file.mtime DESC
```

## Done and dropped

```dataview
TABLE content-type AS "Type", status AS "Status"
FROM "09 YT/Ideas"
WHERE type = "content-idea" AND (status = "published" OR status = "dropped")
SORT status ASC, file.name ASC
```

---

See [[Conventions]] for the `content-type` values and the full status lifecycle.
