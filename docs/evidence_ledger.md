# The empirical evidence ledger

**Updated:** {{DATE}}
**Status:** This note contains **no proofs**. It is a ledger of what has
actually been computed, at what scale, by what method, and — the part that
repeatedly matters — what the computations are *not* entitled to support.
Nothing here is evidence for anything until §1's grading is applied to it.

**Why this note exists.** Programmes get misled by computation: statements
holding without a single exception across an entire exhaustive small range can
be false at the next size up. An evidence ledger that does not grade itself is
how that happens again.

---

## 1. Grading rules

Every number below carries one of four grades. The grade, not the number, is
what licenses an inference.

| grade | meaning | what it licenses |
|:--|:--|:--|
| **E** | exhaustive enumeration of a complete admissible class | a theorem *about that class* |
| **D** | descent / beam / annealing search over admissible states | an **upper** bound on the true extremum, nothing else |
| **W** | a single certified witness, using exact or outward-rounded interval arithmetic | a refutation, if the certified interval has the wrong sign |
| **I** | an identity cross-check to machine precision | confidence in the implementation, not in the mathematics |

Two rules follow:

1. **A grade-D number is never cited as an extremum.** It is an upper (or
   lower) bound in the direction the search controls, and nothing more.
2. **A conjecture may not rest on data below the programme's known
   instability size.** Record that size here the moment it is discovered, and
   treat everything below it as no evidence at all.

## 2. The statements under test

{{Display the precise statements the computations below bear on, each with a
letter, so every table row can point at one.}}

## 3. Ledger

| quantity | value | scale / class | grade | script → output file |
|:--|:--|:--|:--|:--|
| *(no entries yet)* | | | | |

## 4. Verification log

{{What was independently re-derived, to what precision, by which second
implementation, and which previously published statements were withdrawn as a
result. Withdrawn claims also get a row in the README's "Verification and
corrections" table.}}

## 5. Reproducibility index

Every published number maps to the script and section that produces it:

| number (where cited) | script | command / seed |
|:--|:--|:--|
| *(no entries yet)* | | |
