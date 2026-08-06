---
title: Archive Family Videos off Facebook
type: project
status: backlog
domain: personal
priority:
created: 2026-08-05 00:00
todoist:
drive:
tags: []
---

# Archive Family Videos off Facebook

## Overview

Get family video out of Facebook and into storage you actually control. Immediate trigger: a video of my son playing soccer, saved only as a Facebook link.

The underlying problem is that the video exists in exactly one place, and that place is an account on a platform that can change its terms, its API, or its mind. A link is not a copy.

Captured 2026-08-05 from an old bookmark that had survived years of note cleanup precisely because it mattered.

## The video

- `https://www.facebook.com/23301580/videos/1220232785770918/`
- Son playing soccer. Bookmark title recorded only as "(20+) Facebook" — that's the notification badge, not a title, which is why it read as junk for years.

## Tasks

- [ ] Install `yt-dlp` (`sudo pacman -S yt-dlp` — not currently installed; `ffmpeg` already is)
- [ ] Export cookies from a logged-in browser session — required for anything not fully public
- [ ] Download the soccer video and verify it actually plays
- [ ] Check Facebook for other family video worth rescuing while set up to do it
- [ ] Decide where the archive lives — and make sure it's covered by whatever backup you trust
- [ ] Rename with date and context so it's findable in ten years

## How to do it

`yt-dlp` handles Facebook. For a private or friends-only video you must be authenticated, which means passing browser cookies:

```bash
sudo pacman -S yt-dlp

# pull cookies straight from a logged-in browser profile
yt-dlp --cookies-from-browser firefox \
  -o "%(title)s [%(id)s].%(ext)s" \
  "https://www.facebook.com/23301580/videos/1220232785770918/"
```

If `--cookies-from-browser` fails (Chrome on Linux encrypts its cookie DB), export a `cookies.txt` with a browser extension and use `--cookies cookies.txt` instead.

**Better first step:** Facebook's own **Download Your Information** export (Settings → Your Facebook Information) will hand you *everything* at original upload quality in one archive. Slower to arrive, but it captures video you've forgotten about — which is the real risk here. Worth requesting before hand-picking individual URLs.

## Notes

- Facebook re-encodes uploads, so what you download is not the original camera file. If the phone or camera that shot this still has the original, **that's the better source** — check there first.
- This is the argument for doing a sweep rather than a one-off: anything only on Facebook is one account-lockout away from gone.

---

> **GTD Reminder:** When changing status to `active`, create a next action in Todoist.
> Use format: `{Project Name}: {Task}` under the appropriate domain project.
