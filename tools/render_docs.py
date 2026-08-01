#!/usr/bin/env python3
import os
import subprocess
import sys

PANDOC_INPUT = "markdown+tex_math_dollars+tex_math_single_backslash"
MATHJAX_URL = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"

# Candidate source files to render. Adjust or extend this list if you keep
# a different program-plan filename. Keep it in sync with
# .githooks/pre-commit and .github/workflows/verify-docs.yml.
CANDIDATES = [
    "README.md",
    "docs/program_map.md",
    "NEXT_STEPS.md",
]

found = [p for p in CANDIDATES if os.path.exists(p)]
if not found:
    print("No source files found among candidates; nothing to render.")
    sys.exit(0)

failed = False
for src in found:
    out = os.path.splitext(src)[0] + ".html"
    cmd = [
        "pandoc",
        "--from",
        PANDOC_INPUT,
        src,
        "-s",
        "-o",
        out,
        f"--mathjax={MATHJAX_URL}",
    ]
    print(f"Rendering {src} -> {out}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to render {src}: {e}", file=sys.stderr)
        failed = True

if failed:
    sys.exit(1)

print("Rendered files:", ", ".join(os.path.splitext(s)[0] + '.html' for s in found))
