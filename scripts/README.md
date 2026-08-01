# scripts/

Verifiers, probes and search programs, with the raw output files they
produced. Conventions:

- **Naming.** `verify_*` re-derives a claimed identity or bound
  independently; `audit_*` checks a specific manuscript claim against
  computation; `probe_*` / `climb_*` / `search_*` explore. The name should say
  which of these it is, because they license different inferences (see the
  E/D/W/I grades in [`../docs/evidence_ledger.md`](../docs/evidence_ledger.md)).
- **Raw output is committed** next to the program that produced it, with the
  exact command and seed in the file or in the ledger's reproducibility index.
- **Exact arithmetic first.** Integer or rational kernels, interval arithmetic
  (outward-rounded) for certification; floating point confined to logarithms
  and display. A refutation witness must be certified (grade **W**), not
  float-observed.
- **Every published number** gets a row in the evidence ledger with its grade
  and the script that produces it. A computation without a ledger row is not
  a claim.
- `theorem_lean_correspondence.json` is the hand-curated ledger pairing
  manuscript labels with Lean declarations; `generate_lean_blueprint.py` and
  `dump_theorems_with_lean.py` generate the blueprint and the theorem tables
  from it and `master.tex`.
