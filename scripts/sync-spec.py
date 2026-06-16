#!/usr/bin/env python3
"""Generate docs/spec.md from the canonical ARD spec.

Single source of truth: ards-project/ard-spec : spec/ard.md
This script copies that file into docs/spec.md and rewrites the repo-relative
links (which only resolve inside the ard-spec repo) to absolute GitHub URLs so
they work on the published docs site. Run it in CI before `mkdocs build`, or
locally against a checkout of ard-spec. Do not hand-edit docs/spec.md.

Usage:
  python scripts/sync-spec.py [SOURCE]
SOURCE may be a local path or an https:// URL (e.g. the raw GitHub file). It
defaults to $ARD_SPEC_SRC, else ../ard-spec/spec/ard.md.
"""
import os
import posixpath
import re
import sys
import urllib.error
import urllib.request

REPO = "ards-project/ard-spec"
BRANCH = "main"
# Directory of the source file within the repo — relative links resolve here.
SRC_DIR_IN_REPO = "spec"
BLOB = f"https://github.com/{REPO}/blob/{BRANCH}/"

HEADER = (
    "<!-- DO NOT EDIT. Generated from "
    f"{REPO} {SRC_DIR_IN_REPO}/ard.md by scripts/sync-spec.py. -->\n"
)

LINK_RE = re.compile(r"\]\((?P<t>[^)]+)\)")


def rewrite(target: str) -> str:
    """Rewrite a single link target; leave external links and anchors alone."""
    if re.match(r"^(https?:|mailto:|#)", target):
        return target
    # Resolve the repo-relative path against the source file's directory.
    repo_path = posixpath.normpath(posixpath.join(SRC_DIR_IN_REPO, target))
    return BLOB + repo_path


def main() -> int:
    src = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.environ.get("ARD_SPEC_SRC", "../ard-spec/spec/ard.md")
    )
    try:
        if re.match(r"^https?:", src):
            with urllib.request.urlopen(src, timeout=30) as r:
                text = r.read().decode("utf-8")
        else:
            with open(src, encoding="utf-8") as f:
                text = f.read()
    except (OSError, urllib.error.URLError) as e:
        sys.stderr.write(f"sync-spec: could not read source {src}: {e}\n")
        return 1
    out = LINK_RE.sub(lambda m: "](" + rewrite(m.group("t")) + ")", text)
    dest = os.path.join(os.path.dirname(__file__), "..", "docs", "spec.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(HEADER + out)
    sys.stderr.write(f"sync-spec: wrote {os.path.normpath(dest)} from {src}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
