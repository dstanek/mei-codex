---
title: <% tp.file.title %>
type: project
status: backlog
domain: <% tp.system.suggester(["personal", "hpe", "cwru", "learn-fast", "preheat-350", "paige-creations", "freelancing"], ["personal", "hpe", "cwru", "learn-fast", "preheat-350", "paige-creations", "freelancing"], false, "Select domain:") %>
priority: <% tp.system.suggester(["1 — highest", "2", "3", "4 — lowest"], ["1", "2", "3", "4"], false, "Select priority:") %>
created: <% tp.file.creation_date("YYYY-MM-DD HH:mm") %>
todoist: 
drive: 
tags: []
---

# <% tp.file.title %>

## Overview

*Brief description of the project and its goals.*

## Tasks

- [ ] First task

## Support Material

*Material I write lives in this folder. Material I download lives in the Drive folder linked in `drive:` above.*

## Notes

---

> **GTD Reminder:** When changing status to `active`, this project needs all three:
> 1. A Todoist project under the domain parent, with a due-dated next action — `{Project Name}: {Task}`
> 2. A Drive folder at `1. Projects/{Domain}/{Project Name}/`
> 3. Both URLs pasted into `todoist:` and `drive:` above
>
> See [[Project Reconciliation]].
