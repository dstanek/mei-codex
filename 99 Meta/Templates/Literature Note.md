---
type: literature
title: <% tp.file.title %>
author: <% tp.system.prompt("Author?") %>
status: <% tp.system.suggester(["unread", "reading", "finished"], ["unread", "reading", "finished"]) %>
tags: []
---

# 📖 <% tp.file.title %>

---

## 📄 Summary
<% tp.cursor %>

---

## 💡 Takeaways
- <% tp.cursor %>

---

## ❝ Favorite Quotes
- 

---

## ❓ Questions
- 

---

## ☑ Actions
- 

