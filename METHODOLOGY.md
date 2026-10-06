# Methodology

`as_of` in matrix.yaml is the date of the most recent research wave; cells from earlier waves were fetched on the dates recorded in their journals (see journals/MANIFEST.md). Per-row version pins carry what was observed, when.

How every cell in this atlas is produced, so you can trust it — or re-run it.

## Pipeline

1. **One researcher per harness.** Each fetches the harness's official docs (docs site first; repo `docs/` via raw URLs as fallback) and the latest release tag via the GitHub API during the run. Nothing is answered from memory.
2. **Fourteen fixed capability questions.** Same wording for every harness (see `matrix.yaml` keys), so rows are comparable. Verdicts are `yes / partial / no / unknown`.
3. **Evidence per cell.** Every verdict carries the URL it was read from plus a short verbatim quote on the harness page. A cell without a source is `unknown`, never a guess.
4. **Version pin per harness.** Latest release tag (or registry version when the project publishes there), with the URL the pin was read from and the run date.
5. **Mechanical assembly.** `scripts/generate.py` turns the research journal into `harnesses/*.md`, `matrix.md` and `matrix.yaml`. Prose (`SYNTHESIS.md`) is written by a human-equivalent pass over the researchers' notable-findings, never generated blind.

## Re-running

The research step is a workflow of ten parallel researchers; its journal (one JSON result per harness) is the input:

```bash
python3 scripts/generate.py <journal.jsonl>
```

Re-run cadence: quarterly, or whenever a harness ships a breaking rebrand — see SYNTHESIS §3 for why dates matter more here than in most datasets.

## Known limits

- Docs describe intent; we do not execute the harnesses. A capability marked `yes` means "documented and evidenced", not "benchmarked by us".
- `partial` hides variety: read the note on the harness page before relying on a ◐.
- Ecosystems move faster than any snapshot. Treat `as_of` in `matrix.yaml` as part of every claim.
