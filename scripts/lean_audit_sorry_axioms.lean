/-
Sorry / axiom audit for the project's Lean library.

Run from the repository root:

    lake env lean scripts/lean_audit_sorry_axioms.lean

Two checks, both of which a green `lake build` gives you nothing on (see
README, "A green check is not a proof of what you meant"):

1. SORRY CONFINEMENT.  `sorry` may only be *written* in the declared
   placeholder files -- anything matching `*_deps`, plus the external /
   conjecture modules listed in `allowedSorryModules`.  This is a semantic
   check, not a grep: it looks for `sorryAx` occurring directly in a
   declaration's own type or value.  Prose like "this file is sorry-free"
   does not trip it, and a real `sorry` hidden behind a macro does.

   Note "directly".  A theorem that legitimately cites a lemma from a
   `_deps` file inherits `sorryAx` *transitively* -- that is the whole point
   of the deps files and is not a finding.  Only the declaration that
   actually contains the hole is reported.

2. AXIOM CLEANLINESS.  Declarations named in `lean/axiom_clean.txt` must
   depend on nothing beyond Lean's own three (`propext`, `Classical.choice`,
   `Quot.sound`) -- no `sorryAx`, no project axioms, nothing carried in from
   a deps file.  That file is the checked-in list of results claimed to be
   unconditional; this check is what stops one of them silently acquiring a
   dependency later.  A missing or empty list makes the check a no-op.

`--report` (or AUDIT_REPORT=1) additionally prints every project declaration
that is currently axiom-clean, which is how you populate `axiom_clean.txt`
in the first place.
-/

-- The audit has to see every root of the lean_lib. Keep these imports in sync
-- with `roots` in lakefile.toml.
import Conjecture
import conjectures
import external_theorems

import Lean

open Lean

namespace ProjectAudit

/-- Modules whose declarations are allowed to contain `sorry`. Anything whose
name ends in `_deps` is allowed implicitly; these are the named exceptions. -/
def allowedSorryModules : Array Name :=
  #[`external_theorems, `conjectures]

/-- Is this one of the project's own modules (as opposed to Mathlib etc.)?
Keep in sync with `roots` in lakefile.toml: the library root plus every
lowercase module. Adjust the predicate if you adopt a naming prefix. -/
def isProjectModule (m : Name) : Bool :=
  let s := m.toString
  s == "Conjecture" || s == "conjectures" || s == "external_theorems"
    || s.startsWith "part_" || s.endsWith "_deps"

/-- The axioms every ordinary Mathlib proof rests on. Anything else in a
declaration's footprint is a finding. -/
def benignAxioms : Array Name :=
  #[``propext, ``Classical.choice, ``Quot.sound]

def sorryAllowed (m : Name) : Bool :=
  allowedSorryModules.contains m || m.toString.endsWith "_deps"

/-- The declaration's body. `ConstantInfo.value?` returns `none` for theorems --
proof terms are not handed out through it -- so `.thmInfo` has to be matched
explicitly. Getting this wrong makes the sorry check silently vacuous on every
theorem in the library, which is most of it. -/
def declValue? : ConstantInfo → Option Expr
  | .thmInfo tv => some tv.value
  | ci          => ci.value?

/-- Does this declaration *itself* contain a hole, as opposed to inheriting one
from something it cites? -/
def hasDirectSorry (ci : ConstantInfo) : Bool :=
  let hit (e : Expr) : Bool := e.isConstOf ``sorryAx
  (ci.type.find? hit).isSome || ((declValue? ci).bind (·.find? hit)).isSome

/-- Declarations Lean generates for you (`_proof_1`, match equations, ...).
Reporting them just duplicates the parent declaration. -/
def isNoise (n : Name) : Bool :=
  n.isInternal || n.hasMacroScopes

/-- Every declaration defined in a project module, paired with that module. -/
def projectDecls (env : Environment) : Array (Name × Name) := Id.run do
  let mods := env.header.moduleNames
  let data := env.header.moduleData
  let mut out := #[]
  for i in [0 : mods.size] do
    let m := mods[i]!
    if isProjectModule m then
      for n in data[i]!.constNames do
        unless isNoise n do
          out := out.push (n, m)
  return out

def readAxiomCleanList : IO (Array Name) := do
  let path : System.FilePath := "lean" / "axiom_clean.txt"
  if !(← path.pathExists) then return #[]
  let lines := (← IO.FS.readFile path).splitOn "\n"
  return lines.foldl (init := #[]) fun acc raw =>
    let l := raw.trimAscii.toString
    if l.isEmpty || l.startsWith "#" then acc else acc.push l.toName

end ProjectAudit

open ProjectAudit in
#eval show CoreM Unit from do
  let env ← getEnv
  let decls := projectDecls env
  let report := (← IO.getEnv "AUDIT_REPORT").isSome

  -- 1. sorry confinement
  let mut stray : Array (Name × Name) := #[]
  for (n, m) in decls do
    unless sorryAllowed m do
      if let some ci := env.find? n then
        if hasDirectSorry ci then
          stray := stray.push (n, m)

  -- 2. axiom cleanliness of the declared-unconditional results
  let claimed ← readAxiomCleanList
  let mut missing : Array Name := #[]
  let mut dirty : Array (Name × Array Name) := #[]
  for n in claimed do
    if !env.contains n then
      missing := missing.push n
    else
      let ax ← collectAxioms n
      let bad := ax.filter (!benignAxioms.contains ·)
      unless bad.isEmpty do
        dirty := dirty.push (n, bad)

  if report then
    IO.println s!"-- {decls.size} declarations in project modules"
    for (n, _) in decls do
      let ax ← collectAxioms n
      if ax.all (benignAxioms.contains ·) then
        IO.println n

  let mut errs : Array String := #[]
  unless stray.isEmpty do
    let body := String.intercalate "\n" <|
      (stray.map fun (n, m) => s!"  {n}    (in {m})").toList
    errs := errs.push
      s!"`sorry` outside the declared placeholder files ({stray.size}):\n{body}\n\
         Move the hole into a `*_deps` module, or add the module to \
         allowedSorryModules if it is genuinely a declared exception."
  unless missing.isEmpty do
    let body := String.intercalate "\n" ((missing.map (s!"  {·}")).toList)
    errs := errs.push
      s!"lean/axiom_clean.txt names declarations that do not exist ({missing.size}):\n{body}\n\
         They were renamed or removed; fix the list."
  unless dirty.isEmpty do
    let body := String.intercalate "\n" <|
      (dirty.map fun (n, bad) => s!"  {n}  depends on  {bad}").toList
    errs := errs.push
      s!"declarations claimed unconditional but are not ({dirty.size}):\n{body}\n\
         Either the proof regressed, or the claim in axiom_clean.txt was wrong."

  if errs.isEmpty then
    IO.println s!"audit ok: {decls.size} project declarations, \
      {claimed.size} claimed unconditional, no stray sorry"
  else
    throwError (String.intercalate "\n\n" errs.toList)
