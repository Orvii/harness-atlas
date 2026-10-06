#!/usr/bin/env python3
"""Fold journals-incoming/*.json into journals/wf_<wave>.jsonl.

One researcher result per file (the shape independent agents write); the
generator wants workflow-journal lines. This is the adapter, and it validates
the evidence contract on the way in: every non-unknown feature must carry an
http evidence URL, every harness a repo-or-vendor pin with its source.

Usage: python3 scripts/merge-incoming.py <wave-id>
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCOMING = ROOT / "journals-incoming"
FEATURE_IDS = {
    "subagents", "workflow_orchestration", "mcp", "hooks_lifecycle", "skills",
    "memory_persistence", "sandboxing", "plan_mode", "background_tasks",
    "ide_integration", "model_agnostic", "plugins", "session_resume",
    "cost_controls",
}


def main(wave: str) -> int:
    files = sorted(INCOMING.glob("*.json"))
    if not files:
        sys.exit("no incoming files")
    lines, problems = [], []
    for f in files:
        r = json.loads(f.read_text())
        name = r.get("harness")
        if not name:
            problems.append(f"{f.name}: no harness name")
            continue
        if not (r.get("version") and r.get("version_source")):
            problems.append(f"{f.name}: version pin without source")
        for feat in r.get("features", []):
            if feat["id"] not in FEATURE_IDS:
                problems.append(f"{f.name}: unknown capability {feat['id']}")
            if feat["supported"] != "unknown" and not str(feat.get("evidence_url", "")).startswith("http"):
                problems.append(f"{f.name}/{feat['id']}: non-unknown without evidence URL")
        lines.append(json.dumps({"type": "result", "result": r}, ensure_ascii=False))
    if problems:
        print("CONTRACT VIOLATIONS — fix the incoming files first:")
        for p in problems:
            print(" -", p)
        return 1
    dest = ROOT / "journals" / f"{wave}.jsonl"
    dest.write_text("\n".join(lines) + "\n")
    print(f"wrote {dest.relative_to(ROOT)} — {len(lines)} harness results")
    print("remember: append the wave to journals/MANIFEST.md, generate.py's")
    print("wave order, regen-check.yml and release.yml triggers")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "wf_v34-incoming"))
