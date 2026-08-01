/-!
# The standing register of open statements

Every genuinely open proposition the programme carries is STATED here, with
the `CONJ_` provenance prefix, and left open under the repository's `sorry`
policy (this file is one of the declared sorry-allowed files).

Rules (README, "State the theorem even when you cannot prove it"):

* Formalise the statement even with no proof in sight — it fixes the
  quantifiers, the constants, and the exact hypotheses.
* Never weaken a statement to obtain a green build. A theorem that compiles
  because a hypothesis was added or a constant loosened is worse than an
  honest `sorry`: it looks proved.
* Downstream files call the `CONJ_` name directly, so the open boundary stays
  visible in dependency chains. Do not hide it behind an ordinary alias.
* A stated-but-unproved declaration is never listed as coverage in a
  `proved_theorems` PR note.
-/

import Mathlib

/-- The target conjecture, in the normal form the programme attacks.
Replace this placeholder with the real statement; keep the `CONJ_` prefix
until it is proved. -/
theorem CONJ_target : True := by
  sorry
