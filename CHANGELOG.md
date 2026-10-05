# Changelog

## [2026-10-05] - v3.1: gates, coverage honesty, reading guides

### Added
- `GATES.md` — the layer behind documented: env/flag gates, tier gates, OS gates, maturity labels, deprecation gates
- README "How to read a cell" — partial is a verdict with a note; unknown is absence of evidence

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

