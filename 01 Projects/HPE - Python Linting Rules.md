---
type: project
status: active
domain: hpe
---

# HPE - Python Linting Rules

## Overview

Create custom linting rules that can be used in ruff configuration to extend the standard ruleset. These rules will enforce HPE-specific coding standards and patterns across Python projects.

## Goals

- Define HPE-specific Python coding standards
- Implement custom ruff rules to enforce these standards
- Create a reusable configuration that can be shared across HPE Python projects

## Scope

- Custom rule definitions for ruff
- Documentation of HPE Python standards
- Example configurations for common project types

## Tasks

- [ ] Research ruff plugin/extension mechanisms
- [ ] Document desired linting rules (what patterns to enforce/prevent)
- [ ] Implement first custom rule as proof of concept
- [ ] Test rules against existing codebase
- [ ] Package for distribution across projects

## Resources

- [Ruff documentation](https://docs.astral.sh/ruff/)
- [Writing custom rules](https://docs.astral.sh/ruff/contributing/plugins/)

## Rule Ideas

*Original brainstorm of possible rules to implement or find:*

- No `str()` in logging (use lazy formatting)
- Must use a logger (no print statements)
- No re-raising exceptions without context
- *(Add more rules as identified)*

## Notes

*Add implementation notes and decisions here as the project progresses.*

