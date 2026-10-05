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

```bash
python3 scripts/generate.py journal-v1.jsonl journal-v2.jsonl [...]
```

Journals merge by harness slug; later files win on scalar fields, deep fields merge in. Then update `SYNTHESIS.md` by hand — it is prose over the notable findings, and generation cannot judge it.

## What we will not accept

- Cells sourced from a blog post when official docs exist.
- Version pins older than the run date without a stated reason.
- Prose that markets. The atlas describes; the harness markets elsewhere.
