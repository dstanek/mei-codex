<%*
const file = tp.file;
let title = file.title;  // current filename (without .md)

// A fresh note gets filed automatically. An existing note is someone applying
// this template to a note that already has a name and a home — never relocate
// that without asking. (Doing so silently moved 03 Resources/Watch & Read Queue.)
const isFresh = title.startsWith("Untitled");

// Only prompt for a title if we're on a fresh Untitled note
if (isFresh) {
    const input = await tp.system.prompt("Content idea title");

    // If user cancels or leaves blank -> delete this note and abort template
    if (!input || !input.trim()) {
        new Notice("No idea provided. Note will not be created.");
        await app.vault.delete(file.self);  // remove the Untitled note
        tR = "";                            // stop further template output
        return;
    }

    title = input.trim();
}

// All content ideas live here, flat. content-type and status do the grouping.
const targetFolder = "09 YT/Ideas";

// Check for duplicates against the real destination, not the current folder.
// Only a fresh note may be auto-deleted — never delete a note that already existed.
const existing = app.vault.getAbstractFileByPath(`${targetFolder}/${title}.md`);
if (existing && existing.path !== file.path(true)) {
    new Notice(`A content idea with that title already exists: "${title}"`);
    if (isFresh) await app.vault.delete(file.self);
    tR = "";
    return;
}

const contentType = await tp.system.suggester(
    ["Short video", "Long video", "Article", "Course"],
    ["short video", "long video", "article", "course"],
    false,
    "What kind of content?"
) || "short video";

// Ideas usually start life as nothing but a link, so capture it up front
const source = (await tp.system.prompt("Source link (optional)") || "").trim();

// File the note. Templater has no folder mapping for 09 YT, so this is what moves it.
// Fresh notes file themselves. Existing notes must opt in — moving a note the user
// already filed somewhere is destructive and must never happen by surprise.
if (isFresh) {
    await file.move(`${targetFolder}/${title}`);
} else if (file.folder(true) !== targetFolder) {
    const confirm = await tp.system.suggester(
        [`No — leave it in ${file.folder(true)}`, `Yes — move it to ${targetFolder}`],
        [false, true],
        false,
        `Move "${title}" out of ${file.folder(true)}?`
    );
    if (confirm) await file.move(`${targetFolder}/${title}`);
}
-%>
---
title: <% title %>
type: content-idea
content-type: <% contentType %>
status: seed
domain: learn-fast
source: "<% source %>"
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
tags: []
---

# <% title %>

## Source

<% source ? source : "*Where did this come from, and why did it catch your eye?*" %>

## Notes

## Outline

---

[[Content Ideas]]
