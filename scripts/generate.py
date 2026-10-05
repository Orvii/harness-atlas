#!/usr/bin/env python3
"""Regenerate harnesses/*.md, matrix.md and matrix.yaml from a workflow journal.

Usage: python3 scripts/generate.py <journal.jsonl>
The journal is the result log of the harness-atlas-research workflow: one
{"type":"result","result":{...}} line per harness researcher.
"""
import json
import re
import sys
from pathlib import Path

FEATURES = [
    ("subagents", "spawn sub-agents / child agents"),
    ("workflow_orchestration", "multi-agent orchestration primitives (scripts, DAGs, teams, swarms)"),
    ("mcp", "Model Context Protocol support"),
    ("hooks_lifecycle", "lifecycle hooks (pre/post tool, session start/stop)"),
    ("skills", "reusable skill / prompt-pack system"),
    ("memory_persistence", "persistent memory across sessions"),
    ("sandboxing", "command sandboxing / permission modes"),
    ("plan_mode", "explicit plan-then-approve mode"),
    ("background_tasks", "background / async task execution"),
    ("ide_integration", "IDE extension (VS Code / JetBrains)"),
    ("model_agnostic", "works with multiple model providers"),
    ("plugins", "third-party plugin / extension API"),
    ("session_resume", "resume previous sessions"),
    ("cost_controls", "token / cost tracking or limits"),
]
SYMBOL = {"yes": "✅", "partial": "◐", "no": "✗", "unknown": "?"}


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main(journal: Path, out: Path) -> None:
    rows = []
    for line in journal.read_text().splitlines():
        if not line.strip():
            continue
        m = json.loads(line)
        if m.get("type") == "result" and isinstance(m.get("result"), dict):
            rows.append(m["result"])
    rows.sort(key=lambda r: slug(r["harness"]))
    if not rows:
        sys.exit("no results in journal")

    (out / "harnesses").mkdir(exist_ok=True)
    for r in rows:
        s = slug(r["harness"])
        feats = {f["id"]: f for f in r["features"]}
        lines = [
            f"# {r['harness']}",
            "",
            f"- **repo:** {r['repo']}",
            f"- **version pin:** `{r['version']}` — {r['version_source']}",
            f"- **docs home:** {r['docs_home']}",
            "",
            "## What it promises",
            "",
            r["promises"],
            "",
            "## Capabilities",
            "",
            "| capability | support | note | evidence |",
            "|---|---|---|---|",
        ]
        for fid, _desc in FEATURES:
            f = feats.get(fid)
            if not f:
                lines.append(f"| {fid} | ? | not researched | |")
                continue
            note = (f.get("note") or "").replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {fid} | {SYMBOL[f['supported']]} {f['supported']} | {note} | [src]({f['evidence_url']}) |")
        if r.get("surprises"):
            lines += ["", "## Notable", "", r["surprises"]]
        (out / "harnesses" / f"{s}.md").write_text("\n".join(lines) + "\n")

    # matrix.md
    md = ["# Capability matrix", "", f"Symbols: {' / '.join(f'{v} {k}' for k, v in SYMBOL.items())}. Cell links to the harness page.", ""]
    md.append("| harness | " + " | ".join(fid for fid, _ in FEATURES) + " |")
    md.append("|---|" + "---|" * len(FEATURES))
    for r in rows:
        feats = {f["id"]: f for f in r["features"]}
        s = slug(r["harness"])
        cells = []
        for fid, _ in FEATURES:
            f = feats.get(fid)
            sym = SYMBOL[f["supported"]] if f else "?"
            cells.append(f"[{sym}]({f'harnesses/{s}.md'})" if f else sym)
        md.append(f"| [{r['harness']}](harnesses/{s}.md) | " + " | ".join(cells) + " |")
    (out / "matrix.md").write_text("\n".join(md) + "\n")

    # matrix.yaml
    y = ["# machine-readable matrix; regenerate with scripts/generate.py", "as_of: 2026-10-05", "harnesses:"]
    for r in rows:
        feats = {f["id"]: f for f in r["features"]}
        y.append(f"  - id: {slug(r['harness'])}")
        y.append(f"    name: {json.dumps(r['harness'])}")
        y.append(f"    repo: {json.dumps(r['repo'])}")
        y.append(f"    version: {json.dumps(r['version'])}")
        y.append("    features:")
        for fid, _ in FEATURES:
            f = feats.get(fid)
            y.append(f"      {fid}: {json.dumps(f['supported']) if f else '\"unknown\"'}")
    (out / "matrix.yaml").write_text("\n".join(y) + "\n")
    print(f"wrote {len(rows)} harness pages + matrix.md + matrix.yaml")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(__file__).resolve().parent.parent)
