# {{CONJECTURE_NAME}} campaign

> **Using this template.** This repository was instantiated from
> [`conjecture-attack-template`](https://github.com/eyalk11/conjecture-attack-template),
> a layout for long-running, multi-agent attacks on a mathematical conjecture.
> Follow the checklist in [`TEMPLATE_SETUP.md`](TEMPLATE_SETUP.md), then delete
> this block and that file. Until every `{{…}}` placeholder is filled in, the
> repository is a scaffold, not a programme.

Work towards **{{CONJECTURE_STATEMENT_ONE_LINE}}**. Layout:

- `docs/` — notes and manuscripts (`.md`, `.tex`, built `.pdf`). Dated working
  notes land here first; results are later transcribed into the master
  manuscript (see "Write proofs out in full" in [`AGENTS.md`](AGENTS.md)).
- `scripts/` — verifiers, probes and search programs, together with the raw
  output files they produced.
- `lean/` — the Lean formalisation. Partly machine-written; see
  "The Lean formalisation, and who writes it" below before reviewing it.
- `lit/` — the papers cited in the literature scan.
- `old/` — superseded material, kept for the record. Do not delete old notes;
  move them here.
- `agent_status/` — one JSON file per AI agent session: branch, start time,
  task. Kept on `master` so concurrent agents on separate branches can see
  each other. Conventions for agents are in [`AGENTS.md`](AGENTS.md)
  (mirrored by [`CLAUDE.md`](CLAUDE.md)).

---

## Authoritative manuscript

[`master.tex`](master.tex) is the authoritative manuscript and the source of
truth for theorem statements, proofs, numbering, labels, and remarks. If it
conflicts with a note under `docs/`, a generated Blueprint file, or a theorem
export, the master TeX file takes precedence.

The Lean Blueprint and the HTML/Markdown theorem tables are derived artifacts:

- `blueprint/src/content.tex` is generated from the authoritative manuscript
  and `scripts/theorem_lean_correspondence.json`;
- `theorems_with_lean.html` and `theorems_with_lean.md` are generated views
  pairing manuscript statements with their Lean counterparts.

Changes to mathematical prose or theorem statements must be made first in
`master.tex`, followed by regeneration of those derived files
(`scripts/generate_lean_blueprint.py`, `scripts/dump_theorems_with_lean.py`).

## Start here

| read | file | what it is |
|:--|:--|:--|
| 1 | [`NEXT_STEPS.md`](NEXT_STEPS.md) | **Live execution and status manuscript.** The current critical path and the precise remaining gaps. |
| 2 | [`docs/latest_state.md`](docs/latest_state.md) | **Current state in two minutes.** The surviving route, the routes just refuted, and the next decisive computation. |
| 3 | [`master.tex`](master.tex) | **The authoritative manuscript.** The source of truth for integrated theorem statements, proofs, labels, and remarks. |
| 4 | [`RESULTS.md`](RESULTS.md) | **What is actually proved, in one table.** Every partial result with its constant/scope, what is *not* a class theorem and why, and the Lean status of each. Start here if the question is "what do we have", not "what are we doing next". |
| 5 | [`docs/evidence_ledger.md`](docs/evidence_ledger.md) | **The evidence ledger.** What has been computed, at what scale, and — the part that keeps mattering — what it does *not* license. Grades every number **E**/**D**/**W**/**I**. |
| 6 | [`docs/program_map.md`](docs/program_map.md) | **The map.** Diagrams of the whole route — proved / refuted / open / in-flight — plus the critical path in one line. |
| 7 | [`REFUTED_CONJECTURES.md`](REFUTED_CONJECTURES.md) | **The negative-results index.** Every statement this programme proposed and then killed, with the witness that killed it, graded refuted / retired / only-numerically-refuted. Explicitly partial. Read it before proposing a mechanism. |

A referenced index of the load-bearing theorems, ordered by weight rather than
section number, is [`IMPORTANT_THEOREMS.tex`](IMPORTANT_THEOREMS.tex). The
alternative paths to the target — routes other than the master's spine, each
with what it has proved and what it still needs — are collected in
[`docs/extended_manuscript.md`](docs/extended_manuscript.md), which also holds
results proved but not yet authorised into the master.

**Keep the theorem index synchronized.** Whenever a change adds or materially
strengthens a load-bearing theorem — whether in the authoritative master or in
a proved working note — update `IMPORTANT_THEOREMS.tex` in the same change.
If a result is deliberately omitted from that index, say why in the pull
request. The index must point to the full proof; it is never a substitute for
recording the proof in its authoritative manuscript or designated proof note.

## Current state — {{DATE}}

**{{CONJECTURE_NAME}} is open.** The live formulation, the current active
routes, and the most recent refutations are below. The authoritative running
version of this is [`docs/latest_state.md`](docs/latest_state.md); if it and
this section disagree, it wins.

### The target in one line

{{Write the conjecture as one displayed statement, in the exact normal form the
programme is attacking — the reduction actually being used, not the textbook
phrasing. Name the bottleneck explicitly: which single statement, if proved,
closes the conjecture.}}

### The approach, and why it is strong

### What is proved

[`RESULTS.md`](RESULTS.md) is the table. {{One paragraph summary. End with the
honest scope line, e.g.: "These are class theorems and exact reductions. None
of them proves the conjecture in general — `RESULTS.md` says which is which,
and why."}}

### The most recent refutations

{{The two or three latest kills, one bullet each: what was refuted, by which
witness, what it does *not* refute, and the note carrying the proof. Move
older ones into `REFUTED_CONJECTURES.md` and the historical section.}}

### Active routes

{{A short numbered list. Each route: one sentence of mechanism, one sentence of
next decisive step. Before proposing anything else, read
[`REFUTED_CONJECTURES.md`](REFUTED_CONJECTURES.md) — and note that it is
partial, so absence from it is not evidence a route is alive.}}


### State the theorem even when you cannot prove it

An unproved statement is worth writing down. Formalising the *statement* fixes
the quantifiers, the constants, and the exact hypotheses — which is where
programmes like this repeatedly lose time — and it makes the gap explicit and
addressable instead of leaving it in prose. So:

- Write the Lean statement first, with the right provenance prefix
  (`CONJ_…` for an open proposition, `EXT_…` for a published input you are not
  reproving), and leave the proof open under the repository's `sorry` policy —
  `lean/conjectures.lean` and the `*_deps.lean` files are exactly where an
  unproved statement is allowed to live, and `conjectures.lean` is the
  standing register of what is open.
- Do **not** weaken the statement to obtain a green build. A theorem that
  compiles because a hypothesis was added or a constant loosened is worse than
  an honest `sorry`: it looks proved. See "A green check is not a proof of what
  you meant" below.
- Where the missing input is an external theorem, prefer carrying it as an
  explicit hypothesis of the statement over axiomatising a placeholder.
- Say in the `proved_theorems` note (below) which declarations are statements
  only. A stated-but-unproved theorem must never be listed as coverage.


### A green check is not a proof of what you meant

The agent's objective is to make the build succeed. That is not the same as
preserving the statement you wrote. Two failure modes to look for explicitly
when reviewing its commits:

1. **Statement weakening.** A hypothesis added, a constant loosened, or a
   conclusion narrowed until the proof goes through. Diff the theorem
   *statements* against the pre-agent commit, not just the proofs.
2. **Vacuous or unsound assumptions.** A `sorry`-carrying placeholder that is
   actually false proves everything downstream. The `deps-sorry-policy` and
   `sorry-allowed-files` inputs confine `sorry` to `lean/*_deps.lean` and the
   external/conjecture files, but they do not check that what is assumed there
   is *true*. Where an external theorem is genuinely needed, prefer carrying it
   as an explicit hypothesis of the theorem over axiomatising a placeholder.

### Lean provenance prefixes

Public declarations at a proof boundary use a visible prefix:

| prefix | meaning |
|:--|:--|
| `EXT_…` | A theorem imported from a verified external package, or a deliberately unproved published-theorem input. |
| `CONJ_…` | A genuinely open proposition carried as a conjectural declaration. |
| `CALC_…` | A finite computational certificate or a claim whose substantive evidence is exact or exhaustive computation. |
| no prefix | A theorem proved internally by this development. |

The prefix records where the mathematical content comes from, not which tactic
Lean happened to use. A general symbolic theorem proved using `norm_num`,
`ring`, `decide`, or `native_decide` keeps an ordinary name when computation is
only an implementation detail. Use `CALC_…` when the finite enumeration,
specific witness calculation, or exact machine computation is itself the
result. A kernel-checked `CALC_…` theorem can be completely rigorous while
still being evidence about a finite case rather than a general theorem.

Downstream files should call the prefixed name so that external assumptions,
open conjectures, and computational evidence remain visible in dependency
chains. Do not hide one of these boundaries behind an ordinary local alias.

### `proved_theorems` note in Lean pull requests

Every pull request that adds or materially strengthens Lean proofs must attach
a short `proved_theorems` note in its description. For each result, mention
only:

- the Lean declaration name; and
- the manuscript theorem, label, or reference note it formalises.

For example:

```text
proved_theorems
- partA_mainReduction_full — Theorem `thm:main-reduction` in `master.tex`.
- entropy_han_inequality_nats — Appendix Lemma `lem:han-full`.
```

Do not use this note to claim more coverage than the declaration has. If the
Lean theorem is conditional, external, computational, or only a special case,
retain the corresponding `CONJ_…`, `EXT_…`, or `CALC_…` provenance and say
which reference note describes the limitation. The note is an index for
reviewers, not a substitute for comparing the Lean statement with the
authoritative manuscript.

Also Update LEAN_STATE.md 

### Packaging gotcha

The `lean_lib` in `lakefile.toml` pins an explicit `roots` list and no
`globs`. The default per-root glob then means **only the listed modules belong
to the library**: a new file under `lean/` that is not named in `roots` cannot
be imported, and the build fails with `unknown module prefix`. Add every new
module to `roots`.

## Verification and corrections

| file | role |
|:--|:--|
| [`REFUTED_CONJECTURES.md`](REFUTED_CONJECTURES.md) | The **negative-results index**: what was refuted, by which witness, and what survived each refutation. Partial by construction — add to it when you kill something. |
| [`docs/evidence_ledger.md`](docs/evidence_ledger.md) | The graded record of every computation, and the verification log: what was independently re-derived, to what precision, and which statements were withdrawn. |
| {{dated correction notes}} | {{When a claim is withdrawn or corrected, the note carrying the correction gets a row here. The table is how a reader finds out a number they saw elsewhere is dead.}} |

## Literature

{{Where the literature scan lives, in reading order, and — crucially — the
current net verdict: which imported results supply usable leverage and which
credited items were later withdrawn. Papers themselves go in `lit/`. If no
item in the scan supplies an inequality the programme can use, say exactly
that.}}

## Standing warnings

Warnings are earned, not copied: when a computation or convention misleads the
programme, the lesson goes here, numbered, with the witness that taught it.
Four inherited from the FEI campaign that produced this template — each was
learned the hard way, and each generalises:

1. **Small-case evidence is not evidence.** Statements holding without
   exception across an entire exhaustive small parameter range have been false
   at the next size up. Fix the smallest size at which your programme's
   phenomena first appear, and treat anything below it as no evidence at all.
2. **Descents give upper bounds only.** A search minimum cannot see a region
   the search did not enter. Only exhaustive enumeration licenses a claim about
   a class; label everything else as a bound in the direction it actually
   controls.
3. **Search the quantity you are conjecturing.** Optimising a proxy finds the
   proxy's extremisers, and they can separate from the target's at the very
   sizes you care about. Point at least one search directly at the conjectured
   quantity before trusting a proxy's landscape.
4. **Check index conventions against an asymmetric case.** A regression on a
   symmetric state cannot catch an asymmetry bug. Derive masses and derived
   laws from the *same* array, and keep one verifier with no index arithmetic
   at all.
5. **Check agent_status before working on task** It might be related.
   Dont necessarily read the entire work unless permited, to not be confused by alternative directions.
6. **Agent status might contain stale tasks** 
   
