<picture>
  <source media="(prefers-color-scheme: dark)" srcset="hero.svg">
  <img alt="harness-atlas — capability matrix of AI coding harnesses, pinned and evidenced" src="hero.svg">
</picture>

# harness-atlas

[![release](https://img.shields.io/github/v/release/Orvii/harness-atlas?color=FE9106&label=release&style=flat-square)](https://github.com/Orvii/harness-atlas/releases)
[![snapshot](https://img.shields.io/badge/snapshot-2026--10--05-FEAF12?style=flat-square)](https://github.com/Orvii/harness-atlas/blob/main/matrix.yaml)
[![drift CI](https://img.shields.io/github/actions/workflow/status/Orvii/harness-atlas/drift.yml?style=flat-square&label=drift%20CI)](https://github.com/Orvii/harness-atlas/actions/workflows/drift.yml)
[![site](https://img.shields.io/badge/site-live-F05F03?style=flat-square)](https://orvii.github.io/harness-atlas/)

What AI coding harnesses **promise** — and what they **support** — with a version pin and a fetched-doc citation on every cell.

Twenty-five harnesses, fourteen capabilities, one snapshot date: **2026-10-05**.

| | |
|---|---|
| [matrix.md](matrix.md) | the capability grid, symbols linked to per-harness pages |
| [matrix.yaml](matrix.yaml) | same grid, machine-readable, with `as_of` |
| [harnesses/](harnesses/) | one page per harness: promises, capability table with evidence links, notable findings |
| [SYNTHESIS.md](SYNTHESIS.md) | what the grid actually says — interop, transitions, trust models |
| [METHODOLOGY.md](METHODOLOGY.md) | how cells are produced and how to re-run |
| [TRUST.md](TRUST.md) | the three trust layers (OS sandbox, prompts, model review) and who defaults to what |
| [GATES.md](GATES.md) | flags, tiers, OS limits, maturity labels and deprecations behind each ✅ |
| [VERIFYING.md](VERIFYING.md) | how to audit any cell in five minutes, and what a cell is not |

## Why this exists

Capability comparisons of coding agents age in weeks and are usually written from memory. This atlas inverts that: researchers fetch official docs during the run, verdicts carry the URL and a verbatim quote they were read from, and versions are pinned to the release tag observed that day. A cell you cannot trace is marked `unknown`, never guessed.

## Read this first

If you only read one file, read [SYNTHESIS.md](SYNTHESIS.md). Short version: the capability floor has moved (subagents/hooks/skills are table stakes), the ecosystem is interoperating across vendor lines, and half the field is mid-transition — Roo Code discontinued, Gemini CLI superseded, Goose rebranded with plan mode removed. Dates are not metadata here; they are the claim.

## Symbols

✅ documented yes · ◐ partial (read the note) · ✗ documented no · ? unknown/unverified

## How to read a cell

One column needs a caveat: `sandboxing` in this grid asks *does the harness bound the agent by any mechanism*, so permission prompts count. [TRUST.md](TRUST.md) separates the layers and is the stricter read — a harness can be `sandboxing ✅` here with no OS-level sandbox there. For a security decision, read TRUST.md, not this cell.

Take `sandboxing ◐` on some row. It means: on the cited date, the cited doc page documented sandboxing **with a stated limitation** — and the note in that row's capability table says which limitation (off by default, platform-restricted, experimental). `◐` is never a hedge: the note is the verdict's second half. A `?` means the researcher could not fetch a page that answers the question — absence of evidence, recorded as such, never guessed.

---

Orvii — Open, Research, Vision, Innovation & Ideas. Regenerate with `scripts/generate.py` against a fresh research journal; see METHODOLOGY.

Part of the Orvii research set: [convention-map](https://github.com/Orvii/convention-map) · [bench-notes](https://github.com/Orvii/bench-notes) · [equivalence-notes](https://github.com/Orvii/equivalence-notes) · [provider-reliability](https://github.com/Orvii/provider-reliability) · [context-file-evidence](https://github.com/Orvii/context-file-evidence) · [retractions](https://github.com/Orvii/retractions) · [svg-instruments](https://github.com/Orvii/svg-instruments).
