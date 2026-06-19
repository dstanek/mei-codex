# pre-commit: The Pitch - Why Use It (Short)

## Outline

- Open with a relatable pain point: "Have you ever pushed a bug to CI that a linter would have caught?"
- Second pain point: "Or been on a team where nobody agrees on which tools to use — or even when to run them?"
- One sentence on what pre-commit is: a framework for running checks before every commit
- Name two or three things it catches:
  - formatting
  - trailing whitespace
  - secrets
  - linting errors
  - commit messages
- Close with the hook: "Install it once — same tools, same checks, every commit, for the whole team"

## Script

**[On camera, no PiP]**
Have you ever pushed something to CI... only to watch it fail with a linting error that could've caught locally?

Or been on a team where nobody agrees on which tools to use — or even remembers to run them?

**[Cut to screen recording — `.pre-commit-config.yaml` file]**
There's a tool called pre-commit that can help.
pre-commit is a framework that runs checks automatically before every commit. You don't have to remember to run it — it just works.

**[Screen recording — pre-commit running in terminal, hooks scrolling past]**
It catches formatting issues, accidentally committed secrets, and even bad commit messages.

The best part is that you can use existing plugins, or write your own for the ultimate in flexibility.

**[Cut to on camera, no PiP]**
Install it once — same tools, same checks, every commit, for the whole team. It's one of the first things I set up on any new project.
