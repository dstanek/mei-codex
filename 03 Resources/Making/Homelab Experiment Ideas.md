---
type: resource
created: 2026-08-15 19:55
status: reference
domain: personal
tags: []
---

# Homelab Experiment Ideas

Things worth trying in the homelab — services to stand up, configurations to test, tools to evaluate. Nothing here is committed; an experiment leaves this list when it becomes real work *(see [[#Graduating an experiment]])*.

> [!note] Experiments, not the homelab itself
> [[Homelab]] is the project — the running thing you maintain. This is the pile of things you might try *on* it. Keeping them apart means the project stays about work in flight and this stays about candidates.

## Ideas

| Experiment | Why | Stack / Reference | Notes |
| ---------- | --- | ----------------- | ----- |
| Install and test Calibre Web | Browser-based access to the ebook library, and OPDS for reading on any device without syncing files around | [Calibre Web](https://github.com/janeczku/calibre-web) — Docker; needs an existing Calibre library (`metadata.db`) mounted read-write | Check whether it wants its own Calibre install or just the library dir. Worth comparing against [calibre-web-automated](https://github.com/crocodilestick/Calibre-Web-Automated) before committing |

## Tried

The valuable half of the list — what happened, and whether it stuck. An experiment you ran and didn't record is one you'll run again.

| Experiment | Outcome | Kept? |
| ---------- | ------- | ----- |

## Parked

Looked at and set aside — kept so they don't get re-captured.

| Experiment | Why not |
| ---------- | ------- |

## Graduating an experiment

An experiment is a spike: time-boxed, and you're allowed to throw it away. It graduates when you decide to actually run the thing.

| It turns out to be | Goes to |
| ------------------ | ------- |
| A change to the existing homelab | A task in the [[Homelab]] Todoist project |
| A build big enough to stand alone | Its own Todoist project under `Personal`, plus `01 Projects/{Short Name}/` if there's thinking to capture |
| A single afternoon's job | `Personal` → `One-Off`, with a due date |

Then move the row to **Tried** with the outcome, so the idea doesn't resurface.

## Related

- [[Homelab]] — the project this runs against
- [[Homelab Vlan Thoughts]]
- [[ESP32 Project Ideas]] — the things that end up plugged into it
