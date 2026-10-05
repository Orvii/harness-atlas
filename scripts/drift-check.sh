#!/usr/bin/env bash
# Report version-pin drift: compare matrix.yaml pins against current latest
# GitHub release tags. Mechanical only — no docs re-read, no verdicts.
# Usage: scripts/drift-check.sh   (needs gh + python3; read-only)
set -euo pipefail
cd "$(dirname "$0")/.."

python3 - <<'PY'
import json, re, subprocess

repos = {}
cur = None
for line in open("matrix.yaml"):
    m = re.match(r"\s+repo: \"(.+)\"", line)
    if m:
        cur = m.group(1)
    m = re.match(r"\s+version: \"(.+)\"", line)
    if m and cur:
        repos[cur] = m.group(1)
        cur = None

drift = 0
for repo, pin in sorted(repos.items()):
    path = repo.split(" (")[0].strip()
    path = re.sub(r"^https://github\.com/", "", path).rstrip("/")
    pin = pin.split(" (")[0].strip()
    if "/" not in path:
        continue
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{path}/releases/latest", "--jq", ".tag_name"],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
    except Exception:
        out = ""
    if not out or out.startswith("{"):
        print(f"?  {path}: pin {pin} — no release found (registry-pinned or renamed)")
        continue
    if out != pin:
        drift += 1
        print(f"Δ  {path}: pinned {pin} → latest {out}")
    else:
        print(f"=  {path}: {pin}")
print(f"\n{drift} drifted pin(s). Refresh = new research run + generate.py; see CONTRIBUTING.")
PY
