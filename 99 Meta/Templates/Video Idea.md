<%*
const file = tp.file;
let title = file.title;

if (title.startsWith("Untitled")) {
    const input = await tp.system.prompt("Short video idea title");

    if (!input || !input.trim()) {
        new Notice("No idea provided. Note will not be created.");
        await app.vault.delete(file.self);
        tR = "";
        return;
    }

    const ideaShort = input.trim();
    title = "Video Idea - " + ideaShort;

    const folder = file.folder(true);
    const targetPath = `${folder}/${title}.md`;

    const existing = app.vault.getAbstractFileByPath(targetPath);
    if (existing) {
        new Notice(`A note with that idea already exists: "${title}"`);
        await app.vault.delete(file.self);
        tR = "";
        return;
    }

    await file.rename(title);
}
-%>
---
title: <% title %>
type: video-idea
status: draft
domain: learn-fast
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
tags: []
---

# <% title %>

## Hook

*What grabs attention in the first 5 seconds?*

## Main Points

- 

## Call to Action

*What should viewers do next?*

---

[[Content Ideas]]
