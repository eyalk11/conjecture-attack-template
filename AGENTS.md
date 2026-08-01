# Working in this repository

## Start by reading the README

Before touching anything — before searching, before editing, before planning —
read [`README.md`](README.md) end to end. It tells you which file is
authoritative, which files are *derived* from it (and therefore must never be
hand-edited), what the current live target is, what has already been refuted,
and the standing warnings that were each learned the hard way. Then follow its
"Start here" table, at minimum items 1–3
([`NEXT_STEPS.md`](NEXT_STEPS.md), [`docs/latest_state.md`](docs/latest_state.md),
[`master.tex`](master.tex)).

Much of a long conjecture programme's history is *negative* results.
Re-proposing a refuted route is the most common way to waste a session, and the
README is what prevents it. Though you may want to search notes.

[`REFUTED_CONJECTURES.md`](REFUTED_CONJECTURES.md) is the index of those
negative results: one entry per statement the programme proposed and then
killed, with the witness that killed it, what survived it, and a grade
distinguishing *refuted by proof*, *refuted by counterexample*, *retired*
(true-but-useless, e.g. collapsed to the target) and *claimed refuted on
numerical evidence only* — the last of which are still open and must not be
cited as dead. Read it before proposing any mechanism.

The file is **partial**: absence from it is not evidence that a route is
alive. When you refute or retire something, add an entry — statement, grade,
witness, what survived, and the note or script that carries the proof.

## Important guidelines

* You should work in your own branch.
* Don't push to master unless you have been authorized to do so, apart from
  `agent_status` which you can and should push to master.

`agent_status/` commits are described below. They are the exception to this rule.

- Do not change the authoritative manuscript in master (esp. remote) without
  permission. Not recommended in the branch unless asked to as well.
- Do mention the branch you are pushing to when you do!

- Do all work on a branch, and push only that branch. Pushing a branch that is
  yours needs no permission — do not sit on unpushed commits waiting for one.
- Do not merge to `master`, do not fast-forward it, never force-push it.
- When the work is done, open a pull request for the branch, with a purpose line
  saying which kind it is and an entry in the `open_prs` list of your status
  file. Opening it is not authorisation to merge it — merging stays a user
  decision.
- **Subagents push nothing.** A subagent commits to no remote and touches no
  shared ref; it reports to its parent, and the parent decides what is pushed.

See the README, "Branches, pushes and pull requests" below, for the full
statement of what that licence does and does not cover.

REFUTED_CONJECTURES.md can be updated in master in some cases. Ask.

## Never switch branches in the main repository checkout

Treat the main repository folder as belonging to the user. It is normally
expected to be checked out on `master`; do not assume that it is.

- Never run `git checkout`, `git switch`, or any equivalent operation that
  changes or detaches `HEAD` in the main repository folder without the user's
  explicit permission in the current session.
- Never create and check out a task branch in the main repository folder
  without that permission.
- Before any direct commit in the main repository folder, first verify the
  checked-out branch. Commit there only when the user has explicitly permitted
  a direct commit and the verified branch is the intended target (normally
  `master`).
- For work that needs another branch, create a separate Git worktree and do all
  branch changes, commits, builds, and pushes from that worktree.
- If the main repository is on a branch other than the expected `master`, report
  the exact state and ask before changing it. Do not switch it back as an
  automatic "cleanup" step.

## `agent_status/` — the shared status board

`agent_status/` lives on `master` so that every agent, whatever branch it is
working on, can see who else is running and on what. Each agent owns exactly one
file there and writes to no other.

### File name

    agent_status/<subject>_<agentid>.json

- `<subject>` — a short lowercase-hyphenated slug for what you were asked to do
  (`threshold-tail-proof`, `blueprint-regen`, `claude-md-setup`).
- `<agentid>` — an identifier natural to the environment you are running in.
  Take the first one that is set:

      ${CLAUDE_CODE_SESSION_ID%%-*}        # first block of the session UUID
      $CLAUDE_CODE_REMOTE_SESSION_ID       # remote/cloud session id
      $GITHUB_RUN_ID                       # GitHub Actions
      $(shuf -i 100000-999999 -n 1)        # last resort: a random number

  Whatever you pick, keep it for the whole session — the file name must not
  change once created, or you will leave orphans behind.

### Contents

```json
{
  "agent_id": "556aa785",
  "agent_type": "claude-cowork (local)",
  "subject": "claude-md-setup",
  "branch": "claude/claude-md-setup-ofccee",
  "start_time": "2026-07-29T17:06:55Z",
  "last_update": "2026-07-29T17:20:00Z",
  "status": "in_progress",
  "task": "One or two sentences: what the user asked for, in your own words.",
  "open_prs": [
    {
      "number": 32,
      "title": "Lean: bounded-degree formalisation",
      "branch": "claude/some-branch",
      "base": "master",
      "purpose": "What it is for, and whether it is meant to be merged."
    }
  ],
  "notes": "Optional. Blockers, what you touched, what you deliberately did not.",
  "last_commit": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

- `agent_type` — `claude-cowork (local)`, `claude (local)`, `claude (cloud)`,
  `chatgpt (cloud)`, etc.
- `branch` — the branch you are actually committing work to (`master` only if
  you were authorized).
- `start_time` — set once, when you create the file. Never rewrite it.
- `last_update` — refresh on every write. Both timestamps are UTC RFC 3339
  (`date -u +%Y-%m-%dT%H:%M:%SZ`).
- `status` — `in_progress`, `blocked`, `done`, or `abandoned`.
- `open_prs` — every pull request you have open, or `[]`. See below.
- `last_commit` — the SHA of the last commit you pushed to your branch. This is
  used to detect whether your branch has changed since the last time you wrote
  your status file.

### Record your open pull requests

List every PR you open in `open_prs`, and keep the list current when you open,
supersede or close one. Branches alone do not tell another agent what is in
flight, and an unlisted PR is the easiest way for two agents to collide — one
pushes to `master` while the other has the same content sitting in review.

Give each entry a `purpose`, because in this repository a PR is often **not** a
merge request. Several legitimate kinds occur:

- a real change awaiting review and merge;
- a **review-only snapshot**, where the content is already on `master` and the
  PR exists purely so the diff is readable — merging it is a no-op;
- a **CI vehicle**, opened so a workflow that operates on a pull request has
  something to inspect.

Say which it is. A reviewer who merges a snapshot PR thinking it was pending
work has been misled by the omission, not by the diff.

If a PR is superseded, keep it in the list with its `purpose` saying so and by
what, until it is actually closed. And note that PRs based on a snapshot branch
(`review-base/*`, `lean-base/*`) exist only to give such a PR a base — do not
branch from them or build on them.

### When to write it

1. **At the start**, as soon as you know your task and your branch — before the
   real work.
2. **On any material change**: branch changed, blocked, scope changed.
3. **At the end**: set `status` to `done` (or `blocked`/`abandoned`, honestly)
   and refresh `last_update`.

### How to write it

If the user has permitted a direct `master` commit, use the main repository
checkout only after verifying that it is already on `master`. Never switch the
main checkout to make this true. If the verification does not print `master`,
stop and ask the user. The commit must contain nothing but your status file:

```bash
git fetch && git status
git commit -m XXXX  # if git status is strange, let me know
git push -u origin master
```

If the push is rejected because another agent got there first, `git pull --rebase
origin master` and push again — conflicts should not happen, since no two agents
share a file.

Stale files from finished sessions are not garbage: they are the log of who did
what. Do not delete other agents' files, and do not "tidy" the directory.

### Subagents do not touch it

The status board tracks *sessions*, not tasks. Only the top-level agent that
owns the session creates or updates the file. A subagent — anything spawned by
another agent — must not create a file of its own, must not edit its parent's
file, and must not commit to `master` for any reason. It reports back to its
parent, and the parent decides whether the status changed.

## Repository conventions

- [`master.tex`](master.tex) is the source of truth for every theorem
  statement, proof, number, and label. `blueprint/src/content.tex`,
  `theorems_with_lean.html` and `theorems_with_lean.md` are **generated** —
  edit the master TeX first, then regenerate
  (`scripts/generate_lean_blueprint.py`, `scripts/dump_theorems_with_lean.py`).
- Lean lives in `lean/` and is built with `lake exe cache get && lake build`.
  Every new module must be added to the `roots` list of the `lean_lib` in
  `lakefile.toml`, or it is silently not part of the library and the build
  fails with `unknown module prefix`.
- A formalisation of a Part-X manuscript result goes in the matching
  `lean/part_<x>.lean`, not in a new topic file. Other modules are shared
  machinery and external inputs.
- Write the Lean *statement* even when you have no proof — with its `CONJ_…` /
  `EXT_…` prefix, left open under the `sorry` policy. Never weaken a statement
  to make the build green, and never list a stated-but-unproved declaration as
  coverage in a `proved_theorems` note. See README, "The Lean formalisation".
- `sorry` is confined to `lean/*_deps.lean` and the declared external/conjecture
  files. Where an external theorem is needed, prefer carrying it as an explicit
  hypothesis over axiomatising a placeholder.
- A green Lean build is not evidence that the statement you meant survived — see
  README, "A green check is not a proof of what you meant."
- Numerical claims belong in the evidence ledger
  ([`docs/evidence_ledger.md`](docs/evidence_ledger.md)) with their grade and
  the script that produced them. Do not promote a computation to a claim
  without one.
- `README.html`, `NEXT_STEPS.html` and `docs/program_map.html` are the
  rendered views of the corresponding `.md` files, generated by
  `tools/render_docs.py` (pandoc). `.githooks/pre-commit` re-renders them
  and stages the result, so the HTML travels in the same commit as the Markdown.
  Installing it is **optional** — Git does not pick the directory up on its own:

      git config core.hooksPath .githooks

  Without it, run `python tools/render_docs.py` and commit the HTML yourself
  after editing one of those `.md` files. Either way `verify-docs.yml` turns a
  stale committed HTML into a red check on `master`.
- Keep AGENTS.md and CLAUDE.md the same.
- Generally don't delete old notes but move to `old/`.

- Always be creative when researching. If an idea pops up, even if it is not
  exactly the next steps, try to work it.

### Make breakthroughs, believe in yourself. ###

### Write proofs out in full, in both manuscripts

A result is recorded by its **proof**, not by a pointer to the note that has
one. Three standing rules follow.

- The master is the main line. Whatever route the programme is currently
  driving towards the target belongs in [`master.tex`](master.tex), and it goes
  in with the full proof. A theorem environment whose proof body says "see the
  dated note" does not belong in the authoritative manuscript.
- [`docs/extended_manuscript.md`](docs/extended_manuscript.md) is the
  **alternative-paths layer**. It is organised by route, not by chronology:
  one section per alternative approach to the target, each carrying what that
  approach has actually proved, what it still needs, and where it would rejoin
  or replace the master's spine. A result that is simply the master's own
  line, waiting for authorisation, is an integration item, not an alternative
  path — say which it is.
- Every path in it is written out **with complete proofs**, step-checked. The
  status word `proved (note only)` — a statement with a reference where the
  argument should be — is not an acceptable entry. An input carried as an
  explicit hypothesis rather than reproved is fine, but the document must say
  so where it is used.

Length is not a reason to omit a proof, and neither is a computation: an
interval-certified or machine-checked step is written out as the argument plus
the certificate and the script that produced it, with its grade in the evidence
ledger. Keeping the argument in its dated working note as well is right — the
note stays the provenance record and the place corrections land first. What is
not acceptable is the proof existing *only* there.

An alternative path is not a licence to re-propose a dead one: check it against
[`REFUTED_CONJECTURES.md`](REFUTED_CONJECTURES.md) before it gets a section,
and record the grade of anything it revives.

---

## Branches, pushes and pull requests

**Push your own branch, and do not ask first.** A branch you created and are the
only writer of is yours. Pushing it costs nothing, it is what makes the work
reviewable, and it is the only thing that survives a session dying mid-task. Do
not sit on unpushed commits waiting for permission.

"Yours" is the whole of the licence. It does not extend to any ref someone else
writes:

- `master` is not yours. Do not merge to it, do not fast-forward it, never
  force-push it. The single exception is your own `agent_status/` file, which
  you should push to `master` — see above.
- Do not push to a branch another agent is working on — the status board is
  there so you can tell. Do not branch from or build on `review-base/*` or
  `lean-base/*`; they exist only to give a snapshot PR a base.
- Name the branch you pushed to when you report.
- **Subagents do not push at all.** A subagent — anything spawned by another
  agent — commits nothing to any remote and touches no shared ref. It reports
  back to its parent, and the parent decides what gets pushed. This is the same
  rule the status board already uses: sessions push, tasks do not.

**Then try to open a pull request for it**, based on `master`. Give it a purpose
line saying which kind it is — a real change awaiting review, a review-only
snapshot whose content is already on `master`, or a CI vehicle — because in this
repository a PR is often not a merge request, and a reviewer who merges a
snapshot has been misled by the omission. Record it in the `open_prs` list of
your `agent_status/` file and keep that list current. Opening the PR is not
authorisation to merge it: merging stays a user decision.

If you cannot open one — no `gh`, no credentials, no remote — say so plainly in
your report and give the branch name, rather than quietly skipping it.

---
