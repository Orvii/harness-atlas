#!/usr/bin/env python3
"""Generate the static GitHub Pages site (site/index.html) from the atlas.

Reads matrix.yaml (ids, names, pins, feature verdicts) and harnesses/*.md
(the per-capability note + evidence URL behind every verdict), and emits a
single self-contained HTML file: data embedded as JSON, no backend, no
build step on GitHub's side. Re-run after any regenerate:

    python3 scripts/build_site.py

The site's whole point is the atlas's contract made clickable: every cell
opens a drawer showing the note and the fetched-doc URL the verdict came
from. If a cell has no evidence URL in its page, the drawer says so rather
than linking nowhere.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"

CAPS = [
    "subagents", "workflow_orchestration", "mcp", "hooks_lifecycle", "skills",
    "memory_persistence", "sandboxing", "plan_mode", "background_tasks",
    "ide_integration", "model_agnostic", "plugins", "session_resume",
    "cost_controls",
]
CAP_LABEL = {
    "subagents": "subagents", "workflow_orchestration": "orchestration",
    "mcp": "MCP", "hooks_lifecycle": "hooks", "skills": "skills",
    "memory_persistence": "memory", "sandboxing": "sandboxing",
    "plan_mode": "plan mode", "background_tasks": "background",
    "ide_integration": "IDE", "model_agnostic": "models",
    "plugins": "plugins", "session_resume": "resume",
    "cost_controls": "cost",
}
SYM = {"yes": "●", "partial": "◐", "no": "○", "unknown": "?"}


def yq(raw: str) -> str:
    """Unquote a YAML double-quoted scalar; fall back to raw on oddities."""
    raw = raw.strip()
    if raw.startswith('"') and raw.endswith('"'):
        try:
            return json.loads(raw)
        except Exception:
            return raw[1:-1]
    return raw


def load_yaml():
    order, data = [], {}
    cur = None
    in_features = False
    for line in (ROOT / "matrix.yaml").read_text().splitlines():
        m = re.match(r"  - id: (\S+)", line)
        if m:
            cur = m.group(1)
            order.append(cur)
            data[cur] = {"id": cur, "features": {}}
            in_features = False
            continue
        if cur is None:
            continue
        m = re.match(r'    (name|repo|version): "(.*)"\s*$', line)
        if m:
            data[cur][m.group(1)] = yq(m.group(2))
            continue
        if re.match(r"    features:\s*$", line):
            in_features = True
            continue
        if in_features:
            m = re.match(r"      (\w+): \"(.*)\"\s*$", line)
            if m:
                data[cur]["features"][m.group(1)] = yq(m.group(2))
    return order, data


def load_pages():
    pages = {}
    for p in sorted((ROOT / "harnesses").glob("*.md")):
        t = p.read_text()
        head = {}
        for key in ("repo", "version pin", "docs home"):
            m = re.search(rf"^- \*\*{re.escape(key)}:\*\* (.+)$", t, re.M)
            if m:
                head[key] = m.group(1).strip()
        m = re.search(r"^## What it promises\n\n(.+)$", t, re.M)
        head["promises"] = m.group(1).strip() if m else ""
        # deep sections: the prose behind the grid (architecture, governance, …)
        sections = {}
        for sec in ("Architecture", "Context management", "Ecosystem",
                    "Governance", "Limitations"):
            m = re.search(rf"^## {re.escape(sec)}\n\n(.+?)(?=\n## |\Z)", t, re.M | re.S)
            if m:
                sections[sec.lower().replace(" ", "_")] = m.group(1).strip()
        quotes = []
        qm = re.search(r"^## In its own words\n\n(.+?)(?=\n## |\Z)", t, re.M | re.S)
        if qm:
            for line in qm.group(1).splitlines():
                s = line.strip()
                # skip attribution lines ("> — [url](url)") and md line breaks
                if s.startswith(">") and not s.startswith("> —"):
                    quotes.append(s.lstrip("> ").rstrip())
        rows = {}
        for line in t.splitlines():
            if line.startswith("| ") and not line.startswith("| capability") and not line.startswith("|---"):
                # notes may contain escaped pipes (\|); shield them so the
                # column split stays aligned
                cells = [c.replace("\x00", "|").strip()
                         for c in line.replace("\\|", "\x00").strip("|").split("|")]
                if len(cells) >= 4 and cells[0] in CAPS:
                    # evidence column is either a markdown link or a bare URL
                    m = re.search(r"\]\((https?://[^)]+)\)", cells[3]) or \
                        re.search(r"(https?://\S+)", cells[3])
                    rows[cells[0]] = {"note": cells[2], "evidence": m.group(1).rstrip(")") if m else None}
        pages[p.stem] = {"head": head, "rows": rows,
                         "sections": sections, "quotes": quotes}
    return pages


def main():
    order, data = load_yaml()
    pages = load_pages()
    harnesses = []
    for hid in order:
        d = data[hid]
        pg = pages.get(hid, {"head": {}, "rows": {}})
        caps = []
        for cap in CAPS:
            verdict = d["features"].get(cap, "unknown")
            row = pg["rows"].get(cap, {})
            caps.append({
                "cap": cap,
                "support": verdict if verdict in SYM else "unknown",
                "note": row.get("note", ""),
                "evidence": row.get("evidence"),
            })
        harnesses.append({
            "id": hid,
            "name": d.get("name", hid),
            "version": d.get("version", ""),
            "repo": d.get("repo", ""),
            "docs": pg["head"].get("docs home", ""),
            "promises": pg["head"].get("promises", ""),
            "caps": caps,
            "sections": pg.get("sections", {}),
            "quotes": pg.get("quotes", []),
        })

    as_of = re.search(r"^as_of: \"?(\d{4}-\d{2}-\d{2})\"?",
                      (ROOT / "matrix.yaml").read_text(), re.M)
    as_of = as_of.group(1) if as_of else "unknown"
    version = re.search(r'^version: "(.+)"', (ROOT / "CITATION.cff").read_text(), re.M)
    version = version.group(1) if version else "dev"

    payload = {"as_of": as_of, "version": version, "caps": CAPS,
               "cap_label": CAP_LABEL, "harnesses": harnesses}
    html = TEMPLATE.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
    SITE.mkdir(exist_ok=True)
    (SITE / "index.html").write_text(html)
    style = re.search(r"<style>(.*?)</style>", TEMPLATE, re.S).group(1)
    (SITE / "method.html").write_text(METHOD_TEMPLATE
                                      .replace("__CSS__", style)
                                      .replace("__AS_OF__", as_of)
                                      .replace("__VERSION__", version)
                                      .replace("__N__", str(len(harnesses))))
    (SITE / ".nojekyll").write_text("")
    print(f"wrote {SITE.relative_to(ROOT)}/index.html ({len(html)//1024} KB) — {len(harnesses)} harnesses, {len(CAPS)} capabilities, as of {as_of}")
    missing = sum(1 for h in harnesses for c in h["caps"] if c["support"] != "unknown" and not c["evidence"])
    if missing:
        print(f"WARNING: {missing} non-unknown cells have no evidence URL in their page")
    return 0


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>harness-atlas — the capability grid, clickable</title>
<meta name="description" content="What 25 AI coding harnesses promise and support. Every cell opens the note and the fetched-doc URL it was read from. Versions pinned, snapshot dated.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0b0806; --bg2: #100b07; --panel: #140d08; --panel2: #1c130b; --ink: #F8F5F2;
  --muted: #b7a496; --faint: #6e5c50; --line: #3a2c1e;
  --accent: #FE9106; --accent2: #FEAF12; --accent3: #F05F03;
  --yes: #FE9106; --partial: #FEAF12; --no: #5c4c3f; --unknown: #6e5c50;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #f4efe6; --bg2: #ece4d6; --panel: #fbf8f2; --panel2: #efe7d9; --ink: #1d150c;
    --muted: #6e5c50; --faint: #9a8877; --line: #d8cbb8;
    --yes: #c96c00; --partial: #a37300; --no: #b3a493; --unknown: #9a8877;
  }
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 14px; line-height: 1.55;
}
::selection { background: var(--accent); color: #0b0806; }
.wrap { max-width: 1240px; margin: 0 auto; padding: 0 28px; }

/* ---- masthead: a broadsheet head, not a landing hero ---- */
header.mast {
  display: grid; grid-template-columns: minmax(0, 1fr) 330px;
  gap: 44px; align-items: start; padding: 54px 0 30px;
  border-bottom: 3px double var(--line);
}
.eyebrow {
  font-size: 11px; letter-spacing: .3em; text-transform: uppercase;
  color: var(--accent); margin: 0 0 16px;
}
h1 {
  font-family: Fraunces, Georgia, serif; font-weight: 640; font-style: italic;
  font-size: clamp(38px, 4.6vw, 62px); line-height: 1.04; margin: 0 0 16px;
  letter-spacing: -.015em;
}
h1 em { font-style: normal; color: var(--accent); }
.lede { max-width: 58ch; color: var(--muted); font-size: 14.5px; margin: 0; }
.lede b { color: var(--ink); font-weight: 600; }
.chips { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; }
.chip {
  border: 1px solid var(--line); background: var(--panel); color: var(--muted);
  padding: 5px 12px; border-radius: 999px; font-size: 12px;
}
.chip b { color: var(--accent2); font-weight: 600; }

/* the specimen plate: key + live sample + ledger, one framed object */
.plate {
  border: 1px solid var(--line); background: var(--panel);
  padding: 20px 18px 16px; position: relative;
}
.plate::before {
  content: ""; position: absolute; inset: 5px; pointer-events: none;
  border: 1px solid color-mix(in srgb, var(--line) 65%, transparent);
}
.plate-title {
  margin: 0 0 12px; font-size: 10.5px; letter-spacing: .26em;
  text-transform: uppercase; color: var(--faint);
}
.key { list-style: none; margin: 0 0 14px; padding: 0; }
.key li { display: flex; gap: 10px; align-items: baseline; margin: 7px 0; font-size: 12px; color: var(--muted); }
.key i { font-style: normal; font-size: 15px; width: 14px; text-align: center; color: var(--unknown); flex: none; }
.key b { color: var(--ink); font-weight: 600; }
.plate-grid {
  display: grid; grid-template-columns: repeat(8, 1fr); gap: 3px;
  padding: 10px 0; border-block: 1px dotted var(--line);
}
.plate-grid span { text-align: center; font-size: 11px; line-height: 1.6; color: var(--unknown); }
.plate-cap { margin: 8px 0 12px; font-size: 10.5px; color: var(--faint); }
.ledger { margin: 0; }
.ledger div {
  display: flex; justify-content: space-between; align-items: baseline; gap: 12px;
  border-bottom: 1px dotted var(--line); padding: 5px 0;
}
.ledger div:last-child { border-bottom: 0; }
.ledger dt {
  font-size: 10px; letter-spacing: .16em; text-transform: uppercase; color: var(--faint);
}
.ledger dd { margin: 0; font-size: 12px; color: var(--ink); }
.ledger dd b { color: var(--accent2); font-weight: 600; }
.ledger a { color: var(--accent); text-decoration: none; }
.ledger a:hover { text-decoration: underline; }

/* ---- toolbar ---- */
.toolbar {
  position: sticky; top: 0; z-index: 20; padding: 10px 0;
  background: var(--bg); border-bottom: 1px solid var(--line);
  display: flex; gap: 10px; align-items: center; flex-wrap: wrap;
}
.toolbar input, .toolbar select {
  background: var(--panel); color: var(--ink); border: 1px solid var(--line);
  border-radius: 4px; padding: 7px 10px; font: inherit; font-size: 12.5px;
}
.toolbar input { min-width: 200px; }
.toolbar input:focus, .toolbar select:focus, .cell:focus-visible, a:focus-visible,
button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.count { margin-left: auto; color: var(--accent2); font-size: 12px; }

/* ---- the grid ----
   The grid is its own scroll plate on desktop: overflow on the wrapper makes
   it the sticky reference, so thead sticks to the plate top (not the
   viewport) — which is exactly right for a 25×14 matrix. On small screens the
   plate opens up to page flow and the head goes static; the name column
   stays pinned for horizontal reading. */
.gridwrap { overflow-x: auto; padding: 22px 0 60px; }
table.grid { border-collapse: separate; border-spacing: 0; width: 100%; min-width: 1150px; }
table.grid thead th {
  position: sticky; top: 0; z-index: 5; background: var(--bg);
  font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase;
  color: var(--faint); font-weight: 500; padding: 9px 6px 7px; text-align: center;
  white-space: nowrap; height: 33px;
}
table.grid thead th.hname { text-align: left; left: 0; z-index: 6; }
table.grid thead tr.census th {
  top: 33px; height: auto; padding: 0 6px 9px;
}
.cbar { display: flex; height: 4px; width: 100%; background: var(--line); }
.cbar i { display: block; height: 100%; }
.ccount { display: block; margin-top: 4px; font-size: 9.5px; letter-spacing: .04em; color: var(--faint); }
table.grid tbody th {
  position: sticky; left: 0; z-index: 4; background: var(--bg);
  text-align: left; padding: 0; font-weight: 500;
}
table.grid tbody th a {
  display: block; padding: 8px 14px 8px 2px; color: var(--ink);
  text-decoration: none; white-space: nowrap; font-size: 13px;
}
table.grid tbody th a:hover { color: var(--accent); }
table.grid tbody th .idx {
  color: var(--faint); font-size: 10px; margin-right: 9px;
  font-variant-numeric: tabular-nums;
}
table.grid tbody th .pin { display: block; color: var(--faint); font-size: 10px; padding: 0 14px 7px 27px; }
tbody tr:nth-child(even) th, tbody tr:nth-child(even) td { background: var(--bg2); }
tr.row { animation: rise .35s ease-out both; }
@keyframes rise { from { opacity: 0; transform: translateY(6px); } }
td { text-align: center; padding: 0; }
.cell {
  width: 100%; height: 42px; border: 0; background: transparent; cursor: pointer;
  color: var(--unknown); font-size: 14px; line-height: 1;
  transition: background .15s ease-out, transform .15s ease-out;
}
.cell[data-s="yes"] { color: var(--yes); }
.cell[data-s="partial"] { color: var(--partial); }
.cell[data-s="no"] { color: var(--no); }
.cell:hover { background: var(--panel2); transform: scale(1.14); }
td.dim .cell { opacity: .2; }
td.hot { background: color-mix(in srgb, var(--accent) 9%, transparent); }
.cmp {
  position: absolute; right: 6px; top: 11px; width: 24px; height: 24px;
  background: transparent; border: 1px solid var(--line); color: var(--faint);
  border-radius: 4px; cursor: pointer; font-size: 12px; line-height: 1;
}
.cmp:hover { color: var(--accent); border-color: var(--accent); }
.cmp[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: #0b0806; }

/* ---- compare plate ---- */
#compare { padding: 6px 0 10px; }
#compare .eyebrow { margin-bottom: 8px; }
#cmp-summary { color: var(--muted); font-size: 12px; margin: 0 0 10px; }
#compare table { border-collapse: collapse; width: 100%; }
#compare th, #compare td { border: 1px solid var(--line); padding: 6px 10px; font-size: 12.5px; text-align: center; }
#compare thead th { background: var(--panel); color: var(--ink); font-size: 13px; }
#compare th:first-child, #compare td:first-child { text-align: left; color: var(--muted); width: 160px; }
#compare tr.diff td { background: color-mix(in srgb, var(--accent) 7%, transparent); }
#compare tr.diff td:first-child { border-left: 2px solid var(--accent); color: var(--ink); }
#compare .pin { color: var(--faint); font-size: 10.5px; }

/* ---- drawer ---- */
.drawer {
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 40;
  background: var(--panel); border-top: 2px solid var(--accent);
  transform: translateY(102%); transition: transform .28s cubic-bezier(.3,0,.2,1);
  box-shadow: 0 -18px 60px color-mix(in srgb, #000 45%, transparent);
  max-height: 46vh; overflow-y: auto;
}
.drawer.open { transform: translateY(0); }
.drawer .wrap { padding: 22px 28px 30px; }
.drawer h2 {
  font-family: Fraunces, Georgia, serif; font-style: italic; font-weight: 600;
  font-size: 25px; margin: 0 0 4px;
}
.drawer .sub { color: var(--accent2); font-size: 11.5px; letter-spacing: .12em; text-transform: uppercase; margin: 0 0 14px; }
.drawer .note { color: var(--muted); max-width: 88ch; }
.drawer .meta { margin-top: 14px; display: flex; gap: 16px; flex-wrap: wrap; align-items: center; font-size: 12.5px; }
.drawer .meta a { color: var(--accent); }
.drawer .meta .verdict { color: var(--ink); font-weight: 600; }
.drawer .meta button {
  background: transparent; border: 1px solid var(--line); color: var(--muted);
  border-radius: 4px; padding: 3px 10px; cursor: pointer; font: inherit; font-size: 11.5px;
}
.drawer .meta button:hover { color: var(--accent); border-color: var(--accent); }
.drawer .tabs { display: flex; gap: 6px; margin-bottom: 16px; }
.drawer .tabs button {
  background: transparent; border: 1px solid var(--line); color: var(--muted);
  border-radius: 999px; padding: 5px 14px; cursor: pointer; font: inherit; font-size: 11.5px;
  letter-spacing: .06em; text-transform: uppercase;
}
.drawer .tabs button[aria-selected="true"] {
  background: var(--accent); border-color: var(--accent); color: #0b0806; font-weight: 600;
}
.drawer h3 {
  font-size: 11px; letter-spacing: .2em; text-transform: uppercase;
  color: var(--accent2); margin: 18px 0 6px; font-weight: 600;
}
.drawer blockquote {
  margin: 10px 0; padding: 10px 16px; border-left: 2px solid var(--accent);
  background: var(--panel2); color: var(--ink); font-family: Fraunces, Georgia, serif;
  font-style: italic; font-size: 15px;
}
.drawer button.close {
  position: absolute; top: 14px; right: 20px; background: transparent;
  border: 1px solid var(--line); color: var(--muted); border-radius: 4px;
  padding: 4px 10px; cursor: pointer; font: inherit;
}
noscript p { padding: 20px 0; color: var(--muted); }
noscript a { color: var(--accent); }

footer { border-top: 1px solid var(--line); padding: 30px 0 60px; color: var(--faint); font-size: 12.5px; }
footer a { color: var(--accent); }
footer p { max-width: 80ch; }
@media (min-width: 981px) {
  /* plate mode: the matrix scrolls inside its own frame, head pinned to it.
     No top padding here — the scrollport top must BE the plate top, or a
     band of rows peeks above the pinned head. */
  .gridwrap { max-height: calc(100vh - 120px); overflow: auto; padding-top: 0; margin-top: 22px; }
}
@media (max-width: 980px) {
  header.mast { grid-template-columns: 1fr; gap: 26px; }
  .plate { max-width: 420px; }
  table.grid thead th { position: static; }
}
@media (prefers-reduced-motion: reduce) {
  tr.row { animation: none; }
  .drawer { transition: none; }
  .cell { transition: none; }
}
</style>
</head>
<body>
<header class="wrap mast">
  <div>
    <p class="eyebrow">Orvii research set · evidence-contract atlas</p>
    <h1>What coding agents <em>promise</em> — and what they <em>support</em>.</h1>
    <p class="lede">Twenty-five harnesses, fourteen capabilities, one snapshot date. <b>Click any cell</b>: it opens the note and the fetched-doc URL the verdict was read from. A cell you cannot trace does not exist here — it is marked <span aria-label="unknown">?</span>.</p>
  </div>
  <aside class="plate" aria-label="How to read the grid">
    <p class="plate-title">reading the plate</p>
    <ul class="key">
      <li><i style="color:var(--yes)">●</i><div><b>yes</b> — the doc describes it</div></li>
      <li><i style="color:var(--partial)">◐</i><div><b>partial</b> — described with a stated limitation; the note names it</div></li>
      <li><i style="color:var(--no)">○</i><div><b>no</b> — the doc states its absence</div></li>
      <li><i>? </i><div><b>unknown</b> — no fetched page answers; never a guess</div></li>
    </ul>
    <div class="plate-grid" id="plate-grid" aria-hidden="true"></div>
    <p class="plate-cap">the grid at a glance — a live sample of its cells</p>
    <dl class="ledger">
      <div><dt>snapshot</dt><dd><b id="chip-date"></b></dd></div>
      <div><dt>release</dt><dd><b id="chip-ver"></b></dd></div>
      <div><dt>rows</dt><dd><span id="chip-n"></span> harnesses · 14 capabilities</dd></div>
      <div><dt>method</dt><dd><a href="./method.html">why trust this →</a></dd></div>
    </dl>
  </aside>
</header>

<div class="wrap toolbar" role="search">
  <input id="q" type="search" placeholder="filter harnesses…" aria-label="Filter harnesses by name">
  <select id="cap" aria-label="Highlight one capability column">
    <option value="">all capabilities</option>
  </select>
  <select id="verdict" aria-label="Show only rows containing a verdict">
    <option value="">any verdict</option>
    <option value="yes">rows with ● yes</option>
    <option value="partial">rows with ◐ partial</option>
    <option value="no">rows with ○ no</option>
    <option value="unknown">rows with ? unknown</option>
  </select>
  <select id="sort" aria-label="Sort rows">
    <option value="">matrix order</option>
    <option value="az">name a–z</option>
    <option value="doc">most documented first</option>
    <option value="cont">most contested first</option>
  </select>
  <span class="count" id="count" aria-live="polite"></span>
</div>

<section class="wrap" id="compare" hidden>
  <p class="eyebrow">side by side · rows where they disagree are lit</p>
  <p id="cmp-summary"></p>
  <div style="overflow-x:auto"><table id="cmp-table"></table></div>
</section>

<main class="wrap gridwrap">
  <table class="grid" id="grid"></table>
  <noscript><p>The clickable grid needs JavaScript. The canonical copy of the data is plain markdown: <a href="https://github.com/Orvii/harness-atlas/blob/main/matrix.md">matrix.md</a>, one row per harness, every cell citing its source.</p></noscript>
</main>

<div class="drawer" id="drawer" role="dialog" aria-modal="false" aria-labelledby="d-title">
  <div class="wrap">
    <button class="close" id="d-close" aria-label="Close evidence drawer">esc ✕</button>
    <div class="tabs" role="tablist">
      <button id="tab-cell" role="tab" aria-selected="true">cell evidence</button>
      <button id="tab-deep" role="tab" aria-selected="false">this harness, in depth</button>
    </div>
    <div id="pane-cell">
      <h2 id="d-title"></h2>
      <p class="sub" id="d-sub"></p>
      <p class="note" id="d-note"></p>
      <div class="meta" id="d-meta"></div>
    </div>
    <div id="pane-deep" hidden>
      <h2 id="d-title2"></h2>
      <p class="sub" id="d-sub2"></p>
      <div id="d-sections"></div>
      <div id="d-quotes"></div>
    </div>
  </div>
</div>

<footer class="wrap">
  <p>The grid answers <i>does the doc describe it, on the snapshot date</i> — not <i>is it good</i>. Gates (flags, tiers, OS limits, maturity labels) live in the notes and in <a href="https://github.com/Orvii/harness-atlas/blob/main/GATES.md">GATES.md</a>; trust layers in <a href="https://github.com/Orvii/harness-atlas/blob/main/TRUST.md">TRUST.md</a>. Versions are pinned per row; a pin you cannot diff is labelled as such.</p>
  <p>Source: <a href="https://github.com/Orvii/harness-atlas">Orvii/harness-atlas</a> · method: <a href="https://github.com/Orvii/harness-atlas/blob/main/METHODOLOGY.md">METHODOLOGY.md</a> · stale pins are reported monthly by CI, never silently fixed.</p>
</footer>

<script>
const DATA = __DATA__;
const SYM = { yes: "●", partial: "◐", no: "○", unknown: "?" };
const WORD = { yes: "documented yes", partial: "partial — read the note", no: "documented no", unknown: "unknown / unverified" };
const grid = document.getElementById("grid");
const drawer = document.getElementById("drawer");
const capSel = document.getElementById("cap");
const verSel = document.getElementById("verdict");
const sortSel = document.getElementById("sort");

document.getElementById("chip-date").textContent = DATA.as_of;
document.getElementById("chip-ver").textContent = DATA.version;
document.getElementById("chip-n").textContent = DATA.harnesses.length;
DATA.caps.forEach(c => {
  const o = document.createElement("option");
  o.value = c; o.textContent = DATA.cap_label[c];
  capSel.appendChild(o);
});

/* the plate's sample: real cells, first rows × first columns */
(function plate() {
  const box = document.getElementById("plate-grid");
  box.innerHTML = DATA.harnesses.slice(0, 6).map(h =>
    h.caps.slice(0, 8).map(c => `<span style="color:var(--${c.support})">${SYM[c.support]}</span>`).join("")
  ).join("");
})();

function census() {
  return "<tr class='census'>" + "<th class='hname' aria-hidden='true'></th>" + DATA.caps.map(c => {
    const n = { yes: 0, partial: 0, no: 0, unknown: 0 };
    DATA.harnesses.forEach(h => n[h.caps.find(x => x.cap === c).support]++);
    const tot = DATA.harnesses.length;
    const w = k => (n[k] / tot * 100).toFixed(1) + "%";
    return `<th title="${n.yes} yes · ${n.partial} partial · ${n.no} no · ${n.unknown} unknown"><span class="cbar"><i style="width:${w("yes")};background:var(--yes)"></i><i style="width:${w("partial")};background:var(--partial)"></i><i style="width:${w("no")};background:var(--no)"></i><i style="width:${w("unknown")};background:var(--unknown)"></i></span><span class="ccount">${n.yes}/${tot} doc</span></th>`;
  }).join("") + "</tr>";
}

const docs = h => h.caps.filter(c => c.support === "yes").length;
const contested = h => h.caps.filter(c => c.support === "partial" || c.support === "unknown").length;
function currentRows() {
  let rows = [...DATA.harnesses];
  const q = document.getElementById("q").value.trim().toLowerCase();
  if (q) rows = rows.filter(h => h.name.toLowerCase().includes(q));
  const v = verSel.value;
  if (v) rows = rows.filter(h => h.caps.some(c => c.support === v));
  const s = sortSel.value;
  if (s === "az") rows.sort((a, b) => a.name.localeCompare(b.name));
  else if (s === "doc") rows.sort((a, b) => docs(b) - docs(a));
  else if (s === "cont") rows.sort((a, b) => contested(b) - contested(a));
  return rows;
}

function render(rows) {
  const head = "<thead><tr><th class='hname'>harness · version pin</th>" +
    DATA.caps.map(c => `<th scope="col" data-cap="${c}">${DATA.cap_label[c]}</th>`).join("") + "</tr>" +
    census() + "</thead>";
  const body = "<tbody>" + rows.map((h, i) =>
    `<tr class="row" style="animation-delay:${Math.min(i * 25, 400)}ms">` +
    `<th scope="row"><a href="https://github.com/Orvii/harness-atlas/blob/main/harnesses/${h.id}.md"><span class="idx">${String(i + 1).padStart(2, "0")}</span>${esc(h.name)}<span class="pin">${esc(h.version.split(" — ")[0].slice(0, 42))}</span></a><button class="cmp" data-h="${h.id}" aria-pressed="false" title="add to comparison" aria-label="compare ${esc(h.name)}">⇄</button></th>` +
    h.caps.map(c =>
      `<td data-cap="${c.cap}"><button class="cell" data-s="${c.support}" data-h="${h.id}" data-c="${c.cap}" aria-label="${esc(h.name)} — ${DATA.cap_label[c.cap]}: ${WORD[c.support]}">${SYM[c.support]}</button></td>`
    ).join("") + "</tr>"
  ).join("") + "</tbody>";
  grid.innerHTML = head + body;
  document.getElementById("count").textContent = rows.length + " of " + DATA.harnesses.length + " harnesses";
  applyCap();
}
function esc(s) { return String(s).replace(/[&<>"]/g, m => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m])); }

function applyCap() {
  const cap = capSel.value;
  grid.querySelectorAll("td[data-cap]").forEach(td => {
    td.classList.toggle("dim", !!cap && td.dataset.cap !== cap);
    td.classList.toggle("hot", !!cap && td.dataset.cap === cap);
  });
}
const rerender = () => render(currentRows());
capSel.addEventListener("change", applyCap);
document.getElementById("q").addEventListener("input", rerender);
verSel.addEventListener("change", rerender);
sortSel.addEventListener("change", rerender);

const picked = [];
function renderCompare() {
  const box = document.getElementById("compare");
  const tbl = document.getElementById("cmp-table");
  const hs = picked.map(id => DATA.harnesses.find(h => h.id === id)).filter(Boolean);
  if (hs.length < 2) { box.hidden = true; tbl.innerHTML = ""; return; }
  box.hidden = false;
  const head = "<thead><tr><th>capability</th>" +
    hs.map(h => `<th>${esc(h.name)}<br><span class="pin">${esc(h.version.split(" — ")[0].slice(0, 34))}</span></th>`).join("") +
    "</tr></thead>";
  let diffs = 0;
  const body = "<tbody>" + DATA.caps.map(cap => {
    const cells = hs.map(h => h.caps.find(c => c.cap === cap));
    const vals = cells.map(c => c.support);
    const differs = new Set(vals).size > 1;
    if (differs) diffs++;
    return `<tr class="${differs ? "diff" : ""}"><td>${DATA.cap_label[cap]}</td>` +
      cells.map(c => `<td style="color:var(--${c.support})">${SYM[c.support]}</td>`).join("") +
      "</tr>";
  }).join("") + "</tbody>";
  tbl.innerHTML = head + body;
  document.getElementById("cmp-summary").textContent =
    diffs + " of " + DATA.caps.length + " capabilities disagree — lit rows are where the choice matters.";
}
document.getElementById("grid").addEventListener("click", e => {
  const b = e.target.closest(".cmp");
  if (!b) return;
  e.stopPropagation();
  const i = picked.indexOf(b.dataset.h);
  if (i >= 0) picked.splice(i, 1);
  else if (picked.length >= 4) picked.shift();
  else picked.push(b.dataset.h);
  document.querySelectorAll(".cmp").forEach(x =>
    x.setAttribute("aria-pressed", picked.includes(x.dataset.h)));
  renderCompare();
  if (picked.length >= 2) document.getElementById("compare").scrollIntoView({ block: "nearest" });
});

let CURRENT = null;
function showTab(which) {
  const cell = which === "cell";
  document.getElementById("tab-cell").setAttribute("aria-selected", cell);
  document.getElementById("tab-deep").setAttribute("aria-selected", !cell);
  document.getElementById("pane-cell").hidden = !cell;
  document.getElementById("pane-deep").hidden = cell;
}
document.getElementById("tab-cell").addEventListener("click", () => showTab("cell"));
document.getElementById("tab-deep").addEventListener("click", () => showTab("deep"));

function renderDeep(h) {
  document.getElementById("d-title2").textContent = h.name;
  document.getElementById("d-sub2").textContent = "version pin: " + h.version.slice(0, 90);
  const order = ["architecture", "context_management", "ecosystem", "governance", "limitations"];
  const label = { architecture: "architecture", context_management: "context management",
                  ecosystem: "ecosystem", governance: "governance", limitations: "limitations" };
  document.getElementById("d-sections").innerHTML = order.filter(k => h.sections[k]).map(k =>
    `<h3>${label[k]}</h3><p>${esc(h.sections[k])}</p>`).join("") ||
    "<p>No deep sections recorded for this harness.</p>";
  document.getElementById("d-quotes").innerHTML = h.quotes.length
    ? "<h3>in its own words</h3>" + h.quotes.map(q => `<blockquote>${esc(q)}</blockquote>`).join("")
    : "";
}

function openCell(h, c) {
  CURRENT = h;
  document.getElementById("d-title").textContent = h.name + " · " + DATA.cap_label[c.cap];
  document.getElementById("d-sub").textContent = SYM[c.support] + " " + WORD[c.support] + " · as of " + DATA.as_of;
  document.getElementById("d-note").textContent = c.note || "No note recorded for this cell — see the harness page.";
  const meta = document.getElementById("d-meta");
  meta.innerHTML =
    (c.evidence ? `<span>read from: <a href="${esc(c.evidence)}" rel="noopener noreferrer">${esc(c.evidence.replace(/^https?:\/\//, "").slice(0, 64))}</a></span>` : "<span>no evidence URL recorded — see page</span>") +
    `<span>pin: <span class="verdict">${esc(h.version.slice(0, 72))}</span></span>` +
    (h.docs ? `<span><a href="${esc(h.docs)}" rel="noopener noreferrer">docs home</a></span>` : "") +
    `<button id="d-copy">copy cell link</button>`;
  document.getElementById("d-copy").addEventListener("click", ev => {
    navigator.clipboard.writeText(location.href).then(() => {
      ev.target.textContent = "copied ✓";
      setTimeout(() => { ev.target.textContent = "copy cell link"; }, 1500);
    }).catch(() => { ev.target.textContent = location.hash; });
  });
  renderDeep(h);
  showTab("cell");
  drawer.classList.add("open");
  history.replaceState(null, "", "#" + h.id + "/" + c.cap);
  document.getElementById("d-close").focus();
}
grid.addEventListener("click", e => {
  const b = e.target.closest(".cell");
  if (!b) return;
  const h = DATA.harnesses.find(x => x.id === b.dataset.h);
  openCell(h, h.caps.find(x => x.cap === b.dataset.c));
});
function closeDrawer() {
  drawer.classList.remove("open");
  history.replaceState(null, "", location.pathname + location.search);
}
document.getElementById("d-close").addEventListener("click", closeDrawer);
document.addEventListener("keydown", e => { if (e.key === "Escape") closeDrawer(); });

render(DATA.harnesses);
/* deep link: #<harness>/<capability> opens that cell's evidence */
const hm = location.hash.match(/^#([a-z0-9-]+)\/([a-z_]+)$/);
if (hm) {
  const h = DATA.harnesses.find(x => x.id === hm[1]);
  const c = h && h.caps.find(x => x.cap === hm[2]);
  if (h && c) openCell(h, c);
}
</script>
</body>
</html>
"""

METHOD_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>harness-atlas — why trust this</title>
<meta name="description" content="How every cell in the harness-atlas grid is produced, pinned, and kept honest — and what a cell is not.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>__CSS__
.wrap { max-width: 760px; }
main.prose { padding: 20px 28px 60px; }
main.prose h2 {
  font-family: Fraunces, Georgia, serif; font-style: italic; font-weight: 620;
  font-size: 30px; margin: 40px 0 10px;
}
main.prose p, main.prose li { color: var(--muted); max-width: 70ch; }
main.prose b { color: var(--ink); }
main.prose a { color: var(--accent); }
main.prose ol { padding-left: 22px; }
main.prose li { margin: 8px 0; }
main.prose code { color: var(--accent2); }
.pull {
  border-left: 2px solid var(--accent); background: var(--panel);
  padding: 14px 18px; margin: 22px 0; font-family: Fraunces, Georgia, serif;
  font-style: italic; font-size: 17px; color: var(--ink); max-width: 60ch;
}
</style>
</head>
<body>
<header class="wrap">
  <p class="eyebrow"><a href="./" style="color:inherit;text-decoration:none">← harness-atlas</a> · method</p>
  <h1>Why trust <em>this</em> grid.</h1>
  <p class="lede">Every capability comparison of coding agents ages in weeks, and most are written from memory. This one inverts the process: researchers fetch official docs during the run, and no verdict enters the grid without the URL and the verbatim sentence it was read from.</p>
  <div class="chips">
    <span class="chip">snapshot <b>__AS_OF__</b></span>
    <span class="chip">release <b>__VERSION__</b></span>
    <span class="chip"><b>__N__</b> harnesses · 14 capabilities</span>
  </div>
</header>
<main class="wrap prose">
  <h2>The evidence contract</h2>
  <p>A cell in the grid is not an opinion. It is a record that, on the snapshot date, a named document page stated something specific. Four things travel with every verdict:</p>
  <ol>
    <li><b>The primary source.</b> The vendor's own documentation. Blogs, aggregators and press releases are never the citation for a cell.</li>
    <li><b>A verbatim quote.</b> The sentence the verdict was read from, kept in the research journal behind each page. Paraphrase is for notes; the quote is the contract.</li>
    <li><b>A version pin.</b> Open repos pin a release tag you can check out. Closed-source products pin whatever the vendor publishes — an npm dist-tag, a changelog page, an API self-label — and the row <i>says which</i>, because a pin you cannot diff is weaker evidence and should look weaker.</li>
    <li><b><code>unknown</code> over a guess.</b> If no fetched page answers the question, the cell is <code>?</code>. Absence of evidence, recorded as such.</li>
  </ol>
  <div class="pull">A cell you cannot trace does not exist here.</div>

  <h2>What a cell is — and is not</h2>
  <p><b>It is:</b> "on this date, this doc page described this capability." <code>●</code> means described; <code>◐</code> means described <i>with a stated limitation</i>, and the note names it; <code>○</code> means the doc states the absence; <code>?</code> means nobody fetched a page that answers.</p>
  <p><b>It is not:</b> a quality rating, a recommendation, or a version-free truth. A <code>●</code> on sandboxing says the doc describes a sandbox — whether it holds is <a href="https://github.com/Orvii/harness-atlas/blob/main/TRUST.md">TRUST.md</a>'s layer analysis plus your own judgment. Gates (flags, tiers, OS limits, maturity labels, deprecations) live in <a href="https://github.com/Orvii/harness-atlas/blob/main/GATES.md">GATES.md</a>, because a matrix of five-valued cells would be unreadable and the notes are where the truth fits.</p>

  <h2>How a row is produced</h2>
  <ol>
    <li>One researcher per harness fetches the official docs live and returns a structured record: verdicts with URLs and quotes, a version pin with its source, and five deep sections (architecture, context management, ecosystem, governance, limitations).</li>
    <li>Records land in a journal; a mechanical generator (<code>scripts/generate.py</code>) compiles journals into pages and the matrix. Prose is sanitized at load time so internal research framing can never reach a published page.</li>
    <li>Nothing is hand-edited after generation. A correction means re-running the research, not patching a cell.</li>
  </ol>

  <h2>What happens when a vendor ships</h2>
  <p>Vendors ship weekly; the grid does not move between research runs — by design. Instead, CI runs <code>drift-check.sh</code> monthly: every pin compared against the current release (or reported as not-diffable for closed-source rows), and the result committed to <a href="https://github.com/Orvii/harness-atlas/blob/main/reports/drift-log.md">reports/drift-log.md</a>. A link-rot checker separates dead evidence URLs from blocked ones. Drift is a research task, never a silent edit: the log is the honest distance between the snapshot and today.</p>

  <h2>Audit us</h2>
  <p>The whole point is that a stranger can check any cell in five minutes with nothing but the page and the URL it cites. <a href="https://github.com/Orvii/harness-atlas/blob/main/VERIFYING.md">VERIFYING.md</a> is the procedure, and the <a href="https://github.com/Orvii/harness-atlas/issues/new/choose">issue templates</a> are the door: a correction report must carry the doc URL and the verbatim contradicting sentence. Disagreements about interpretation are welcome too — the note column should argue with itself in the open.</p>
  <p>Cite the release, not the date: cells move as vendors ship. <code>__VERSION__</code> is the current one.</p>
</main>
<footer class="wrap">
  <p>Orvii — Open, Research, Vision, Innovation &amp; Ideas. <a href="https://github.com/Orvii/harness-atlas">source</a> · <a href="https://github.com/Orvii/harness-atlas/blob/main/METHODOLOGY.md">METHODOLOGY.md</a> · <a href="./">the grid</a></p>
</footer>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())
