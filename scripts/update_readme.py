#!/usr/bin/env python3
"""Merge build results into status.json and regenerate the image table in README.md.

usage: update_readme.py <namespace> [results_dir]
Every <results_dir>/*.json is {"repo","tag","status","date","sha","run_url"}.
"""
import glob, json, os, sys

START, END = "<!-- IMAGES:START -->", "<!-- IMAGES:END -->"
ICON = {"success": "✅ success", "failure": "❌ failure", "cancelled": "⚠️ cancelled"}

ns = sys.argv[1]
results = sys.argv[2] if len(sys.argv) > 2 else None

status = json.load(open("status.json")) if os.path.exists("status.json") else {}
if results:
    for f in sorted(glob.glob(os.path.join(results, "*.json"))):
        r = json.load(open(f))
        status[f"{r['repo']}:{r['tag']}"] = r

images = sorted(
    tuple(p.split("/")[:2])
    for p in glob.glob("*/*/Containerfile")
    if not p.startswith((".", "scripts"))
)
# drop status of images that no longer exist
status = {k: v for k, v in status.items() if tuple(k.split(":", 1)) in images}
json.dump(status, open("status.json", "w"), indent=2, sort_keys=True)
open("status.json", "a").write("\n")

rows = ["| Image | Tag | Docker Hub | Last build (UTC) | Status | Commit |", "|---|---|---|---|---|---|"]
for repo, tag in images:
    s = status.get(f"{repo}:{tag}")
    link = f"[{ns}/{repo}:{tag}](https://hub.docker.com/r/{ns}/{repo}/tags?name={tag})"
    if s:
        st = f"[{ICON.get(s['status'], s['status'])}]({s['run_url']})"
        rows.append(f"| `{repo}` | `{tag}` | {link} | {s['date']} | {st} | `{s['sha'][:7]}` |")
    else:
        rows.append(f"| `{repo}` | `{tag}` | {link} | – | ⏳ never built | – |")

readme = open("README.md").read()
head, rest = readme.split(START, 1)
tail = rest.split(END, 1)[1]
open("README.md", "w").write(f"{head}{START}\n" + "\n".join(rows) + f"\n{END}{tail}")
