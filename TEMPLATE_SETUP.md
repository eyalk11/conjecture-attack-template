# Instantiating this template

This repository is a layout for a long-running, possibly multi-agent attack on
a mathematical conjecture, extracted from the working conventions of
[`eyalk11/fei_conjecture`](https://github.com/eyalk11/fei_conjecture) (the
Fourier Entropy–Influence campaign). Everything here was earned there: the
authoritative-manuscript discipline, the negative-results index, the graded
evidence ledger, the agent status board, and the Lean/blueprint pipeline.

Work through this checklist, then delete this file and the "Using this
template" block at the top of `README.md`.

## 1. Name the target

- [ ] Replace every `{{…}}` placeholder. Find them all with:

      grep -rn '{{' --include='*.md' --include='*.tex' .

- [ ] `README.md` — conjecture name, one-line statement, "The target in one
      line", approach, active routes.
- [ ] `master.tex` — title, and the conjecture stated as the first
      environment (`conj:target`).
- [ ] `docs/latest_state.md`, `NEXT_STEPS.md` — initial state.

## 2. Decide names (defaults are fine)

The template uses generic file names; keep them, or rename consistently
everywhere (README, AGENTS.md, workflows, hook, `tools/render_docs.py`,
blueprint scripts):

| file | role |
|:--|:--|
| `master.tex` | authoritative manuscript |
| `NEXT_STEPS.md` | live execution/status manuscript |
| `RESULTS.md` | proved-results table |
| `REFUTED_CONJECTURES.md` | negative-results index |
| `IMPORTANT_THEOREMS.tex` | weighted theorem index |
| `docs/latest_state.md` | two-minute current state |
| `docs/evidence_ledger.md` | graded computation ledger |
| `docs/program_map.md` | route map (mermaid) |
| `docs/extended_manuscript.md` | alternative-paths layer |

## 3. Lean (optional but recommended)

- [ ] Pick the library name (default `Conjecture`) — it appears in
      `lakefile.toml` (`name`, `defaultTargets`, `lean_lib`, `roots`),
      `lean/Conjecture.lean`, the workflows' `imports:` input, and
      `scripts/generate_lean_blueprint.py` (`LEAN_LIB`).
- [ ] Check/update the pinned `lean-toolchain` and the mathlib rev in
      `lakefile.toml`; run `lake update` once and commit `lake-manifest.json`.
- [ ] As the manuscript grows parts, add `lean/part_<x>.lean` files and
      register them in `roots`.
- [ ] If you use AI Lean Generate, keep `.github/workflows/ai-lean-generate.yml`
      and read the trust notes in `README.md`. Otherwise delete it.

## 4. Docs rendering

- [ ] `pandoc` is required for the rendered HTML views. Install the hook:

      git config core.hooksPath .githooks

- [ ] Or delete the rendering machinery (`tools/render_docs.py`,
      `.githooks/pre-commit`, `.github/workflows/verify-docs.yml`, and the
      `.html` mentions in README/AGENTS) if you don't want checked-in HTML.

## 5. Blueprint (optional)

`scripts/generate_lean_blueprint.py` and `scripts/dump_theorems_with_lean.py`
parse the theorem environments of `master.tex` and pair them with Lean
declarations through the hand-curated ledger
`scripts/theorem_lean_correspondence.json`. They assume the master uses
`\part{Part A}` … headings and standard `theorem`/`lemma`/`proposition`/
`corollary`/`conjecture` environments with `\label{}`s. Delete `blueprint/`
and the two scripts if you don't want this pipeline.

## 6. Multi-agent conventions

- [ ] Read `AGENTS.md` end to end; it is the contract every agent session is
      pointed at (`CLAUDE.md` just includes it).
- [ ] The `agent_status/` board lives on `master`; the branch/PR discipline is
      in `AGENTS.md`. Adjust the branch-name examples if your default branch
      is `main` rather than `master` (and update the workflows' `branches:`
      filters to match).

## 7. Seed the ledgers honestly

`REFUTED_CONJECTURES.md`, `RESULTS.md` and `docs/evidence_ledger.md` start
empty. Resist the urge to fill them with aspirations: the whole value of the
system is that every entry is backed by a proof, a witness, or a graded
computation. Empty and honest beats full and hopeful.
