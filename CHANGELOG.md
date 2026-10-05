# Changelog

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
