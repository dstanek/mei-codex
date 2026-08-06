---
created: <% tp.file.creation_date() %>
---
#DailyNote

# <% moment(tp.file.title,'YYYY-MM-DD').format("dddd, MMMM DD, YYYY") %>

⪡ [[07 Daily/<% tp.date.now("YYYY-MM-DD", -1) %>|prev]] ═════ [[07 Daily/<% tp.date.now("YYYY-MM-DD", 1) %>|next]] ⪢

<%* if (tp.date.now("ddd") == "Sun") { %>
---
## Weekly Review

### 🗂 Capture & Clarify

Empty each one. Every item goes through the tree in [[99 Meta/Conventions#Clarify]] — nothing stays.

- [ ] Todoist Inbox
- [ ] Obsidian `00 Inbox/`
- [ ] Personal Gmail
- [ ] Case Gmail
- [ ] HPE Email
- [ ] Evernote Inbox
- [ ] Loose paper and downloads

### 📅 Calendar
- [ ] Clean up your calendar (past week for follow-ups, upcoming week for prep).

### 🔄 Reflect
- [ ] Run `/project-reconcile`, then work down the report.
- [ ] Review the **Waiting For** filter — chase anything gone quiet.
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
