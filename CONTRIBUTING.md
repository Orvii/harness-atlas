# Adding or refreshing a harness

The atlas is generated, not hand-written. A harness page is the rendered form of one structured research result.

## The contract

One researcher (human or agent) produces, per harness:

- `repo`, `version`, `version_source` — the release tag or registry version **observed during the run**, with the URL it was read from.
- `features` — the 14 capability ids from `matrix.yaml`, each `yes|partial|no|unknown` plus `evidence_url` (a page fetched during the run) and, where possible, a verbatim `evidence_quote`.
- `promises` — 1-2 sentences in the project's own framing.
- Deep fields (optional but expected for full rows): `architecture`, `context_mgmt`, `ecosystem`, `governance`, `limitations`, `quotes`, `docs_map`.

Rules that keep the atlas honest:

1. **No memory answers.** Every verdict cites a URL fetched in the same run. Unfetchable → `unknown`.
2. **Dates travel with numbers.** `as_of` in `matrix.yaml` is part of every claim; a refresh re-pins versions.
3. **Partial is a verdict, not a hedge.** The note must say what is missing.
4. **Discontinued is data.** If a project is archived or superseded, say so in `limitations` and keep the row — see SYNTHESIS §3.

## Regenerating

The public journals live in [journals/](journals/) — one sanitized research
result per line, wave-ordered ([MANIFEST.md](journals/MANIFEST.md)). A new or
refreshed harness arrives as a single JSON object (the contract above) in
`journals-incoming/<slug>.json`; the merge script validates the evidence
contract before it enters the record:

```bash
python3 scripts/merge-incoming.py wf_<wave>      # incoming -> journals/<wave>.jsonl
python3 scripts/generate.py journals/wf_d9fe5bfc-a50.jsonl journals/wf_15cd0c06-541.jsonl \
        journals/wf_3decfb86-b1b.jsonl journals/wf_bf7ccd99-1e2.jsonl \
        journals/wf_7fea83f9-209.jsonl journals/wf_<wave>.jsonl
```

Journals merge by harness slug; later files win on scalar fields, deep fields merge in. `journals-incoming/` is scratch and gitignored: once a wave is merged, the journal under `journals/` is the only record. Wave order is load-bearing — append new waves to `journals/MANIFEST.md`, to the order list in `.github/workflows/regen-check.yml`, and to `release.yml`'s triggers. CI regenerates from journals/ on every data-path push and fails on any difference, so a page and its journal can never disagree. Then update `SYNTHESIS.md` by hand — it is prose over the notable findings, and generation cannot judge it.

## What we will not accept

- Cells sourced from a blog post when official docs exist.
- Version pins older than the run date without a stated reason.
- Prose that markets. The atlas describes; the harness markets elsewhere.
