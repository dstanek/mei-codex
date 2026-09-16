---
type: zettel
created: 2026-09-16 12:22
source: "staff brainstorm, September 2026"
tags: []
---

# Agents Should Own Behavior, Workflows Should Own Time

The useful split in an assistant system is that the agent owns judgment: what a message means, what to do, and which tool to use.

The workflow engine owns time: when things happen, retries, waiting, and fan-out.

Keeping those separate keeps long-running state out of an LLM conversation and keeps the agent replaceable.

---

## Links

- [[Agentic AI]]
- [[Agent guardrails & infinite loop detection]]

## Source

Staff brainstorm, September 2026.
