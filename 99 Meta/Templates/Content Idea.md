<%*
const file = tp.file;

// --- Guard: never touch a note that already has content ---------------------
// This template renders a whole note, so running it on an existing note
// prepends a second frontmatter block and body. Two notes were damaged this way
// (03 Resources/Watch & Read Queue, 09 YT/Content Ideas) before this guard.
// "Create new note from template" gives an empty file; "Insert template" does not.
let existingContent = null;   // null => the content API didn't answer
try {
    const c = file.content;
    const v = (typeof c === "function" ? await c() : c);
    existingContent = (v === undefined || v === null) ? null : String(v);
} catch (e) {
    existingContent = null;
}

// Fall back to file size, so a Templater API change can't silently re-open the hole
if (existingContent === null) {
    existingContent = (file.self?.stat?.size ?? 0) > 0 ? "non-empty" : "";
}

if (existingContent.trim()) {
    new Notice("Content Idea only runs on a new, empty note. Use \"Templater: Create new note from template\".", 8000);
    tR = "";
    return;
}
// ---------------------------------------------------------------------------

let title = file.title;  // current filename (without .md)

// Only prompt for a title if we're on a fresh Untitled note
if (title.startsWith("Untitled")) {
    const input = await tp.system.prompt("Content idea title");

    // If user cancels or leaves blank -> delete this note and abort template
    if (!input || !input.trim()) {
        new Notice("No idea provided. Note will not be created.");
        await app.vault.delete(file.self);  // safe: guard above proved it's empty
        tR = "";
        return;
    }

    title = input.trim();
}

// All content ideas live here, flat. content-type and status do the grouping.
const targetFolder = "09 YT/Ideas";

// Check for duplicates against the real destination, not the current folder
const existing = app.vault.getAbstractFileByPath(`${targetFolder}/${title}.md`);
if (existing && existing.path !== file.path(true)) {
    new Notice(`A content idea with that title already exists: "${title}"`);
    await app.vault.delete(file.self);
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
// Safe to move unconditionally: the guard above proved this note is empty.
if (file.folder(true) !== targetFolder) {
    await file.move(`${targetFolder}/${title}`);
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
