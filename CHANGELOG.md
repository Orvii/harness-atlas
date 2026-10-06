# Changelog

## [2026-10-06] - v3.4: thirty harnesses — the capability-vendor cluster

### Added
- Five rows: **Augment Code** (Auggie CLI + Cosmos: subagents, trigger automations, Expert memory, Git-marketplace plugins), **Tabnine** (broad CLI agent surface on a CLI the vendor calls maintenance-mode, deprecation after 2026-12-31), **Replit Agent** (cloud task system with plan-gated parallelism, no published version), **Qodo** (Agentic Toolbox: review agents and standards that plug into other agents — a capability layer with no execution layer), **Bolt** (web-native agent; plan review without a documented hard gate).
- `SYNTHESIS.md` §10 — the stack is splitting: capability vendors that execute nothing; web-native rows where the environment is the product; deprecation as a row property; unknowns concentrating in hosted vendors.
- `GATES.md` eighth kind — the gate that opens under automation: Tabnine's headless YOLO switch, Bolt's plan-after-first-build, Replit's billable review, Augment's CLI-only enforcement.
- `TRUST.md` — five rows; Qodo recorded as n/a on the sandbox axis (it executes nothing); new bullet on review-layer vendors riding host agents' trust models.
- `journals/wf_v34-incoming.jsonl` — wave 6, five independent researchers, merged via the new `scripts/merge-incoming.py` (contract-validated on entry).
- `matrix.csv` in the generated set; `scripts/merge-incoming.py`.

### Modified
- Counts to 30 everywhere (README, SYNTHESIS, TRUST, hero.svg, CITATION v3.4); `as_of` 2026-10-06; METHODOLOGY clarifies that as_of is the latest wave's date while journals carry per-wave fetch dates.
- Site: cell history now records verdict movement only (row additions are the changelog's job); lede count dynamic.

## [2026-10-06] - enforced reproducibility: public journals + regeneration gate

### Added
- `journals/` — sanitized researcher results (one JSON line each; head + enrichment lines, wave-ordered; MANIFEST.md records merge order). `python3 scripts/generate.py journals/*.jsonl` in wave order reproduces every committed page byte-identically.
- `scripts/export-journals.py` — exports sanitized results from workflow journals in the generator's line shape.
- `.github/workflows/regen-check.yml` — regenerates pages from journals/ on data-path pushes and fails if any page or the harness set differs.

### Modified
- `scripts/generate.py` — enrichment-only results may enrich an existing row but never start one; `as_of` carried forward from the committed matrix.yaml so regeneration is byte-stable.
- `VERIFYING.md`, method page — point at the public journals and the enforced regeneration.

## [2026-10-06] - site redesign: specimen-plate layout, plate-mode grid, deep links

### Modified
- `scripts/build_site.py` — index.html rebuilt around a broadsheet masthead: two-column head with a framed "reading the plate" specimen (symbol key, live cell sample, snapshot ledger) replacing the chip row; legend moved out of the toolbar; toolbar gains verdict filter (rows containing ●/◐/○/?) and row sort (name a–z, most documented, most contested); compare view gains a disagreement-count summary line; grid gains a per-column census bar (yes/partial/no/unknown proportions + documented count) as a second sticky head row and two-digit row indices; every cell is deep-linkable (`#<harness>/<capability>`) with a copy-link button in the drawer; `<noscript>` fallback points at matrix.md.
- `scripts/build_site.py` — sticky-head fix: the grid is now its own scroll plate on desktop (`max-height` + `overflow: auto`), so the head pins to the plate top; on ≤980px the head goes static and the name column stays pinned. Root cause: an `overflow-x` scroll container becomes the sticky reference, which previously floated the head mid-grid on small screens.
- `scripts/build_site.py` — shared CSS keeps `.chips`/`.chip` for method.html; entry animation shortened to 350ms.

## [2026-10-05] - v3.3: twenty-five harnesses — the cloud-autonomous cluster

### Added
- `harnesses/cursor.md`, `windsurf.md`, `google-jules.md`, `amazon-kiro.md`, `devin.md` — five closed-source agents incl. the first three whose loop runs server-side (Jules, Devin, Kiro cloud sessions). Version pins from npm dist-tags, vendor changelogs and API self-labels; each row says which.
- `SYNTHESIS.md` §9 "Execution locality is now a first-class axis" — the human gate relocates when the loop leaves the machine (Jules: plan approval instead of prompts; Windsurf/Devin: fail-closed sandbox); where the human left, a model was hired (Cursor Auto-review default, Jules' critic agent); `background_tasks` was conflating async with remote.
- `SYNTHESIS.md` §6 retitled: the compatibility chain no longer has one direction — v3.3 rows cross-read Claude/Codex/Cursor directories.
- `TRUST.md` five rows; prompts-floor now has two exceptions (Amp by choice, Jules by structure); cloud rows are VM-isolated by construction while local sandboxes stay opt-in.
- `GATES.md` seventh gate kind (locality) plus the new env/tier/OS/maturity/deprecation entries.

### Modified
- Counts to twenty-five across README, hero.svg, SYNTHESIS, TRUST, CITATION (v3.3).

## [2026-10-05] - v3.2: twenty harnesses — the closed-source cluster

### Added
- `harnesses/sourcegraph-amp.md`, `harnesses/factory-droid.md`, `harnesses/jetbrains-junie.md` — three closed-source commercial agents, researched from vendor docs with the same evidence contract (per-cell URL + verbatim quote). Version pins come from npm `dist-tag latest`, the vendor changelog page, and the vendor what's-new page respectively, since no release tags exist; each row says which.
- `SYNTHESIS.md` §8 "The closed-source cluster answers differently" — what changes when a pin is not a git tag, when deprecation is a policy rather than a commit, and when a trust claim is a vendor security page.
- `GATES.md` "A sixth kind: the closed-source gate" plus the new harnesses' env/tier/OS/maturity/deprecation gates in the existing five lists.
- `TRUST.md` rows for all three, including **Sourcegraph Amp as the first harness in the set that documents no local permission prompt at all** ("By default, Amp does not ask for approval before running tools") — the universal-prompt floor now has one hole.
- `bench-notes`: `the-benchmark-code-is-the-result` (note 14). `equivalence-notes`: `environment-is-part-of-the-program` (note 11).

### Modified
- Counts to twenty across `README.md`, `hero.svg`, `SYNTHESIS.md`, `TRUST.md`, `CITATION.cff`.
- `TRUST.md` analysis bullets rewritten against the enlarged table: prompts 19/20, no-OS-sandbox 8/20, partial 4/20.
- `README.md` "How to read a cell" and `TRUST.md` intro now state the `sandboxing` definitional gap explicitly — the matrix cell counts permission gating, TRUST separates the layers, and where they disagree TRUST is the one to use for a security decision (OpenCode and Cline are the concrete cases).
- Stripped internal-process phrasing ("task-provided", "the task's") from `harnesses/sourcegraph-amp.md`, `harnesses/continue.md`, `harnesses/vibe.md` — the dead-URL findings stay, described as legacy/canonical paths instead.

## [2026-10-05] - v3.1: gates, coverage honesty, reading guides

### Added
- `GATES.md` — the layer behind documented: env/flag gates, tier gates, OS gates, maturity labels, deprecation gates
- README "How to read a cell" — partial is a verdict with a note; unknown is absence of evidence

## [2026-10-05] - v3: 17 harnesses, deep sections, trust + precedence + citation

### Added
- `harnesses/` pages for crush, amazon-q-developer-cli, vibe (batch 3, full capability + deep pass)
- Deep-dive sections on all pages: architecture, context management, ecosystem, governance, limitations, quotes, sources (research runs wf_15cd0c06, wf_3decfb86)
- `TRUST.md` — three-layer trust model (OS sandbox / prompts / model review), default postures per harness
- `scripts/drift-check.sh` — mechanical version-pin freshness report; multi-stream release tags handled (Qwen CLI vs sdk), nightlies excluded
- `scripts/link-rot.sh` — evidence-URL rot checker; dead (404/410) vs bot-gated (403/429) separated; first run: 235 URLs, 232 ok, 0 dead
- `.github/workflows/drift.yml` — monthly drift + link-rot reports committed back by CI
- `CITATION.cff` — cite the snapshot date, not the repo
- `CONTRIBUTING.md` — evidence contract for adding or refreshing a harness

### Modified
- `SYNTHESIS.md` — v3: compatibility chain widens (Vibe, Crush), Amazon Q as capability-shipped-to-no-audience, governance as differentiator
- `scripts/generate.py` — v2: multi-journal merge by harness slug, deep-section rendering
- README counts 10 → 14 → 17; hero updated to match

## [2026-10-05] - v1: 10 harnesses x 14 capabilities

### Added
- Research run wf_d9fe5bfc: one researcher per harness, official docs only, per-cell evidence URL + verbatim quote, release-tag version pins
- `matrix.md`, `matrix.yaml`, `harnesses/*.md`, `SYNTHESIS.md`, `METHODOLOGY.md`, `hero.svg`

