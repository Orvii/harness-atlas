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
        pages[p.stem] = {"head": head, "rows": rows}
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
    (SITE / ".nojekyll").write_text("")
    print(f"wrote site/index.html ({len(html)//1024} KB) — {len(harnesses)} harnesses, {len(CAPS)} capabilities, as of {as_of}")
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
  --bg: #0b0806; --panel: #140d08; --panel2: #1c130b; --ink: #F8F5F2;
  --muted: #b7a496; --faint: #6e5c50; --line: #3a2c1e;
  --accent: #FE9106; --accent2: #FEAF12; --accent3: #F05F03;
  --yes: #FE9106; --partial: #FEAF12; --no: #5c4c3f; --unknown: #6e5c50;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #f4efe6; --panel: #fbf8f2; --panel2: #efe7d9; --ink: #1d150c;
    --muted: #6e5c50; --faint: #9a8877; --line: #d8cbb8;
    --yes: #d97400; --partial: #b07d00; --no: #b3a493; --unknown: #9a8877;
  }
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 14px; line-height: 1.55;
  background-image:
    radial-gradient(1200px 500px at 85% -10%, color-mix(in srgb, var(--accent) 7%, transparent), transparent 70%),
    repeating-linear-gradient(0deg, transparent 0 39px, color-mix(in srgb, var(--line) 35%, transparent) 39px 40px);
}
::selection { background: var(--accent); color: #0b0806; }
.wrap { max-width: 1280px; margin: 0 auto; padding: 0 28px; }

header { padding: 64px 0 28px; }
.eyebrow {
  font-size: 11px; letter-spacing: .32em; text-transform: uppercase;
  color: var(--accent); margin: 0 0 14px;
}
h1 {
  font-family: Fraunces, Georgia, serif; font-weight: 640; font-style: italic;
  font-size: clamp(44px, 7vw, 84px); line-height: .98; margin: 0 0 18px;
  letter-spacing: -.015em;
}
h1 em { font-style: normal; color: var(--accent); }
.lede { max-width: 62ch; color: var(--muted); font-size: 15px; }
.lede b { color: var(--ink); font-weight: 600; }
.chips { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; }
.chip {
  border: 1px solid var(--line); background: var(--panel); color: var(--muted);
  padding: 5px 12px; border-radius: 999px; font-size: 12px;
}
.chip b { color: var(--accent2); font-weight: 600; }

.toolbar {
  position: sticky; top: 0; z-index: 20; padding: 14px 0;
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: blur(8px); border-block: 1px solid var(--line);
  display: flex; gap: 12px; align-items: center; flex-wrap: wrap;
}
.toolbar input, .toolbar select {
  background: var(--panel); color: var(--ink); border: 1px solid var(--line);
  border-radius: 6px; padding: 8px 12px; font: inherit; font-size: 13px;
}
.toolbar input { min-width: 220px; }
.toolbar input:focus, .toolbar select:focus, .cell:focus-visible, a:focus-visible {
  outline: 2px solid var(--accent); outline-offset: 2px;
}
.legend { margin-left: auto; color: var(--faint); font-size: 12px; display: flex; gap: 14px; }
.legend i { font-style: normal; }
.count { color: var(--accent2); font-size: 12px; }

.gridwrap { overflow-x: auto; padding: 26px 0 60px; }
table.grid { border-collapse: separate; border-spacing: 0; width: 100%; min-width: 1080px; }
table.grid th, table.grid td { border-bottom: 1px solid var(--line); }
table.grid thead th {
  position: sticky; top: 57px; z-index: 5; background: var(--bg);
  font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase;
  color: var(--faint); font-weight: 500; padding: 10px 6px; text-align: center;
  white-space: nowrap;
}
table.grid thead th.hname { text-align: left; left: 0; z-index: 6; }
table.grid tbody th {
  position: sticky; left: 0; z-index: 4; background: var(--bg);
  text-align: left; padding: 0; font-weight: 500;
}
table.grid tbody th a {
  display: block; padding: 9px 14px 9px 2px; color: var(--ink);
  text-decoration: none; white-space: nowrap; font-size: 13.5px;
}
table.grid tbody th a:hover { color: var(--accent); }
table.grid tbody th .pin { display: block; color: var(--faint); font-size: 10.5px; padding: 0 14px 7px 2px; }
tr.row { animation: rise .5s ease-out both; }
@keyframes rise { from { opacity: 0; transform: translateY(8px); } }
td { text-align: center; padding: 0; }
.cell {
  width: 100%; height: 44px; border: 0; background: transparent; cursor: pointer;
  color: var(--unknown); font-size: 15px; line-height: 1;
  transition: background .15s ease-out, transform .15s ease-out;
}
.cell[data-s="yes"] { color: var(--yes); }
.cell[data-s="partial"] { color: var(--partial); }
.cell[data-s="no"] { color: var(--no); }
.cell:hover { background: var(--panel2); transform: scale(1.12); }
td.dim .cell { opacity: .22; }
td.hot { background: color-mix(in srgb, var(--accent) 8%, transparent); }

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
  font-size: 26px; margin: 0 0 4px;
}
.drawer .sub { color: var(--accent2); font-size: 12px; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 14px; }
.drawer .note { color: var(--muted); max-width: 88ch; }
.drawer .meta { margin-top: 14px; display: flex; gap: 18px; flex-wrap: wrap; font-size: 12.5px; }
.drawer .meta a { color: var(--accent); }
.drawer .meta .verdict { color: var(--ink); font-weight: 600; }
.drawer button.close {
  position: absolute; top: 14px; right: 20px; background: transparent;
  border: 1px solid var(--line); color: var(--muted); border-radius: 6px;
  padding: 4px 10px; cursor: pointer; font: inherit;
}
footer { border-top: 1px solid var(--line); padding: 34px 0 60px; color: var(--faint); font-size: 12.5px; }
footer a { color: var(--accent); }
footer p { max-width: 80ch; }
@media (prefers-reduced-motion: reduce) {
  tr.row { animation: none; }
  .drawer { transition: none; }
  .cell { transition: none; }
}
</style>
</head>
<body>
<header class="wrap">
  <p class="eyebrow">Orvii research set · evidence-contract atlas</p>
  <h1>What coding agents <em>promise</em> —<br>and what they <em>support</em>.</h1>
  <p class="lede">Twenty-five harnesses, fourteen capabilities, one snapshot date. <b>Click any cell</b>: it opens the note and the fetched-doc URL the verdict was read from. A cell you cannot trace does not exist here — it is marked <span aria-label="unknown">?</span>.</p>
  <div class="chips">
    <span class="chip">snapshot <b id="chip-date"></b></span>
    <span class="chip">release <b id="chip-ver"></b></span>
    <span class="chip"><b id="chip-n"></b> harnesses</span>
    <span class="chip">every cell cites a fetched doc</span>
  </div>
</header>

<div class="wrap toolbar" role="search">
  <input id="q" type="search" placeholder="filter harnesses…" aria-label="Filter harnesses by name">
  <select id="cap" aria-label="Highlight one capability column">
    <option value="">all capabilities</option>
  </select>
  <span class="count" id="count" aria-live="polite"></span>
  <span class="legend" aria-hidden="true">
    <i style="color:var(--yes)">● yes</i><i style="color:var(--partial)">◐ partial</i><i style="color:var(--no)">○ no</i><i> ? unknown</i>
  </span>
</div>

<main class="wrap gridwrap">
  <table class="grid" id="grid"></table>
</main>

<div class="drawer" id="drawer" role="dialog" aria-modal="false" aria-labelledby="d-title">
  <div class="wrap">
    <button class="close" id="d-close" aria-label="Close evidence drawer">esc ✕</button>
    <h2 id="d-title"></h2>
    <p class="sub" id="d-sub"></p>
    <p class="note" id="d-note"></p>
    <div class="meta" id="d-meta"></div>
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

document.getElementById("chip-date").textContent = DATA.as_of;
document.getElementById("chip-ver").textContent = DATA.version;
document.getElementById("chip-n").textContent = DATA.harnesses.length;
DATA.caps.forEach(c => {
  const o = document.createElement("option");
  o.value = c; o.textContent = DATA.cap_label[c];
  capSel.appendChild(o);
});

function render(rows) {
  const head = "<thead><tr><th class='hname'>harness · version pin</th>" +
    DATA.caps.map(c => `<th scope="col" data-cap="${c}">${DATA.cap_label[c]}</th>`).join("") + "</tr></thead>";
  const body = "<tbody>" + rows.map((h, i) =>
    `<tr class="row" style="animation-delay:${Math.min(i * 35, 500)}ms">` +
    `<th scope="row"><a href="https://github.com/Orvii/harness-atlas/blob/main/harnesses/${h.id}.md">${h.name}<span class="pin">${esc(h.version.split(" — ")[0].slice(0, 42))}</span></a></th>` +
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
capSel.addEventListener("change", applyCap);
document.getElementById("q").addEventListener("input", e => {
  const q = e.target.value.trim().toLowerCase();
  render(DATA.harnesses.filter(h => h.name.toLowerCase().includes(q)));
});

grid.addEventListener("click", e => {
  const b = e.target.closest(".cell");
  if (!b) return;
  const h = DATA.harnesses.find(x => x.id === b.dataset.h);
  const c = h.caps.find(x => x.cap === b.dataset.c);
  document.getElementById("d-title").textContent = h.name + " · " + DATA.cap_label[c.cap];
  document.getElementById("d-sub").textContent = SYM[c.support] + " " + WORD[c.support] + " · as of " + DATA.as_of;
  document.getElementById("d-note").textContent = c.note || "No note recorded for this cell — see the harness page.";
  const meta = document.getElementById("d-meta");
  meta.innerHTML =
    (c.evidence ? `<span>read from: <a href="${esc(c.evidence)}" rel="noopener noreferrer">${esc(c.evidence.replace(/^https?:\/\//, "").slice(0, 64))}</a></span>` : "<span>no evidence URL recorded — see page</span>") +
    `<span>pin: <span class="verdict">${esc(h.version.slice(0, 72))}</span></span>` +
    (h.docs ? `<span><a href="${esc(h.docs)}" rel="noopener noreferrer">docs home</a></span>` : "");
  drawer.classList.add("open");
  document.getElementById("d-close").focus();
});
document.getElementById("d-close").addEventListener("click", () => drawer.classList.remove("open"));
document.addEventListener("keydown", e => { if (e.key === "Escape") drawer.classList.remove("open"); });

render(DATA.harnesses);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(main())
