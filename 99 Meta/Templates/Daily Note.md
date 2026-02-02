---
created: <% tp.file.creation_date() %>
---
#DailyNote

# <% moment(tp.file.title,'YYYY-MM-DD').format("dddd, MMMM DD, YYYY") %>

⪡ [[07 Daily/<% tp.date.now("YYYY-MM-DD", -1) %>|prev]] ═════ [[07 Daily/<% tp.date.now("YYYY-MM-DD", 1) %>|next]] ⪢

<%* if (tp.date.now("ddd") == "Sun") { %>
---
## Weekly Review

### 🗂 Capture & Collect
- [ ] Gather loose papers, notes, and digital inputs.
- [ ] Process Personal Gmail
- [ ] Process Case Gmail
- [ ] Process HPE Email
- [ ] Process Obsidian Inbox
- [ ] Process Evernote Inbox

### ✅ Clarify & Update
- [ ] Update projects and ensure each has a next action.
- [ ] Clean up your calendar (past week for follow-ups, upcoming week for prep).

### 🔄 Reflect & Organize
- [ ] Review Next Actions list (add/remove tasks).
- [ ] Review Waiting For list (follow up if needed).
- [ ] Review Projects list (ensure progress).
- [ ] Review Someday/Maybe list (move anything actionable).
- [ ] Identify key priorities for the upcoming week.
<%* } else if (tp.date.now("ddd") == "Sat") { %>
## 💭 Reflections

<% tp.file.cursor() %>
<%* } else { %>
---
## ❗ Top Priorities

- [ ] <% tp.file.cursor() %>

---
## 📅 Top Meetings To Prepare For

- [ ] 

<%* } %>

---
### Notes created today
```dataview
List FROM "" WHERE file.cday = date("<%tp.date.now("YYYY-MM-DD")%>") SORT file.ctime asc
```

### Notes last touched today
```dataview
List FROM "" WHERE file.mday = date("<%tp.date.now("YYYY-MM-DD")%>") SORT file.mtime asc
```
