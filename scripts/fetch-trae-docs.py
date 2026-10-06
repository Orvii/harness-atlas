#!/usr/bin/env python3
"""Fetch docs.trae.ai pages as plain text.

Trae's documentation is a client-side SPA (ByteDance's arcosites platform).
There is no llms.txt, no sitemap.xml, no `.md` suffix and no public JSON
content API — all four return the same 287 KB app shell, and following their
redirects lands on the app's default route. A researcher fetching these URLs
normally gets an empty page, which is why the Trae row needs this script.

The content IS on the server, though: every page's SSR payload embeds its own
document under

    window._ROUTER_DATA.loaderData.$["docDetail"].content

as a component tree whose `local.component.Text` nodes carry Quill-Delta rich
text (`{"t": {"0": {"ops": [{"insert": "..."}]}}}`). This script walks that
tree and flattens the deltas to plain text. The site's own doc index is in the
same payload under `loaderData.layout.busStructure`, so `--index` enumerates
every page without a crawl.

Usage:
    python3 scripts/fetch-trae-docs.py --index            # list EN doc pages
    python3 scripts/fetch-trae-docs.py <path> [path...]   # print pages as text

<path> is the URL segment, e.g. `subagents` for docs.trae.ai/ide/subagents.
Router is /ide unless the path is prefixed, e.g. `plugin/install-trae-plugin`.
"""
import json
import re
import subprocess
import sys

UA = "Mozilla/5.0 (X11; Linux x86_64) Chrome/120"
BASE = "https://docs.trae.ai"


def fetch(url):
    r = subprocess.run(
        ["curl", "-s", "-L", "--compressed", "--max-time", "40", "-A", UA, url],
        capture_output=True, timeout=60)
    return r.stdout.decode("utf-8", "replace")


def router_data(html):
    m = re.search(r"window\._ROUTER_DATA = (\{.*?\});?\s*</script>", html, re.S)
    if not m:
        raise SystemExit(f"no _ROUTER_DATA in {len(html)} bytes — is the URL a doc page?")
    return json.loads(m.group(1))["loaderData"]


def delta_text(value):
    """Flatten Quill-Delta ops to plain text.

    Only `ops[].insert` strings are content. Walking arbitrary string values
    instead appends every paragraph twice (the delta stores both a zoned and a
    flat copy), which is what the first version of this script did.
    """
    out = []

    def walk(n):
        if isinstance(n, dict):
            if isinstance(n.get("ops"), list):
                for op in n["ops"]:
                    if isinstance(op, dict) and isinstance(op.get("insert"), str):
                        out.append(op["insert"])
                return                      # ops consumed; do not descend again
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(value)
    return re.sub(r"\n{3,}", "\n\n", "".join(out)).strip()


def page_text(doc_detail):
    parts = []

    def walk(n):
        if isinstance(n, dict):
            if (n.get("componentType") or "") == "local.component.Text":
                v = (n.get("props") or {}).get("value")
                if v:
                    parts.append(delta_text(v))
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(doc_detail.get("content"))
    return "\n\n".join(p for p in parts if p)


def index(html, lang="en"):
    """Every doc node in the site's busStructure: (path, title, lang, is_dir)."""
    out = []

    def walk(n):
        if isinstance(n, dict):
            if "_id" in n and ("title" in n or "path" in n):
                out.append({k: n.get(k) for k in ("path", "title", "lang", "is_dir")})
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    data = router_data(html)
    walk(data["layout"].get("busStructure") or data["$"].get("busStructure") or [])
    seen, uniq = set(), []
    for x in out:
        if x.get("lang") != lang or x.get("is_dir"):
            continue
        if x.get("path") and x["path"] not in seen:
            seen.add(x["path"])
            uniq.append(x)
    return uniq


def main(argv):
    if not argv or argv[0] == "--index":
        html = fetch(f"{BASE}/ide/what-is-trae?_lang=en")
        for n in index(html):
            print(f"{n['path']:52} {n.get('title','')}")
        return 0
    for p in argv:
        router, _, rest = p.partition("/") if p.startswith("plugin/") else ("ide", "", p)
        url = f"{BASE}/{router}/{rest}?_lang=en"
        d = router_data(fetch(url))["$"]["docDetail"]
        print(f"# {d.get('title')}")
        print(f"# source: {BASE}/{router}/{rest}")
        print(f"# updated: {d.get('updated_at')}")
        print()
        print(page_text(d))
        print("\n" + "=" * 72 + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
