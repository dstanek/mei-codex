---
title: Browser-Based Jupyter
type: project
status: backlog
domain: cwru
created: 2026-08-05 00:00
tags: []
---

# Browser-Based Jupyter

## Overview

Let students run Jupyter notebooks **in the browser** for the CWRU Python intro course — no local Python install, no `pip` troubleshooting, no "it works on my machine" in week one.

The environment-setup tax is the single biggest time sink at the start of an intro course, and it falls hardest on the students who are already least confident. Removing it means class time goes to Python instead of PATH variables.

Captured 2026-08-05. This existed only as a saved Google search for "jupyterlite" in an old bookmark dump — the search was a reminder to self, so it's recorded properly here.

## Options to evaluate

| Option | How it works | Trade-off |
| ------ | ------------ | --------- |
| **JupyterLite** | Full Jupyter running client-side via WebAssembly; served as static files | No server to run or pay for, works offline once loaded. Limited package support — anything needing C extensions or network may not work |
| **Pyodide** | CPython compiled to WebAssembly; the engine underneath JupyterLite | Lower level; useful if you want a custom UI rather than the Jupyter interface |
| **Google Colab** | Hosted notebooks | Zero setup, students likely know it. Requires Google accounts, and you don't control the environment or its availability |
| **JupyterHub** | You host real Jupyter servers per student | Full Python, no WASM limits. You now operate a server, handle auth, and pay for compute |

## Tasks

- [ ] Decide hosting model — static (JupyterLite) vs hosted (JupyterHub) vs third-party (Colab)
- [ ] Test whether the packages the course needs actually work under WebAssembly — this gates the JupyterLite option entirely
- [ ] Check how students save and submit work; JupyterLite persists to browser storage, which is easy to lose
- [ ] Confirm it works on a Chromebook and on locked-down lab machines
- [ ] Build a trial notebook from one real lesson and run a student through it
- [ ] Decide fallback for anything WASM can't handle

## Notes

- **The package question is the gate.** JupyterLite is elegant until the course needs a library that won't compile to WASM. Worth testing against the actual curriculum before committing.
- **Student work persistence is the sharp edge.** Browser-local storage means clearing cookies loses homework. Whatever the choice, submission needs to not depend on it.
- Related: [[Python Intro Course Ideas]] — `status: active`, the course this supports.
- Related: [[Spring Schedule]].

---

> **GTD Reminder:** When changing status to `active`, create a next action in Todoist.
> Use format: `{Project Name}: {Task}` under the appropriate domain project.
