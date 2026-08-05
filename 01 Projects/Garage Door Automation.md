---
title: Garage Door Automation
type: project
status: backlog
domain: personal
created: 2026-08-05 00:00
tags: []
---

# Garage Door Automation

## Overview

Put the garage door on Home Assistant using **ratgdo** — an ESP32/ESP8266 board that wires directly into the opener and exposes door state and control locally. No vendor cloud, no myQ subscription, no dependency on Chamberlain's API staying open.

Captured from a link saved in the old OneTab dump; promoted to a project on 2026-08-05.

## Tasks

- [ ] Identify the opener model and match it to a ratgdo board variant (v2.5 series vs v3 board, security+ vs dry-contact wiring differ)
- [ ] Order the board
- [ ] Flash firmware — [installation guide](https://ratcloud.llc/pages/installation) covers firmware, wiring, and mounting
- [ ] Wire to the opener
- [ ] Mount the board
- [ ] Add to Home Assistant and confirm state reporting + control
- [ ] Decide on automations (auto-close after N minutes, alert if open after dark, presence-based open)

## Notes

- **Primary reference:** [ratgdo installation guide](https://ratcloud.llc/pages/installation) — firmware installation, wiring diagrams per opener type, mounting suggestions.
- Wiring differs by opener generation, so step 1 gates everything else — worth confirming the model before ordering.
- Related: [[Home Assistant]] (also `status: backlog`) holds the broader integration TODO list.
- Related: the ESP32 smart-home-sensor video in [[Watch & Read Queue]] covers similar ESP-based HA hardware.

---

> **GTD Reminder:** When changing status to `active`, create a next action in Todoist.
> Use format: `{Project Name}: {Task}` under the appropriate domain project.
