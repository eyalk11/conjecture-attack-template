# Lean Blueprint

`master.tex` is the authoritative manuscript. This Blueprint is a generated
alignment view and does not supersede the master TeX file. Mathematical
statements and prose must be edited in the master first.

The blueprint is generated from:

- `master.tex`
- `scripts/theorem_lean_correspondence.json`

Regenerate the tracked source after either input changes:

```text
python scripts/generate_lean_blueprint.py
```

Install the pinned tooling and build locally:

```text
python -m pip install -r requirements-blueprint.txt
leanblueprint web
leanblueprint pdf
leanblueprint checkdecls
```

The web build requires Graphviz. The declaration check also requires a
successful `lake build`.

Hand-maintained supplements (e.g. a dependency blueprint for a closed case)
may live in `src/` alongside the generated `content.tex`; they are input from
`web.tex`/`print.tex` explicitly and must be kept synchronized with their
corresponding manuscripts and Lean entrypoints by hand.
