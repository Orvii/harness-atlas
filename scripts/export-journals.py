#!/usr/bin/env python3
"""Publish the sanitized research journals that generated the current pages.

The evidence contract promises that a stranger can re-run the pipeline. The
raw workflow journals contain researcher working prose ("the task", "this
session") that we do not publish; the generator sanitizes it at load time
anyway, so exporting the *sanitized* results loses nothing the pages do not
already show, and makes regeneration public:

    python3 scripts/generate.py journals/*.jsonl

Usage: python3 scripts/export-journals.py <journal.jsonl> [...]
Writes journals/<name>.jsonl (one sanitized result object per line) and
refreshes journals/MANIFEST.md with the merge order.
"""
import json
import sys
from pathlib import Path

from generate import DEEP_FIELDS, sanitize, slug

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "journals"

# merge order matters: later files win on conflicts (see generate.py)
WAVES = {
    "wf_d9fe5bfc-a50": "wave 1 — first ten harnesses with deep sections",
    "wf_15cd0c06-541": "wave 2 — expansion to seventeen",
    "wf_3decfb86-b1b": "wave 3 — Crush, Amazon Q Developer CLI, Vibe",
    "wf_bf7ccd99-1e2": "wave 4 — Sourcegraph Amp, Factory Droid, JetBrains Junie",
    "wf_7fea83f9-209": "wave 5 — Cursor, Windsurf, Google Jules, Amazon Kiro, Devin",
}


def main(paths):
    OUT.mkdir(exist_ok=True)
    written = []
    for p in paths:
        src = Path(p)
        heads, enrich = [], []
        for line in src.read_text().splitlines():
            if not line.strip():
                continue
            m = json.loads(line)
            r = m.get("result")
            if m.get("type") != "result" or not isinstance(r, dict) or "harness" not in r:
                continue
            if r.get("repo") and r.get("version"):
                heads.append(sanitize(r))
            elif any(r.get(f) for f in DEEP_FIELDS):
                # deep-prose-only results: they enrich a row started earlier
                # in the same file, so they must stay AFTER the head lines
                enrich.append(sanitize(r))
        heads.sort(key=lambda r: slug(r["harness"]))
        enrich.sort(key=lambda r: slug(r["harness"]))
        rows = heads + enrich
        name = src.parent.name  # wf_<id>
        dest = OUT / f"{name}.jsonl"
        # same line shape the workflow journals use, so generate.py reads
        # these files unchanged
        dest.write_text("".join(json.dumps({"type": "result", "result": r}, ensure_ascii=False) + "\n" for r in rows))
        written.append((name, len(rows)))
        print(f"wrote {dest.relative_to(ROOT)} — {len(rows)} harness results")

    order = list(WAVES)
    written.sort(key=lambda wn: order.index(wn[0]) if wn[0] in order else len(order))
    manifest = ["# Journals — the public source of every page", "",
                "Sanitized researcher results, one JSON object per line. Regenerate the",
                "whole atlas from these files alone:", "",
                "    python3 scripts/generate.py journals/*.jsonl", "",
                "Merge order below is the order the waves ran; later files win on",
                "conflicts (see `scripts/generate.py`). Working-prose framing was",
                "stripped at export and the generator re-sanitizes at load, so what you",
                "see here is exactly what the pages were compiled from.", "",
                "| file | harness results | wave |", "|---|---|---|"]
    for name, n in written:
        manifest.append(f"| [{name}.jsonl]({name}.jsonl) | {n} | {WAVES.get(name, 'see research run')} |")
    (OUT / "MANIFEST.md").write_text("\n".join(manifest) + "\n")
    print("wrote journals/MANIFEST.md")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
