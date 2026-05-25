---
title: Video Idea - pre-commit crash course
type: video-idea
status: draft
domain: personal
created: 2026-03-10 18:11
tags: []
---

# Video Idea - Stop Committing Mistakes: A pre-commit Crash Course

*(Target length: 3–5 min)*

## Outline

### Hook

**Hook (0:00–0:30)**

- Open with: _"Do you have a suite of commands you run before you commit? Linter, formatter, type checker... How about we automate that."_
- Show a quick flash of the manual workflow: running `ruff`, `black`, `mypy` one by one in the terminal. Speak to creating shell scripts or Makefiles to have a single command.
- Cut to: one `git commit` that runs them all automatically

### Main Points

#### What is pre-commit?

*(0:30–1:00)*

- Git hooks are scripts Git runs automatically at key points — like before a commit
- pre-commit is a framework that manages those hooks for you
- Single declarative config file replaces hand-rolled shell scripts — versioned, shareable, and language-aware
- Hooks run in isolated environments — no polluting your virtualenv
- Language-agnostic: works with Python, JS, Go, anything
- Hooks can lint, format, scan for secrets, validate config files, etc.

#### Installation

*(1:00–1:30)*

- Installed once globally — it lives outside your project's dependencies
- Install via `pip`, `pipx` (recommended — keeps it global), `brew`, or `choco`
- Verify: `pre-commit --version`

#### Simple Configuration

*(1:30–2:40)*

- Create `.pre-commit-config.yaml` in your project root
- Demo config using hooks your Python audience will recognize immediately:
    - `ruff` — linting
    - `ruff-format` or `black` — formatting
    - `mypy` — type checking (optional, can mention it's slower)
    - `check-yaml` / `end-of-file-fixer` from `pre-commit-hooks` — free wins
- `pre-commit install` to register the hooks
- Demo: make a dirty commit → watch it get blocked and auto-fixed
- Quick tip: `pre-commit run --all-files` to run manually
- Maintenance tip: `pre-commit autoupdate` to keep hooks fresh

#### GitHub Actions Enforcement

*(2:40–3:40)*

- Problem: developers may skip `pre-commit install`, or bypass hooks with `git commit --no-verify` — CI enforcement catches both
- Solution: enforce the same checks in CI using `pre-commit/action`
- Show a minimal workflow YAML (trigger on `push`/`pull_request`)
- Mention `--show-diff-on-failure` for clear feedback in CI logs

#### Wrap-up

*(3:40–4:10)*

- Recap: install once, configure hooks, enforce in CI
- CTA: link to pre-commit.com hook registry — hundreds of ready-made hooks
- Tease next video or drop a like/subscribe (hook dependencies and custom hooks)

## Script

### Hook (0:00–0:30)

Hey, quick question — do you have a little ritual before you commit code? Maybe you run `ruff`, then `black`, then `mypy`... one by one, in the terminal, every single time?

*(show terminal: running ruff, black, mypy manually)*

Maybe you got fancy and wrapped them all in a Makefile target or a shell script. Totally valid. But there's a better way — one that's automatic, shareable with your whole team, and runs *before the commit even happens*.

*(cut to: single `git commit` triggering all the checks)*

That's `pre-commit`, and in the next few minutes I'll show you how to set it up from scratch.

---

### What is pre-commit? (0:30–1:00)

So first — what even is this thing?

Git has a feature called *hooks* — little scripts it can run automatically at key moments. Like right before you make a commit. The problem is, setting those up by hand is kind of a pain. You're writing shell scripts, managing paths, hoping your teammates actually copy the right files...

`pre-commit` fixes all of that. It's a framework that manages your git hooks for you. You get one clean config file, checked into your repo, that everyone on your team shares. The hooks run in isolated environments so they don't mess with your virtualenv. And it's not just Python — it works with JavaScript, Go, whatever you're using.

Think: linting, formatting, secret scanning, config validation — all automated, all consistent.

---

### Installation (1:00–1:30)

Alright, let's get it installed. The key thing here is that `pre-commit` lives *outside* your project's dependencies — you install it once, globally, and it works across all your projects.

The easiest way is with `pipx`:

```bash
pipx install pre-commit
```

You can also use `pip`, `brew`, or `choco` — whatever fits your setup. Then just verify it worked:

```bash
pre-commit --version
```

Great. Now let's actually use it.

---

### Simple Configuration (1:30–2:40)

In your project root, create a file called `.pre-commit-config.yaml`. This is where all the magic lives.

Here's a solid starting config for a Python project:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.4
    hooks:
      - id: ruff
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
```

You've got `ruff` for linting and formatting, `mypy` for type checking — heads up, mypy can be a bit slow, so some folks leave it out of the git hook and just run it in CI — and then a couple of free wins from the `pre-commit-hooks` repo: checking your YAML files are valid, and making sure files end with a newline.

Now register the hooks with your repo:

```bash
pre-commit install
```

That's it. Now let's see what happens when we try to commit something messy.

*(demo: make a dirty commit — watch it get blocked and auto-fixed)*

See that? It caught the issue, fixed it automatically, and blocked the commit so you can review before trying again. Clean.

A couple more useful commands to know:

```bash
pre-commit run --all-files   # run manually on everything
pre-commit autoupdate        # bump your hooks to the latest versions
```

Run `autoupdate` every now and then to keep things fresh.

---

### GitHub Actions Enforcement (2:40–3:40)

Here's the thing though — `pre-commit install` has to be run manually. And some people forget. Or they use `git commit --no-verify` to bypass it entirely. We've all been there.

So the real safety net is enforcing the same checks in CI. That way, even if someone skips the local hook, the pull request won't pass.

Here's a minimal GitHub Actions workflow to do exactly that:

```yaml
name: pre-commit

on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - uses: pre-commit/action@v3.0.1
        with:
          extra_args: --show-diff-on-failure
```

Drop that in `.github/workflows/pre-commit.yml` and you're done. The `--show-diff-on-failure` flag is a nice touch — it shows you exactly what changed in the CI logs so you're not guessing.

---

### Wrap-up (3:40–4:10)

So to recap: install `pre-commit` once globally, add a `.pre-commit-config.yaml` to your project, run `pre-commit install`, and back it up with a CI check. That's really it.

And we've only scratched the surface here — there are hundreds of ready-made hooks over at `pre-commit.com`. Secrets scanners, JSON validators, spell checkers... seriously worth browsing.

If you want to go deeper, the next step is writing your own custom hooks or handling hook dependencies — I'll cover that in a future video.

If this was helpful, drop a like — it helps a lot. And I'll see you in the next one.

[[Content Ideas]]
