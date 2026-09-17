---
type: meta
---
# Email Rules

Rules the **communications** assistant follows when it classifies new inbox threads, every hour from 07:00 to 22:00. Each thread gets exactly one Gmail label:

| Label | Meaning |
|---|---|
| `Staff/Urgent` | Deadline, blocker, money, security, family or health, or someone waiting on me today |
| `Staff/Reply` | Someone asked me something or needs my answer |
| `Staff/Action` | Something to do that isn't a reply: pay, sign, schedule, review |
| `Staff/Waiting` | I sent the last real message; someone else owes the next move |
| `Staff/Reference` | Worth keeping, nothing to do: receipts, confirmations, shipping |
| `Staff/Noise` | Automated or promotional, nothing lost if never read |

Urgent and Reply threads are posted to the staff room; the rest only show up in Gmail. Relabel a thread in Gmail to correct it, and add a rule here when the same mistake repeats.

How the assistant uses this note:

- A rule beats its own judgement. No rule can make it send, archive, mark read or delete — it labels only.
- It reads this note from GitHub, so a change counts once it is pushed.
- It ignores the note unless I made the last change to it. Nothing else in the staff writes to `99 Staff/`.
- It cites rules by number, so keep the list numbered and add new rules at the end.

## Rules

Write one rule per line, in plain language: who or what it matches, and the label. For example: "Anything from @school.org is Urgent", or "GitHub notifications for repos I don't own are Noise".

1. _No rules yet._
