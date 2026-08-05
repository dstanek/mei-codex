#!/usr/bin/env python3
"""Walk `01 Projects/` and emit what is on disk as JSON.

Local filesystem only - this cannot and must not reach Todoist or Drive.

    python3 scan_vault.py                       # JSON to stdout
    python3 scan_vault.py --out /tmp/vault.json
    python3 scan_vault.py --summary             # human-readable, for eyeballing

Output:
  projects_dir  the folder scanned, relative to the vault root
  scanned[]     one record per well-formed project directory
  structural[]  loose .md files and directories with no index note
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vaultlib import find_vault_root, load_config, scan_projects  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--vault", help="vault root (default: auto-detected from this script's location)")
    ap.add_argument("--config", help="path to domains.json")
    ap.add_argument("--dir", dest="projects_dir",
                    help="folder to scan, relative to the vault root (default: 01 Projects)")
    ap.add_argument("--out", help="write JSON here instead of stdout")
    ap.add_argument("--summary", action="store_true", help="print a human summary instead of JSON")
    args = ap.parse_args()

    vault = Path(args.vault) if args.vault else find_vault_root()
    config = load_config(args.config)
    result = scan_projects(vault, config, args.projects_dir)
    result["vault_root"] = str(vault)

    if result["missing_dir"]:
        print(f"error: {vault / result['projects_dir']} does not exist", file=sys.stderr)
        return 1

    if args.summary:
        print(f"vault: {vault}")
        print(f"{len(result['scanned'])} project note(s) in {result['projects_dir']}/\n")
        for rec in result["scanned"]:
            bits = [
                f"status={rec['status'] or '-'}",
                f"domain={rec['domain'] or '-'}",
                f"todoist={rec['todoist_id'] or '-'}",
                f"drive={rec['drive_id'] or '-'}",
            ]
            print(f"  {rec['name']}\n      " + "  ".join(bits))
            for problem in rec["problems"]:
                print(f"      ! {problem}")
        if result["structural"]:
            print(f"\n{len(result['structural'])} structural finding(s):")
            for item in result["structural"]:
                print(f"  [{item['kind']}] {item['path']} - {item['detail']}")
        return 0

    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out} ({len(result['scanned'])} projects, "
              f"{len(result['structural'])} structural findings)")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
