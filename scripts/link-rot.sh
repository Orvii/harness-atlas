#!/usr/bin/env bash
# Check every URL on every harness page for rot. Appends a dated report to
# reports/link-rot.md. Two link classes carry different weight:
#
#   claim-bearing — [src](url) evidence links, quote attributions, parenthetical
#                   citations in prose sections, version-pin sources. A 404 here
#                   means a verdict can no longer be traced: contract violation.
#   provenance    — the "Sources fetched" navigation log at the foot of each
#                   page, which legitimately includes paths that were already
#                   404 when the researcher probed them. Reported, never failed.
#
# Extracts ALL http(s) URLs on the page (markdown-linked AND bare), so a
# parenthetical prose citation cannot slip through the way it did before this
# script's 2026-10-06 rewrite — the old markdown-only regex missed the exact
# dead link (replitai/plan-vs-build-mode) that a manual audit had just caught.
#
# Exit codes: 0 = no claim-bearing dead links; 2 = at least one (CI gates on
# this AFTER committing the report, so the evidence lands even on red runs).
# Usage: scripts/link-rot.sh   (read-only against the web, writes one report)
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p reports

python3 - <<'PY'
import re, subprocess, datetime, collections, glob, sys
from concurrent.futures import ThreadPoolExecutor

URL_RE = re.compile(r"https?://[^\s)\]>,\"']+")
SPLIT = "## Sources fetched"
# A note may cite a URL precisely BECAUSE it is dead — "the architecture page
# X returned HTTP 404", "legacy X returns 404", "docs frozen — X returns 404".
# Such a citation is evidence FOR the claim, not a broken link: killing it or
# "repairing" it would destroy the documented fact. The death must be predicated
# on THIS URL, not merely co-resident in a sentence: "legacy X returns 404; the
# current docs home is Y" cites dead X and LIVE Y in one sentence, and a
# ±240-char window (first attempt) or even a whole-sentence window (second) both
# swept the live Y into the class. So look only at the forward clause after each
# URL — up to the next URL, a newline, or 60 chars — for a 404 predication.
DOCDEAD_FWD_RE = re.compile(r"\b(404|410)\b|\bno longer resolv|\bis (dead|gone)\b|\bdead link\b|\b404s\b", re.I)

def docdead_urls(chunk):
    """URLs whose immediately-following clause documents them as 404/dead.

    The clause ends at the first of: the next URL, a newline, a sentence
    boundary (`. ` — the slice contains no URL, so its periods are real), or
    60 characters. The sentence bound matters: Devin cites a LIVE release-notes
    feed and the *next sentence* mentions an unnamed legacy path that 404s —
    a pure distance window misclassified the live URL (run 3, 2026-10-06).
    """
    ms = list(URL_RE.finditer(chunk))
    out = set()
    for i, m in enumerate(ms):
        end = m.end()
        stop = len(chunk)
        if i + 1 < len(ms):
            stop = min(stop, ms[i + 1].start())     # cut before the next URL
        nl = chunk.find("\n", end)
        if nl != -1:
            stop = min(stop, nl)
        sent = re.search(r"\.\s", chunk[end:stop])
        if sent:
            stop = min(stop, end + sent.start())    # cut at the sentence bound
        fwd = chunk[end:min(end + 60, stop)]
        if DOCDEAD_FWD_RE.search(fwd):
            out.add(m.group(0).rstrip(".;:"))
    return out

# url -> [cls, page]; claim outranks provenance, documented-dead outranks plain
found = {}
RANK = {"provenance": 0, "claim": 1, "claim-documented-dead": 2}
for page in sorted(glob.glob("harnesses/*.md")):
    text = open(page, encoding="utf-8").read()
    at = text.find(SPLIT)
    head, tail = text[:at], text[at:]
    deadset = docdead_urls(head)
    for chunk, cls in ((head, "claim"), (tail, "provenance")):
        for m in URL_RE.finditer(chunk):
            u = m.group(0).rstrip(".;:")
            this_cls = cls
            if cls == "claim" and u in deadset:
                this_cls = "claim-documented-dead"
            prev = found.get(u)
            if prev is None or RANK[this_cls] > RANK[prev[0]]:
                found[u] = [this_cls, page]

def check(item):
    u, (cls, page) = item
    if cls == "claim-documented-dead":
        return (u, cls, page, "DOCDEAD")  # its 404 IS the claim; do not request
    try:
        r = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-L",
             "--max-time", "20", "-A", "orvii-atlas-linkcheck/1.1", u],
            capture_output=True, text=True, timeout=30)
        code = r.stdout.strip()
    except Exception:
        code = "ERR"
    return (u, cls, page, code)

with ThreadPoolExecutor(max_workers=4) as ex:
    results = list(ex.map(check, found.items()))

status = collections.Counter()
dead_claim, dead_prov, blocked, docdead = [], [], [], []
for u, cls, page, code in results:
    if code == "DOCDEAD":
        status["documented-dead"] += 1; docdead.append((page, u)); continue
    status[f"{cls}:{'dead' if code in ('404','410') else 'blocked' if code in ('403','429') else 'ok' if code.startswith('2') else 'other:'+code}"] += 1
    if code in ("404", "410"):
        (dead_claim if cls == "claim" else dead_prov).append((page, u, code))
    elif code in ("403", "429"):
        blocked.append((cls, page, u, code))

n_claim = sum(1 for v in found.values() if v[0] == "claim")
n_dead_doc = len(docdead)
out = [f"## {datetime.date.today().isoformat()}",
       f"checked {len(found)} unique urls — {n_claim} claim-bearing "
       f"({n_dead_doc} cited-as-dead, not requested), "
       f"{len(found)-n_claim-n_dead_doc} provenance · " +
       " · ".join(f"{k}: {v}" for k, v in sorted(status.items()))]
if dead_claim:
    out += ["", "### dead — claim-bearing (contract violations: fix by re-pointing)"]
    out += [f"- {p}: {u} ({c})" for p, u, c in dead_claim]
if docdead:
    out += ["", "### cited-as-dead (the note documents this 404; left alone on purpose)"]
    out += [f"- {p}: {u}" for p, u in docdead]
if dead_prov:
    out += ["", "### dead — provenance (navigation log; recorded, not failures)"]
    out += [f"- {p}: {u} ({c})" for p, u, c in dead_prov]
if blocked:
    out += ["", "### blocked (bot-gated, not dead)"]
    out += [f"- [{cls}] {p}: {u} ({c})" for cls, p, u, c in blocked]
open("reports/link-rot.md", "a", encoding="utf-8").write("\n".join(out) + "\n\n")
print("\n".join(out))
sys.exit(2 if dead_claim else 0)
PY
