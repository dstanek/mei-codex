"""Shared vault plumbing for the project-* skills.

Everything in here is local-filesystem only. Nothing in this module (or in any
script that imports it) can reach Todoist or Google Drive - MCP tools belong to
the agent, not to subprocesses. Remote data always arrives as a JSON file the
agent wrote.

The rules this code enforces live in the vault, not here:
  99 Meta/Conventions.md            - naming, frontmatter, statuses, the GTD rule
  99 Meta/Project Reconciliation.md - invariants, procedure, finding taxonomy
Opaque IDs live in ../domains.json. Keep it that way: when the conventions
change, these scripts should keep working without edits.
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------
# Locating the vault and the shared config
# --------------------------------------------------------------------------

SHARED_DIR = Path(__file__).resolve().parent.parent          # .../.claude/skills/_shared
SKILLS_DIR = SHARED_DIR.parent                                # .../.claude/skills


def find_vault_root(start: Path | str | None = None) -> Path:
    """Walk up from `start` (default: this file) looking for the vault root.

    The vault is identified by having both a `.claude` directory and the
    projects folder named in domains.json, so this keeps working if the vault
    is moved or cloned to another machine.
    """
    here = Path(start).resolve() if start else Path(__file__).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / ".claude" / "skills").is_dir() and (candidate / "99 Meta").is_dir():
            return candidate
    # Fall back to the structural assumption: <vault>/.claude/skills/_shared/scripts
    return SKILLS_DIR.parent.parent


def load_config(config_path: Path | str | None = None) -> dict:
    path = Path(config_path) if config_path else SHARED_DIR / "domains.json"
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# --------------------------------------------------------------------------
# URL <-> ID
# --------------------------------------------------------------------------

def url_id(url) -> str | None:
    """Last path segment of a Todoist/Drive URL, per Conventions.md.

    Tolerates trailing slashes, query strings, fragments, surrounding
    whitespace, and Obsidian's habit of wrapping links in <> or [](). Returns
    None for anything that isn't a usable URL - including a bare ID, which is
    deliberately *not* accepted, because binding is by URL.
    """
    if not isinstance(url, str):
        return None
    text = url.strip().strip("<>")
    match = re.search(r"\((https?://[^)]+)\)", text)      # [label](url)
    if match:
        text = match.group(1)
    if not text.startswith(("http://", "https://")):
        return None
    text = text.split("#", 1)[0].split("?", 1)[0].rstrip("/")
    segment = text.rsplit("/", 1)[-1]
    return segment or None


def todoist_url(project_id: str) -> str:
    return f"https://app.todoist.com/app/project/{project_id}"


def drive_url(folder_id: str) -> str:
    return f"https://drive.google.com/drive/folders/{folder_id}"


# --------------------------------------------------------------------------
# Frontmatter
# --------------------------------------------------------------------------

_SCALAR_QUOTES = ("'", '"')


def _coerce_scalar(raw: str):
    text = raw.strip()
    if not text:
        return None
    if text[0] in _SCALAR_QUOTES and len(text) > 1 and text[-1] == text[0]:
        return text[1:-1]
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        if not inner:
            return []
        return [_coerce_scalar(part) for part in inner.split(",")]
    if re.fullmatch(r"-?\d+", text):
        return int(text)
    if text.lower() in ("true", "false"):
        return text.lower() == "true"
    if text.lower() in ("null", "~"):
        return None
    return text


def parse_frontmatter(path: Path | str) -> dict:
    """Read a note's YAML frontmatter without ever raising on bad input.

    Real vault notes are messy: some have no frontmatter, some have `type:
    [project]` as a list, some have keys with empty values, some have block
    lists. Returning a partial parse plus a `problems` list is far more useful
    to a report than an exception, so nothing here throws.

    Returns {fields, problems, has_frontmatter, body_offset, raw}.
    """
    path = Path(path)
    result = {
        "fields": {},
        "problems": [],
        "has_frontmatter": False,
        "raw": "",
    }
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
        result["problems"].append("file is not valid UTF-8; decoded with replacements")
    except OSError as exc:
        result["problems"].append(f"unreadable: {exc}")
        return result

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        result["problems"].append("no frontmatter block")
        return result

    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() in ("---", "..."):
            end = index
            break
    if end is None:
        result["problems"].append("frontmatter block is never closed")
        return result

    result["has_frontmatter"] = True
    block = lines[1:end]
    result["raw"] = "\n".join(block)

    # Prefer PyYAML when available; fall back to a tolerant line parser so the
    # scripts still run on a bare Python install.
    parsed = None
    try:
        import yaml  # type: ignore

        loaded = yaml.safe_load(result["raw"] or "")
        if isinstance(loaded, dict):
            parsed = loaded
        elif loaded is not None:
            result["problems"].append("frontmatter is not a mapping")
    except ImportError:
        pass
    except Exception as exc:  # noqa: BLE001 - any YAML error is a finding, not a crash
        result["problems"].append(f"YAML did not parse ({type(exc).__name__}); used fallback parser")

    if parsed is None:
        parsed = {}
        current_key = None
        for line in block:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.startswith(("  - ", "- ", "\t- ")) and current_key:
                parsed.setdefault(current_key, [])
                if isinstance(parsed[current_key], list):
                    parsed[current_key].append(_coerce_scalar(line.split("-", 1)[1]))
                continue
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            current_key = key.strip()
            parsed[current_key] = _coerce_scalar(value) if value.strip() else None

    result["fields"] = parsed
    return result


def as_scalar(value):
    """Collapse a one-element list to its element.

    `type: [project]` and `tags: [x]` both show up in this vault. For fields
    that are conceptually scalar, treat a single-element list as the scalar and
    let the caller decide whether to report the shape as a finding.
    """
    if isinstance(value, list):
        if len(value) == 1:
            return value[0]
        if not value:
            return None
    return value


def norm_str(value):
    """Normalize a frontmatter value to a stripped string, or None if empty."""
    value = as_scalar(value)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


# --------------------------------------------------------------------------
# Scanning 01 Projects/
# --------------------------------------------------------------------------

def scan_projects(vault_root: Path | str, config: dict, projects_dir: str | None = None) -> dict:
    """Walk the projects folder and describe what is actually on disk.

    Reports structure the way Project Reconciliation.md defines it: a project is
    a *directory* containing an index note of the same name. Loose .md files and
    index-less directories are structural findings, not projects.
    """
    vault_root = Path(vault_root)
    rel_dir = projects_dir or config["paths"]["projects_dir"]
    root = vault_root / rel_dir

    out = {
        "projects_dir": rel_dir,
        "scanned": [],
        "structural": [],
        "missing_dir": False,
    }
    if not root.is_dir():
        out["missing_dir"] = True
        return out

    valid_domains = set(config["domains"])
    valid_statuses = set(config["statuses"])

    for entry in sorted(root.iterdir(), key=lambda p: p.name.lower()):
        if entry.name.startswith("."):
            continue

        if entry.is_file():
            if entry.suffix.lower() == ".md":
                out["structural"].append({
                    "kind": "loose_file",
                    "path": f"{rel_dir}/{entry.name}",
                    "detail": "a project must be a directory containing an index note of the same name",
                })
            continue

        if not entry.is_dir():
            continue

        index = entry / f"{entry.name}.md"
        support = sorted(
            p.name for p in entry.rglob("*.md")
            if p.is_file() and p != index
        )

        if not index.is_file():
            candidates = sorted(p.name for p in entry.glob("*.md") if p.is_file())
            out["structural"].append({
                "kind": "no_index_note",
                "path": f"{rel_dir}/{entry.name}",
                "detail": (
                    f"expected {entry.name}.md; found: " + ", ".join(candidates)
                ) if candidates else "directory contains no markdown at all",
            })
            continue

        fm = parse_frontmatter(index)
        fields = fm["fields"]

        record = {
            "name": entry.name,
            "dir": f"{rel_dir}/{entry.name}",
            "index_path": f"{rel_dir}/{entry.name}/{entry.name}.md",
            "index_abspath": str(index),
            "has_frontmatter": fm["has_frontmatter"],
            "title": norm_str(fields.get("title")),
            "type": norm_str(fields.get("type")),
            "status": norm_str(fields.get("status")),
            "domain": norm_str(fields.get("domain")),
            "priority": as_scalar(fields.get("priority")),
            "created": norm_str(fields.get("created")),
            "todoist_url": norm_str(fields.get("todoist")),
            "drive_url": norm_str(fields.get("drive")),
            "support_notes": support,
            "problems": list(fm["problems"]),
        }
        record["todoist_id"] = url_id(record["todoist_url"])
        record["drive_id"] = url_id(record["drive_url"])

        # Shape problems worth surfacing, kept factual - never filled in with a
        # guessed default, because a report that invents a priority is worse
        # than one that says the priority is unset.
        if isinstance(fields.get("type"), list):
            record["problems"].append("`type` is a YAML list; Conventions.md expects a string")
        if record["type"] and record["type"] != "project":
            record["problems"].append(f"`type: {record['type']}` - expected `project`")
        if not record["type"]:
            record["problems"].append("`type` is unset")
        if record["domain"] and record["domain"] not in valid_domains:
            record["problems"].append(
                f"`domain: {record['domain']}` is not one of the seven domains"
            )
        if not record["domain"]:
            record["problems"].append("`domain` is unset")
        if record["status"] and record["status"] not in valid_statuses:
            record["problems"].append(
                f"`status: {record['status']}` is not one of {', '.join(sorted(valid_statuses))}"
            )
        if not record["status"]:
            record["problems"].append("`status` is unset")
        if record["todoist_url"] and not record["todoist_id"]:
            record["problems"].append(f"`todoist` is not a usable URL: {record['todoist_url']!r}")
        if record["drive_url"] and not record["drive_id"]:
            record["problems"].append(f"`drive` is not a usable URL: {record['drive_url']!r}")
        if record["title"] and record["title"] != record["name"]:
            record["problems"].append(
                f"`title: {record['title']}` differs from the folder name {record['name']!r}"
            )

        out["scanned"].append(record)

    return out


# --------------------------------------------------------------------------
# Todoist JSON written by the agent
# --------------------------------------------------------------------------

def flatten_overview(overview: dict) -> dict:
    """Turn a get-overview payload into {project_id: {...}} with parent chains."""
    projects: dict[str, dict] = {}

    def walk(nodes, parent_id=None):
        for node in nodes or []:
            pid = node.get("id")
            if not pid:
                continue
            projects[pid] = {
                "id": pid,
                "name": node.get("name"),
                "parent_id": node.get("parentId", parent_id),
                "child_ids": [c["id"] for c in node.get("children") or [] if c.get("id")],
            }
            walk(node.get("children"), pid)

    walk(overview.get("projects"))
    inbox = overview.get("inbox")
    if isinstance(inbox, dict) and inbox.get("id"):
        projects[inbox["id"]] = {
            "id": inbox["id"],
            "name": inbox.get("name", "Inbox"),
            "parent_id": None,
            "child_ids": [],
            "is_inbox": True,
        }
    return projects


def resolve_domain(project_id: str, projects: dict, config: dict) -> dict:
    """Find which domain parent a Todoist project sits under, and how deep.

    Conventions.md requires every project to sit *directly* under its domain
    parent, so depth is reported alongside the domain rather than folded into
    it - depth 2+ is a real finding, not a detail.
    """
    parents = {
        meta["todoist_parent_id"]: key
        for key, meta in config["domains"].items()
    }
    node = projects.get(project_id)
    if not node:
        return {"domain": None, "depth": None, "is_domain_parent": False, "chain": []}
    if project_id in parents:
        return {"domain": parents[project_id], "depth": 0, "is_domain_parent": True, "chain": []}

    chain = []
    depth = 0
    seen = set()
    current = node.get("parent_id")
    while current and current not in seen:
        seen.add(current)
        depth += 1
        chain.append(current)
        if current in parents:
            return {
                "domain": parents[current],
                "depth": depth,
                "is_domain_parent": False,
                "chain": chain,
            }
        parent_node = projects.get(current)
        current = parent_node.get("parent_id") if parent_node else None

    return {"domain": None, "depth": depth, "is_domain_parent": False, "chain": chain}


def one_off_ids(config: dict) -> dict:
    """{one_off_project_id: domain} for every domain that declares one.

    These are permanent buckets, not projects (Conventions.md → One-Off Tasks).
    They never complete, so the GTD rule and the stalled check don't apply, and
    they never get an Obsidian note or Drive folder. Skipping them is a rule
    rather than a preference, which is why it reads from the domains table and
    not from the human's `excluded_todoist_project_ids`.
    """
    return {
        meta["one_off_project_id"]: domain
        for domain, meta in config["domains"].items()
        if meta.get("one_off_project_id")
    }


def domain_parent_ids(config: dict) -> dict:
    """{todoist_parent_id: domain}."""
    return {meta["todoist_parent_id"]: domain for domain, meta in config["domains"].items()}


def derive_status(has_due_dated_task: bool, archived: bool = False) -> str:
    """Derive a project's status from Todoist state.

    Todoist has no project status field, so Conventions.md derives it:
    archived → `archived`; at least one due-dated task → `active`; otherwise
    `backlog` or `on-hold`. The last case is genuinely ambiguous - only a human
    knows whether something is paused or simply not started - so it is returned
    as the pair rather than guessed at.
    """
    if archived:
        return "archived"
    return "active" if has_due_dated_task else "backlog/on-hold"


def status_conflict(note_status: str | None, derived: str) -> str | None:
    """Describe how a note's `status` disagrees with the derived one, or None.

    `backlog` and `on-hold` are interchangeable against a `backlog/on-hold`
    derivation - Todoist cannot tell them apart, so neither can this.
    """
    if not note_status:
        return None
    current = note_status.strip().lower()
    if derived == "backlog/on-hold":
        if current in ("backlog", "on-hold"):
            return None
        if current == "active":
            return "`status: active` but no due-dated task in Todoist"
        if current == "archived":
            return "`status: archived` but the Todoist project is live"
        return f"`status: {current}` is not a known status"
    if current == derived:
        return None
    if derived == "active":
        return f"`status: {current}` but Todoist has a due-dated task, which derives `active`"
    return f"`status: {current}` but Todoist derives `{derived}`"


def task_due_date(task: dict) -> str | None:
    """Extract a YYYY-MM-DD due date from any of the shapes the API returns."""
    for key in ("dueDate", "due_date"):
        value = task.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()[:10]
    for key in ("dueDatetime", "due_datetime"):
        value = task.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()[:10]
    due = task.get("due")
    if isinstance(due, dict):
        for key in ("date", "datetime"):
            value = due.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()[:10]
    return None


def parse_date(value) -> date | None:
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y/%m/%d"):
        try:
            return datetime.strptime(text[:len(fmt) + 2].strip(), fmt).date()
        except ValueError:
            continue
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", text)
    if match:
        return date(*(int(g) for g in match.groups()))
    return None


def load_remote(path: Path | str) -> dict:
    """Load the JSON blob the agent wrote from its MCP calls.

    Accepts either the documented envelope {overview, tasks, ...} or a bare
    get-overview payload, so a hand-assembled file still works.
    """
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if "overview" not in data and "projects" in data:
        data = {"overview": data}
    data.setdefault("overview", {})
    for key in ("tasks", "completed", "activity", "drive_folders"):
        value = data.get(key)
        if value is None:
            data[key] = []
        elif isinstance(value, dict):
            # Tolerate the raw tool response being pasted in whole.
            for inner in ("tasks", "items", "events", "files"):
                if isinstance(value.get(inner), list):
                    data[key] = value[inner]
                    break
            else:
                data[key] = []
    return data


def today_utc() -> date:
    return datetime.now(timezone.utc).date()
