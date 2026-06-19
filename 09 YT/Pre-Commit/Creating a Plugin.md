# pre-commit: Creating a Plugin

## Outline

- When to write your own hook vs. using an existing one
- Repo structure: any language works, just needs an entry point
- The `.pre-commit-hooks.yaml` manifest: `id`, `name`, `entry`, `language`, `types`
- Language options: `python`, `node`, `script`, `system`, `docker`
- Writing a minimal hook script (show a simple Python example)
- Testing locally with `pre-commit try-repo`
- Publishing: tag a release so others can pin a `rev`
- Pointing your own project at a local or remote custom hook

## Script
