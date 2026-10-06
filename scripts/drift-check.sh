#!/usr/bin/env bash
# Report version-pin drift: compare matrix.yaml pins against current latest
# GitHub release tags. Mechanical only — no docs re-read, no verdicts.
# Usage: scripts/drift-check.sh   (needs gh + a python interpreter; read-only)
set -euo pipefail
cd "$(dirname "$0")/.."

# Resolve an interpreter once. `python3` is tried first so Linux and CI keep
# the documented command; on Windows `python3` is frequently a Microsoft
# Store alias that MATCHES `command -v` but exits non-zero, so probe each
# candidate by running it rather than trusting its presence.
PY=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "" >/dev/null 2>&1; then
    PY="$cand"
    break
  fi
done
if [ -z "$PY" ]; then
  echo "drift-check: neither 'python3' nor 'python' ran; install Python 3.9+." >&2
  exit 127
fi

"$PY" - <<'PY'
import re, subprocess, sys

# Windows consoles and redirects default to cp1252, where this report's
# markers (—  Δ  –) fail to encode and print() raises: the script dies before
# it can print a line, which is the same failure as not looking. Force UTF-8
# with a replacement fallback so a marker can never abort the run; on CI
# (already UTF-8) this changes nothing.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def run_gh(args):
    """(returncode, stripped stdout) for a gh invocation; (1, "") on any
    failure to launch, so callers see a non-zero code rather than an exception."""
    try:
        p = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=30)
    except Exception:
        return 1, ""
    return p.returncode, p.stdout.strip()


# Fail loudly without API auth. Every `gh api` call below needs a token; when
# one is missing the API answers unauthenticated, each repo reports "no
# release found", and the script prints "0 drifted" — a clean-looking report
# produced by not looking. That is exactly what the first CI run of this
# script did (the workflow never exported GITHUB_TOKEN). A report that cannot
# fail is worse than no report.
rc, probe = run_gh(["api", "repos/cli/cli/releases/latest", "--jq", ".tag_name"])
if rc != 0 or not probe:
    sys.exit(
        "drift-check: GitHub API is not authenticated — set GH_TOKEN "
        "(CI: `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}`). Refusing to print a "
        "report that would read as 'no drift'."
    )

repos = {}
cur = None
for raw in open("matrix.yaml", encoding="utf-8"):
    m = re.match(r"\s+repo: \"(.+)\"", raw)
    if m:
        cur = m.group(1)
    m = re.match(r"\s+version: \"(.+)\"", raw)
    if m and cur:
        repos[cur] = m.group(1)
        cur = None

CLOSED = re.compile(r"closed[- ]source|not public|no public", re.I)
STABLE = re.compile(r"nightly|-(pre|rc|beta|alpha)\b", re.I)
# The pin's version token, at the very start of the pin and preceded only by a
# bare identifier prefix (`rust-`, `desktop-`, or a lone `v`). A number that
# sits after descriptive words — "Kiro CLI 2.27.0", "Qodo 3.0" — is a vendor
# label, not a release tag, and must not be extracted.
PIN = re.compile(r"^(?:[A-Za-z][A-Za-z0-9]*-)?(v?\d+(?:\.\d+){2,4}(?:-[0-9A-Za-z][0-9A-Za-z.-]*)?)")
# Fallback for a pin that opens with words but DID name its GitHub stream, as
# the task's example does: "GitHub v0.86.0 (2025-08-09), PyPI 0.86.2" -> the
# tag right after the word "GitHub". Anchored to "GitHub" on purpose so a
# vendor label ("Kiro CLI 2.27.0") still yields no tag.
GITHUB_TAG = re.compile(r"github\s+(v?\d+(?:\.\d+){2,4}(?:-[0-9A-Za-z][0-9A-Za-z.-]*)?)", re.I)
# The leading segment of a release tag: everything before the version begins.
# `v0.62.0` -> "v", `rust-v0.160.0` -> "rust-", `desktop-v0.0.43` -> "desktop-",
# `sdk-typescript-v0.1.18` -> "sdk-typescript-".
SEGMENT = re.compile(r"^(.*?)(?=[vV]?\d+(?:\.\d+)+)")


def split_tag(tag):
    """(leading segment, version token) for a release tag, or None when the tag
    carries no semver-ish number at all."""
    seg = SEGMENT.match(tag).group(1) if SEGMENT.match(tag) else ""
    mv = re.match(r"v?\d+(?:\.\d+){2,4}(?:-[0-9A-Za-z][0-9A-Za-z.-]*)?", tag[len(seg):])
    if not mv:
        return None
    return seg, mv.group(0)


class NotDiffable(Exception):
    """Raised when a pin cannot be honestly turned into a GitHub release tag.
    The row is skipped with its own line; it is never compared against some
    other stream's tag, which is what the old prefix fallback did."""


def resolve_version(pin):
    """The GitHub release tag a pin names, or raise NotDiffable.

    A pin that opens with the tag is that tag: "v0.86.0", "rust-v0.160.0",
    "v0.86.0 (latest GitHub release; PyPI aider-chat latest is 0.86.2)". A
    pin that opens with a vendor label ("Qodo 3.0", "Cursor 3.x") does NOT
    name a tag — the label must never be mistaken for one. Such a pin is
    diffable only when it says GitHub and gives the tag right after the word,
    e.g. "GitHub v0.86.0 (2025-08-09), PyPI 0.86.2"."""
    m = PIN.match(pin)
    if m and not any(ch.isdigit() for ch in pin[: m.start(1)]):
        # Keep the whole matched tag, identifier prefix included:
        # `rust-v0.160.0` must not be flattened to `v0.160.0`.
        return m.group(0)
    g = GITHUB_TAG.search(pin)
    if g:
        return g.group(1)
    raise NotDiffable


def latest_in_stream(path, core):
    """Newest stable tag whose leading segment equals `core`, or ''."""
    _rc, listing = run_gh(["api", f"repos/{path}/releases", "--jq", ".[].tag_name"])
    for t in listing.split():
        if STABLE.search(t):
            continue
        st = split_tag(t)
        if st and st[0] == core:
            return st[1]
    return ""


drift = 0
closed = 0
skipped = 0
for repo, pin in sorted(repos.items()):
    path = repo.split(" (")[0].strip()
    path = re.sub(r"^https://github\.com/", "", path).rstrip("/")
    # Closed-source products have no public repo to diff against: their pin
    # comes from an npm dist-tag or a vendor changelog page. Report as
    # uncheckable here rather than as a missing release, which would read like
    # a rename.
    if CLOSED.search(repo):
        closed += 1
        print(f"—  {path or repo.split(' (')[0]}: pin {pin} — closed source, docs/registry-pinned (not diffable)")
        continue
    if "/" not in path:
        # No owner/repo slug to query. Say so rather than dropping the row:
        # every row must leave a line behind, or the report lies by omission.
        skipped += 1
        print(f"–  {path or repo}: pin {pin} — repo value has no owner/repo slug (not diffable here)")
        continue
    try:
        pin_version = resolve_version(pin)
    except NotDiffable:
        skipped += 1
        print(f"–  {path}: pin {pin} — names no GitHub release stream (not diffable here)")
        continue
    rc, latest = run_gh(["api", f"repos/{path}/releases/latest", "--jq", ".tag_name"])
    if rc != 0 or not latest or latest.startswith("{"):
        skipped += 1
        print(f"?  {path}: pin {pin} — no release found (registry-pinned or renamed)")
        continue
    # Repos with multiple release streams (CLI + SDK tags) publish `latest` on
    # whichever stream moved last. Trust it only when its leading segment is
    # the pin's; otherwise fall back to the newest stable tag in the pin's own
    # stream, and if that stream is absent from recent releases, skip the row
    # rather than invent a comparison.
    pin_core, pin_num = split_tag(pin_version)
    latest_tag = split_tag(latest)
    if latest_tag and latest_tag[0] == pin_core:
        out_tag = latest
    else:
        out_tag = latest_in_stream(path, pin_core)
        if not out_tag:
            skipped += 1
            seen = latest_tag[0] if latest_tag else "non-semver"
            print(f"?  {path}: pin {pin} — latest release {latest} is a different "
                  f"stream ({seen}); pin's stream not in recent releases (not diffable here)")
            continue
    # Compare the tag, but tolerate a bare pin: `0.36.0` and `v0.36.0` are the
    # same release written two ways, and calling that drift would be noise.
    digit = re.compile(r"[vV]")
    same = digit.sub("", out_tag) == digit.sub("", pin_version)
    if not same:
        drift += 1
        print(f"Δ  {path}: pinned {pin_version} → latest {out_tag}")
    else:
        # Print the PIN's own spelling, not a normalized one, so the line can
        # be grepped straight back into matrix.yaml.
        print(f"=  {path}: {pin_version}")
print(f"\n{drift} drifted pin(s), {closed} closed-source pin(s) not diffable, "
      f"{skipped} pin(s) skipped (no comparable stream). "
      f"Refresh = new research run + generate.py; see CONTRIBUTING.")
PY