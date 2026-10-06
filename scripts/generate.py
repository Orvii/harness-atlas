#!/usr/bin/env python3
"""Regenerate harnesses/*.md, matrix.md and matrix.yaml from a workflow journal.

Usage: python3 scripts/generate.py <journal.jsonl> [more-journals...]
Each journal is a workflow result log: one {"type":"result","result":{...}}
line per researcher. Results carrying "features" supply capability rows;
results carrying "architecture" supply deep-dive sections. Multiple journals
merge by harness name (later files win on conflicts, deep fields merge in).
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


DEEP_FIELDS = ("architecture", "context_mgmt", "ecosystem", "governance", "limitations", "quotes", "docs_map")

# Researcher prose is written for the orchestrator, not for publication: it refers
# to "the task", "this session", "the prompt". The findings stay; the framing that
# only makes sense inside a research run does not. Applied at load time so a
# regenerate can never reintroduce it.
LEAK_SUBS = [
    (r"\bthe task-provided\b", "the legacy"),
    (r"\btask-provided\b", "legacy"),
    (r"\bthe task-referenced\b", "the"),
    (r"\btask-referenced\b", ""),
    (r"\bthe task's own\b", "the"),
    (r"\bthe task's\b", "the"),
    (r"\bthe task pointed at\b", "the shorter path"),
    (r"\bthe task-provided docs URL\b", "the legacy docs URL"),
    (r"\bchecked this session\b", "checked during research"),
    (r"\bfetched this session\b", "fetched during research"),
    (r"\bverified dead this session\b", "verified dead during research"),
    (r"\bthis session\b", "the research run"),
    # NOTE: no "the prompt" rule. It collides with real technical terms
    # (prompt cache, prompt engineering, system prompt) and silently rewrites
    # them. The task/session leaks above are the ones worth catching.
]


def sanitize(text):
    """Strip internal-process framing from researcher prose, recursively."""
    if isinstance(text, str):
        for pat, rep in LEAK_SUBS:
            text = re.sub(pat, rep, text, flags=re.I)
        # collapse horizontal runs only — `\s` would eat the \n\n that markdown
        # paragraphs live on; keep line structure intact.
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text.replace(" )", ")").replace("( ", "(").strip()
    if isinstance(text, list):
        return [sanitize(v) for v in text]
    if isinstance(text, dict):
        return {k: sanitize(v) for k, v in text.items()}
    return text


def manifest_order(journals: list, manifest: Path) -> list:
    """Order journal files by the wave order MANIFEST.md declares.

    "Later waves win on conflicts" is a load-bearing rule, and it is NOT the
    alphabetical order a shell glob produces: `journals/*.jsonl` puts
    `wf_15cd0c06` (wave 2) BEFORE `wf_d9fe5bfc` (wave 1), so running the
    command the README used to print applied wave 1 LAST and its empty deep
    fields overwrote wave 2's prose — ten harness pages lost their
    Architecture/Context/Ecosystem/Governance sections. Sort by the manifest
    when it lists the file, and keep unlisted files after it (newest last,
    alphabetical among themselves, which is the incoming-journal convention).
    """
    if not manifest.exists():
        return list(journals)
    text = manifest.read_text(encoding="utf-8")
    declared = []
    for name in re.findall(r"\((wf_[A-Za-z0-9._-]+\.jsonl)\)", text):
        if name not in declared:
            declared.append(name)
    rank = {name: i for i, name in enumerate(declared)}
    return sorted(
        journals,
        key=lambda j: (rank.get(Path(j).name, len(rank)), Path(j).name),
    )


def load(journals: list) -> list:
    merged = {}
    for journal in journals:
        for line in Path(journal).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            m = json.loads(line)
            r = m.get("result")
            if m.get("type") != "result" or not isinstance(r, dict) or "harness" not in r:
                continue
            r = sanitize(r)
            key = slug(r["harness"])
            if key not in merged and not (r.get("repo") and r.get("version")):
                # a result that carries only deep prose and no head fields
                # cannot start a row; it may only enrich an existing one
                continue
            cur = merged.setdefault(key, {"harness": r["harness"], "features": []})
            for field in ("version_source", "docs_home", "promises", "surprises"):
                cur.setdefault(field, "")
            for field in ("repo", "version", "version_source", "docs_home", "promises", "surprises"):
                if r.get(field):
                    cur[field] = r[field]
            if r.get("features"):
                cur["features"] = r["features"]
            for field in DEEP_FIELDS:
                if r.get(field):
                    cur[field] = r[field]
    return sorted(merged.values(), key=lambda r: slug(r["harness"]))


def main(journals: list, out: Path, manifest: Path = None) -> None:
    # Order by MANIFEST.md's wave sequence, not the order the shell expanded:
    # later waves must win on conflicts (see manifest_order's docstring). The
    # caller passes the repo root as `out`, so the manifest sits beside the
    # journals it describes; an explicit path overrides it (CI regenerates
    # into /tmp from the same checkout).
    if manifest is None:
        candidate = out / "journals" / "MANIFEST.md"
        manifest = candidate if candidate.exists() else None
    if manifest is not None:
        journals = manifest_order(journals, manifest)
    rows = load(journals)
    if not rows:
        sys.exit("no results in journals")

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
        if r.get("architecture"):
            lines += ["", "## Architecture", "", r["architecture"]]
        if r.get("context_mgmt"):
            lines += ["", "## Context management", "", r["context_mgmt"]]
        if r.get("ecosystem"):
            lines += ["", "## Ecosystem", "", r["ecosystem"]]
        if r.get("governance"):
            lines += ["", "## Governance", "", r["governance"]]
        if r.get("limitations"):
            lines += ["", "## Limitations", "", r["limitations"]]
        if r.get("quotes"):
            lines += ["", "## In its own words", ""]
            for q in r["quotes"]:
                lines.append(f"> {q['text']}  \n> — [{q['url']}]({q['url']})")
                lines.append("")
        if r.get("surprises"):
            lines += ["", "## Notable", "", r["surprises"]]
        if r.get("docs_map"):
            # `docs_map` is a list of URLs in 23 of 25 journals, but two
            # (Continue, Zed) recorded it as ONE string in the researcher's own
            # shape: a prose prefix, then entries separated by ` | `, each an
            # URL optionally followed by a parenthesized label. Iterating a
            # string yields its CHARACTERS, so those two pages rendered their
            # "Sources fetched" list one character per line — and because
            # regeneration reproduced the corruption byte-identically, the
            # drift gate stayed green on it. Normalize both shapes to one
            # entry per source.
            docs = r["docs_map"]
            if isinstance(docs, str):
                parts = [part.strip() for part in docs.split(" | ") if part.strip()]
                urls = []
                for part in parts:
                    # The first chunk carries prose that may itself CONTAIN a
                    # URL reference before the real first source
                    # ("…per https://zed.dev/docs/llms.txt): https://…"): take
                    # the LAST `http` in the chunk, so the cited source wins
                    # over its mention in the prefix.
                    at = part.rfind("http")
                    urls.append(part[at:] if at > 0 else part)
            else:
                urls = [str(u) for u in docs]
            lines += ["", "## Sources fetched", ""] + [f"- {u}" for u in urls]
        (out / "harnesses" / f"{s}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

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
    (out / "matrix.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # matrix.yaml — as_of is a property of the research snapshot, not of the
    # run: carry the committed value forward so a regenerate is byte-stable
    src_yaml = Path(__file__).resolve().parent.parent / "matrix.yaml"
    m = re.search(r'^as_of: "?(\d{4}-\d{2}-\d{2})"?', src_yaml.read_text(encoding="utf-8"), re.M) if src_yaml.exists() else None
    as_of = m.group(1) if m else "unknown"
    y = ["# machine-readable matrix; regenerate with scripts/generate.py", f"as_of: {as_of}", "harnesses:"]
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
    (out / "matrix.yaml").write_text("\n".join(y) + "\n", encoding="utf-8")

    # matrix.csv — the same grid for spreadsheet people: one row per harness,
    # one column per capability, verdict words (not symbols)
    import csv
    with (out / "matrix.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["harness", "id", "version"] + [fid for fid, _ in FEATURES])
        for r in rows:
            feats = {f["id"]: f for f in r["features"]}
            w.writerow([r["harness"], slug(r["harness"]), r["version"]] +
                       [feats[fid]["supported"] if fid in feats else "unknown"
                        for fid, _ in FEATURES])
    print(f"wrote {len(rows)} harness pages + matrix.md + matrix.yaml + matrix.csv")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1:], Path(__file__).resolve().parent.parent)
