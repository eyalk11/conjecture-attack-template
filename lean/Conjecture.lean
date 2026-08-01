/-!
The library root. Import every module of the development here so that
`import Conjecture` pulls in the whole library.

As the manuscript grows parts, add `lean/part_<x>.lean` files mirroring the
parts of `master.tex` one-to-one, import them here, and register them in the
`roots` list of `lakefile.toml` (see the packaging gotcha in README.md).
-/

import conjectures
import external_theorems
