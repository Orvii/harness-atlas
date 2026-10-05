#!/usr/bin/env bash
# Check every evidence URL in harnesses/*.md for rot. Appends a dated report
# to reports/link-rot.md. Distinguishes dead (404/410) from blocked (403/429)
# and redirected (3xx followed) — only dead links are failures.
# Usage: scripts/link-rot.sh   (read-only against the web, writes one report)
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p reports

python3 - <<'PY'
import re, subprocess, datetime, collections

urls = []
seen = set()
for page in sorted(__import__('glob').glob("harnesses/*.md")):
    for m in re.finditer(r"\]\((https?://[^)\s]+)\)", open(page).read()):
        u = m.group(1)
        if u not in seen:
            seen.add(u)
            urls.append((page, u))

status = collections.Counter()
dead, blocked = [], []
for page, u in urls:
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L",
             "--max-time", "20", "-A", "orvii-atlas-linkcheck/1.0", u],
            capture_output=True, text=True, timeout=30)
        code = r.stdout.strip()
    except Exception:
        code = "ERR"
    if code in ("404", "410"):
        status["dead"] += 1
        dead.append((page, u, code))
    elif code in ("403", "429"):
        status["blocked"] += 1
        blocked.append((page, u, code))
    elif code.startswith("2"):
        status["ok"] += 1
    else:
        status[f"other:{code}"] += 1

out = [f"## {datetime.date.today().isoformat()}",
       f"checked {len(urls)} unique evidence urls · " +
       " · ".join(f"{k}: {v}" for k, v in sorted(status.items()))]
if dead:
    out.append("")
    out.append("### dead")
    out += [f"- {p}: {u} ({c})" for p, u, c in dead]
if blocked:
    out.append("")
    out.append("### blocked (bot-gated, not dead)")
    out += [f"- {p}: {u} ({c})" for p, u, c in blocked]
open("reports/link-rot.md", "a").write("\n".join(out) + "\n\n")
print("\n".join(out))
PY
