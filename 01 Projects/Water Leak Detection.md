---
title: Water Leak Detection
type: project
status: backlog
domain: personal
created: 2026-08-05 00:00
tags: []
---

# Water Leak Detection

## Overview

Networked leak sensors reporting into Home Assistant — so a leak triggers a phone notification rather than a beep nobody's home to hear.

Scoped deliberately to **ESPHome/ESP32** rather than the standalone Arduino build that seeded this idea. A non-networked buzzer only helps if you're already in the room; the point of doing this at all is remote alerting and history.

## Tasks

- [ ] Decide sensor placement — water heater, washer, sump, under sinks, dishwasher
- [ ] Pick an approach: ESPHome on ESP32 with leak probes (DIY, cheap per unit) vs off-the-shelf Zigbee leak sensors (faster, no soldering)
- [ ] Prototype one sensor and confirm it reports to Home Assistant
- [ ] Decide power strategy — battery vs USB. Battery life is the usual failure point for DIY leak sensors
- [ ] Build out remaining sensors once one works end to end
- [ ] Automations: push notification, and consider an auto-shutoff valve for the main if this proves reliable

## Notes

- **Seed reference:** [Arduino Uno Water Alarm](https://www.instructables.com/Arduino-Uno-Water-Alarm/) — 4-step Instructables build. Useful only for the basic probe/detection circuit; it has no networking, so treat it as background rather than a plan.
- The real decision is DIY vs off-the-shelf. DIY is cheaper per sensor and more fun; Zigbee sensors are batteries-included and you'd be done in an evening. Worth being honest about which you actually want before ordering parts.
- Related: [[Home Assistant]] — broader integration TODO list.
- Related: [[Garage Door Automation]] — same ESP-into-HA pattern, also `status: backlog`.
- Related: the ESP32 smart-home-sensor video in [[Watch & Read Queue]].
- Possible tie-in: the gutter/drainage research in [[Home Improvement]], if outdoor water intrusion is part of the concern.

---

> **GTD Reminder:** When changing status to `active`, create a next action in Todoist.
> Use format: `{Project Name}: {Task}` under the appropriate domain project.
