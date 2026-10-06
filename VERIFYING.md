# Verifying a cell — a five-minute audit

The atlas makes one promise: **every cell is checkable by a stranger in five minutes, with no access to our research notes.** This page is the procedure. If you follow it and a cell fails, that is a bug — file it with the [stale-cell template](.github/ISSUE_TEMPLATE/stale-cell.yml).

## The procedure

1. **Pick a cell.** Say `Cursor · sandboxing`. Open [harnesses/cursor.md](harnesses/cursor.md) and find the row.
2. **Read the evidence URL.** The last column links the exact doc page the verdict was read from. Open it. (If the page has moved, the monthly link-rot CI may already have flagged it; a dead link is not by itself a wrong verdict.)
3. **Find the quoted sentence.** The note column paraphrases; the research journal behind the page carries the verbatim quote. The verdict must follow from the quote — `yes` needs the doc to describe the capability, `no` needs the doc to state its absence or an equivalent, `partial` needs the note to name the limitation the doc states.
4. **Check the pin.** The row's header carries the version pin and *where it came from*: a release tag for open repos, an npm dist-tag or vendor changelog page for closed-source products. Compare against the source it names. A pin older than the vendor's latest release is **drift, not error** — the atlas snapshots; [reports/drift-log.md](reports/drift-log.md) is where drift accumulates between research runs.
5. **Check the symbol semantics.** `✅` = the doc describes it; `◐` = describes it *with a stated limitation* (the note is the second half of the verdict); `✗` = the doc documents the absence; `?` = no fetched page answers the question. A `✅` where the doc only implies is a bug; a `?` where we guessed would be a bigger one.

## What a cell is NOT

- **Not "works well".** The grid records documentation, not quality. A `✅` on `sandboxing` says the doc describes a sandbox; whether it holds is [TRUST.md](TRUST.md)'s layer analysis plus your own judgment.
- **Not version-free.** Every cell is true *as of the snapshot date and the pinned version*. Vendors ship weekly; the snapshot does not move between research runs by design.
- **Not the whole doc.** Notes compress. The quote is the contract; the note is a summary of it.

## Verifying the verification

The sanitized research journals are published in [journals/](journals/) — one JSON result per line, working-prose framing stripped at export. The contract is mechanical and re-runnable by anyone:

```bash
python3 scripts/generate.py journals/*.jsonl   # rebuilds every page, byte-identical
scripts/drift-check.sh                        # pins vs current releases, read-only
scripts/link-rot.sh                           # dead vs blocked evidence URLs
```

The wave order matters (later waves win on conflicts) and is **not** the alphabetical order a shell glob produces — so the generator sorts the files itself by the order [journals/MANIFEST.md](journals/MANIFEST.md) declares, and the glob form above is safe. CI runs the same regeneration on every data-path push and fails the build if any page differs from what the journals compile to — a hand-edited cell cannot land.

Links on a harness page fall into three classes, and `link-rot.sh` treats each differently:

- **Claim-bearing** — the evidence URL in a capability row, the parenthetical citations inside the prose sections, and the journal's quotes. A 404 here means the verdict can no longer be traced. The checker requests every one (markdown-linked and bare alike) and exits non-zero — failing the monthly CI run — if any is dead. Repairing one is a data commit: re-point the journal entry to the live canonical page, and update the verbatim quote too when the vendor rewrote the sentence off the old page.
- **Cited-as-dead** — a URL the note quotes *precisely because* it 404s: "the architecture page … returned HTTP 404" (Aider), "docs frozen — `continue.dev/docs/intro` returns 404" (Continue), "the legacy slug returns 404" (Sourcegraph Amp). Here the dead link **is** the evidence; the checker recognizes the 404 predication in the clause immediately after the URL, skips the request, and reports the citation separately. Killing it would destroy a documented deprecation — the atlas's most honest cells. (The predication must be local: one Amp sentence cites the dead legacy slug *and* the live replacement in the same breath, so sentence-wide or window-wide heuristics misclassify the live one.)
- **Provenance** — the "Sources fetched" navigation log at the foot of the page, which legitimately includes paths that were already 404 when probed (a `managing-context` guess beside the real `manage-context.md`, an old slug beside its replacement). Dead provenance links are recorded, not failed.

Only claim-bearing URLs are the contract; the gate is red on those and quiet on the other two classes by design. The two checkers above run monthly and commit their reports; a green drift run means *no pin moved since the last run*, not *no pin is stale* — the distinction is the whole point of publishing the log.

## Reporting

- Wrong verdict, wrong quote, wrong pin source → [stale-cell issue](.github/ISSUE_TEMPLATE/stale-cell.yml). Include the doc URL and the verbatim sentence; that is what lets us fix the cell without re-running the research.
- Missing harness → [new-harness issue](.github/ISSUE_TEMPLATE/new-harness.yml).
- A disagreement about *interpretation* (is this a `partial` or a `yes`?) is worth an issue too — the note column is where interpretation lives, and it should argue with itself in the open.
