/-!
# External inputs

Published theorems the development uses but does not reprove live here, with
the `EXT_` provenance prefix, under the `sorry` policy (this file is one of
the declared sorry-allowed files).

Prefer carrying an external theorem as an explicit HYPOTHESIS of the theorem
that needs it over axiomatising a placeholder here: a `sorry`-carrying
placeholder that is actually false proves everything downstream (README,
"A green check is not a proof of what you meant"). Use this file only when a
hypothesis is genuinely impractical, and cite the source precisely.
-/

import Mathlib

/-- Example shape of an external input. Delete once real content exists.
Cite: {{author, paper, theorem number}}. -/
theorem EXT_example : True := by
  sorry
