<picture>
  <source media="(prefers-color-scheme: dark)" srcset="hero.svg">
  <img alt="harness-atlas — capability matrix of AI coding harnesses, pinned and evidenced" src="hero.svg">
</picture>

# harness-atlas

[![release](https://img.shields.io/github/v/release/Orvii/harness-atlas?color=FE9106&label=release&style=flat-square)](https://github.com/Orvii/harness-atlas/releases)
[![snapshot](https://img.shields.io/badge/snapshot-2026--10--06-FEAF12?style=flat-square)](https://github.com/Orvii/harness-atlas/blob/main/matrix.yaml)
[![drift CI](https://img.shields.io/github/actions/workflow/status/Orvii/harness-atlas/drift.yml?style=flat-square&label=drift%20CI)](https://github.com/Orvii/harness-atlas/actions/workflows/drift.yml)
[![site](https://img.shields.io/badge/site-live-F05F03?style=flat-square)](https://orvii.github.io/harness-atlas/)

What AI coding harnesses **promise** — and what they **support** — with a version pin and a fetched-doc citation on every cell.

Thirty-seven harnesses, fourteen capabilities, one snapshot date: **2026-10-06**.

| | |
|---|---|
| [matrix.md](matrix.md) | the capability grid, symbols linked to per-harness pages |
| [matrix.yaml](matrix.yaml) | same grid, machine-readable, with `as_of` |
| [matrix.csv](matrix.csv) | same grid as CSV — verdict words, one row per harness, for spreadsheets |
| [harnesses/](harnesses/) | one page per harness: promises, capability table with evidence links, notable findings |
| [SYNTHESIS.md](SYNTHESIS.md) | what the grid actually says — interop, transitions, trust models |
| [METHODOLOGY.md](METHODOLOGY.md) | how cells are produced and how to re-run |
| [TRUST.md](TRUST.md) | the three trust layers (OS sandbox, prompts, model review) and who defaults to what |
| [GATES.md](GATES.md) | flags, tiers, OS limits, maturity labels and deprecations behind each ✅ |
| [VERIFYING.md](VERIFYING.md) | how to audit any cell in five minutes, and what a cell is not |
| [the site](https://orvii.github.io/harness-atlas/) | the grid, clickable: filter, compare up to four harnesses, open any cell's note and evidence URL, deep-link a cell (`#harness/capability`) |
| [journals/](journals/) | the sanitized research results every page was compiled from — regenerate the atlas with `python3 scripts/generate.py journals/*.jsonl` (wave order in MANIFEST.md); CI fails any drift |
| [feed.xml](https://orvii.github.io/harness-atlas/feed.xml) | Atom feed of data snapshots, generated from the changelog |

## Why this exists

Capability comparisons of coding agents age in weeks and are usually written from memory. This atlas inverts that: researchers fetch official docs during the run, verdicts carry the URL and a verbatim quote they were read from, and versions are pinned to the release tag observed that day. A cell you cannot trace is marked `unknown`, never guessed.

## Read this first

If you only read one file, read [SYNTHESIS.md](SYNTHESIS.md). Short version: the capability floor has moved (subagents/hooks/skills are table stakes), the ecosystem is interoperating across vendor lines, and half the field is mid-transition — Roo Code discontinued, Gemini CLI superseded, Goose rebranded with plan mode removed. Dates are not metadata here; they are the claim.

## Symbols

✅ documented yes · ◐ partial (read the note) · ✗ documented no · ? unknown/unverified

## How to read a cell

One column needs a caveat: `sandboxing` in this grid asks *does the harness bound the agent by any mechanism*, so permission prompts count. [TRUST.md](TRUST.md) separates the layers and is the stricter read — a harness can be `sandboxing ✅` here with no OS-level sandbox there. For a security decision, read TRUST.md, not this cell.

Take `sandboxing ◐` on some row. It means: on the cited date, the cited doc page documented sandboxing **with a stated limitation** — and the note in that row's capability table says which limitation (off by default, platform-restricted, experimental). `◐` is never a hedge: the note is the verdict's second half. A `?` means the researcher could not fetch a page that answers the question — absence of evidence, recorded as such, never guessed.

## Cite

Cite the release, not the date — cells move as vendors ship. Metadata lives in [CITATION.cff](CITATION.cff); for BibTeX:

```bibtex
@misc{orvii2026harnessatlas,
  title  = {harness-atlas: capability matrix of AI coding harnesses, pinned and evidenced},
  author = {{Orvii}},
  year   = {2026},
  howpublished = {\url{https://github.com/Orvii/harness-atlas}},
  note   = {Cite the release you queried: see CITATION.cff for the current version and snapshot date. Every cell cites the vendor doc it was read from.}
}
```

---

Orvii — Open, Research, Vision, Innovation & Ideas. Regenerate with `scripts/generate.py` against the public journals; see METHODOLOGY and [journals/MANIFEST.md](journals/MANIFEST.md).

Part of the Orvii research set: [convention-map](https://github.com/Orvii/convention-map) · [equivalence-notes](https://github.com/Orvii/equivalence-notes) · [provider-reliability](https://github.com/Orvii/provider-reliability) · [context-file-evidence](https://github.com/Orvii/context-file-evidence) · [retractions](https://github.com/Orvii/retractions) · [svg-instruments](https://github.com/Orvii/svg-instruments) · [bench-notes](https://github.com/Orvii/bench-notes) · [ts-lto-research](https://github.com/Orvii/ts-lto-research).
