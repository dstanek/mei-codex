---
type: meta
created: 2026-09-17 14:22
tags: []
---
# Email Rules

Rules the **communications** assistant follows when it classifies new inbox threads, every hour from 07:00 to 22:00. Each thread gets exactly one Gmail label:

| Label | Meaning |
|---|---|
| `Staff/Urgent` | Deadline, blocker, money, security, family or health, or someone waiting on me today |
| `Staff/Reply` | Someone asked me something or needs my answer |
| `Staff/Action` | Something to do that isn't a reply: pay, sign, schedule, review |
| `Staff/Waiting` | I sent the last real message; someone else owes the next move |
| `Staff/Research` | An article, paper, talk or release worth my time, judged against [[Interests]]. Nothing asked of me |
| `Staff/Reference` | Worth keeping, nothing to do: receipts, confirmations, shipping |
| `Staff/Noise` | Automated or promotional, nothing lost if never read |

A thread gets exactly one label. Research only applies when nothing is asked of me; if a message both links an article and needs an answer, it is Reply.

Urgent and Reply threads are posted to the staff room; the rest only show up in Gmail. Relabel a thread in Gmail to correct it, and add a rule here when the same mistake repeats.

How the assistant uses this note:

- A rule beats its own judgement. No rule can make it send, archive, mark read or delete — it labels only.
- It reads this note from GitHub, so a change counts once it is pushed.
- It ignores the note unless I made the last change to it. Nothing else in the staff writes to `99 Staff/`.
- It cites rules by number, so keep the list numbered and add new rules at the end.

## Rules

Write one rule per line, in plain language: who or what it matches, and the label. For example: "Anything from @school.org is Urgent", or "GitHub notifications for repos I don't own are Noise".

1. Mail carrying an article, paper, talk or release that matches [[Interests]] is Research. A newsletter counts when at least one piece genuinely matches; otherwise it is Noise.
