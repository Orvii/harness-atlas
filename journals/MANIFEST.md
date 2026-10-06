# Journals — the public source of every page

Sanitized researcher results, one JSON object per line. Regenerate the
whole atlas from these files alone:

    python3 scripts/generate.py journals/*.jsonl

Merge order below is the order the waves ran; later files win on
conflicts (see `scripts/generate.py`). Working-prose framing was
stripped at export and the generator re-sanitizes at load, so what you
see here is exactly what the pages were compiled from.

| file | harness results | wave |
|---|---|---|
| [wf_d9fe5bfc-a50.jsonl](wf_d9fe5bfc-a50.jsonl) | 10 | wave 1 — first ten harnesses with deep sections |
| [wf_15cd0c06-541.jsonl](wf_15cd0c06-541.jsonl) | 14 | wave 2 — expansion to seventeen |
| [wf_3decfb86-b1b.jsonl](wf_3decfb86-b1b.jsonl) | 3 | wave 3 — Crush, Amazon Q Developer CLI, Vibe |
| [wf_bf7ccd99-1e2.jsonl](wf_bf7ccd99-1e2.jsonl) | 3 | wave 4 — Sourcegraph Amp, Factory Droid, JetBrains Junie |
| [wf_7fea83f9-209.jsonl](wf_7fea83f9-209.jsonl) | 5 | wave 5 — Cursor, Windsurf, Google Jules, Amazon Kiro, Devin |
| [wf_v34-incoming.jsonl](wf_v34-incoming.jsonl) | 5 | wave 6 — Augment Code, Tabnine, Replit Agent, Qodo, Bolt (independent researchers, merged via merge-incoming.py) |
| [wf_v35-incoming.jsonl](wf_v35-incoming.jsonl) | 7 | wave 7 — Warp, Trae, Google Antigravity, Qoder, Lovable, v0, Void (independent researchers, merged via merge-incoming.py; Trae read via scripts/fetch-trae-docs.py because its docs are a JS-only SPA) |
