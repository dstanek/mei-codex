<%*
const file = tp.file;
let title = file.title;  // current filename (without .md)

// Only prompt/rename if we're on a fresh Untitled note
if (title.startsWith("Untitled")) {
    const input = await tp.system.prompt("Short video idea title");

    // If user cancels or leaves blank -> delete this note and abort template
    if (!input || !input.trim()) {
        new Notice("No idea provided. Note will not be created.");
        await app.vault.delete(file.self);  // remove the Untitled note
        tR = "";                            // stop further template output
        return;
    }

    const ideaShort = input.trim();
    title = "Video Idea - " + ideaShort;   // this will be both filename + frontmatter title

    // Build full path to check for duplicates
    const folder = file.folder(true);      // current folder path
    const targetPath = `${folder}/${title}.md`;

    const existing = app.vault.getAbstractFileByPath(targetPath);
    if (existing) {
        new Notice(`A note with that idea already exists: "${title}"`);
        await app.vault.delete(file.self);  // delete the new Untitled note
        tR = "";
        return;
    }

    // At this point we have a non-empty, non-duplicate title: rename the file
    await file.rename(title);
}
-%>
---
title: <% title %>
type: video-idea
status: draft
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
tags: []
---

# <% title %>

your idea here...

[[Content Ideas]]
