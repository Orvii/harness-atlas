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
    # repos with multiple release streams (CLI + SDK tags): latest may belong
    # to another stream. Fall back to the newest tag in the pin's prefix family.
    pin_prefix = re.match(r"^[^-]*", pin).group(0)
    tag_prefix = re.match(r"^[^-]*", out).group(0)
    if pin_prefix != tag_prefix:
        tags = subprocess.run(
            ["gh", "api", f"repos/{path}/releases", "--jq", ".[].tag_name"],
            capture_output=True, text=True, timeout=30,
        ).stdout.split()
        stable = [t for t in tags if not re.search(r"nightly|-(pre|rc|beta|alpha)\b", t, re.I)]
        same = [t for t in stable if re.match(r"^[^-]*", t).group(0) == pin_prefix]
        if same:
            out = same[0]
    if out != pin:
        drift += 1
        print(f"Δ  {path}: pinned {pin} → latest {out}")
    else:
        print(f"=  {path}: {pin}")
print(f"\n{drift} drifted pin(s). Refresh = new research run + generate.py; see CONTRIBUTING.")
PY
