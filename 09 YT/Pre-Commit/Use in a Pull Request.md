# pre-commit: Use in a Pull Request

## Outline

- Why run pre-commit in CI: catches contributors who skipped local install
- GitHub Actions setup: `pre-commit/action` vs. rolling your own step
- Running `pre-commit run --all-files` vs. only changed files
- Caching the hook environments to speed up CI runs
- Handling auto-fix hooks in CI: fail the job, let the dev fix locally (or push a fix commit)
- Badge and status checks: making pre-commit a required check on the branch

## Script
