---
type: dashboard
---

# Project Dashboard

> Use this dashboard to see which active projects need next actions.

## Active Projects by Domain

### 💼 HPE
```dataview
TABLE status, file.mtime as "Last Modified"
FROM "01 Projects"
WHERE type = "project" AND status = "active" AND domain = "hpe"
SORT file.mtime DESC
```

### 🎓 CWRU
```dataview
TABLE status, file.mtime as "Last Modified"
FROM "01 Projects"
WHERE type = "project" AND status = "active" AND domain = "cwru"
SORT file.mtime DESC
```

### 🚀 Learn Fast
```dataview
TABLE status, file.mtime as "Last Modified"
FROM "01 Projects"
WHERE type = "project" AND status = "active" AND domain = "learn-fast"
SORT file.mtime DESC
```

### 🏠 Personal
```dataview
TABLE status, file.mtime as "Last Modified"
FROM "01 Projects"
WHERE type = "project" AND status = "active" AND domain = "personal"
SORT file.mtime DESC
```

---

## All Active Projects

```dataview
TABLE domain, status, file.mtime as "Last Modified"
FROM "01 Projects"
WHERE type = "project" AND status = "active"
SORT domain ASC, file.name ASC
```

---

## Backlog Projects

```dataview
TABLE domain, file.mtime as "Last Modified"
FROM "01 Projects"
WHERE type = "project" AND status = "backlog"
SORT domain ASC, file.name ASC
```

---

## Projects Missing Metadata

These projects are missing `status` or `domain` in their frontmatter:

```dataview
TABLE type, status, domain
FROM "01 Projects"
WHERE type = "project" AND (!status OR !domain)
```

---

## GTD Check

> **Rule:** Every active project should have at least one next action in Todoist.
>
> Review the active projects above. For each one, ask yourself:
> - Is there a task in Todoist for this project?
> - If not, either add a next action or change status to `backlog`.

**Quick Links:**
- [Todoist Today](https://app.todoist.com/app/today)
- [Todoist Projects](https://app.todoist.com/app/projects)
