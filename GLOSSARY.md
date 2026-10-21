# pedigree-graph-validate glossary

**Oracle**:
Other software that implements a method pedigree-graph also implements,
installed at a pinned version and rerun live on the same input, never copied
(ADR 0001). Its output is the reference a Check is scored against.
_Avoid_: golden, ground truth

**Published value**:
A number printed in a paper, vignette or test file. It is recorded beside the
Oracle's rerun as an INFO row, for provenance, and never scored.
_Avoid_: expected value, truth

**Case**:
One input pedigree (seeded, bundled with an R package, or downloaded) run
through both pedigree-graph bindings and every Oracle its Checks name. One
entry under `cases:` in cases.yaml.

**Check**:
One comparison of one pedigree-graph result with one reference, at a stated
tolerance, giving one row of results. Both bindings must meet it, and agree
with each other exactly.

**Conversion**:
A declared mapping from an Oracle's convention to pedigree-graph's, from the
closed list in conversions.py, shown in the row. A gap that no listed
Conversion explains is a FAIL.
_Avoid_: correction, adjustment

**Cap**:
A size or resource limit on one Oracle (rows, sampled pairs, wall time,
memory), stated in cases.yaml. A Case over a Cap writes a skip row naming it,
never nothing.
_Avoid_: budget (for a single limit)

**Status**:
The outcome of a Check: PASS (within tolerance), DIFF (a known difference,
explained in differences.md), GAP (not checked, with an id), INFO (not
scored), SKIP (over a Cap), FAIL, ERROR. A FAIL or ERROR makes the harness
exit 1.

**Release pair**:
The PyPI wheel and the R source tarball of one pedigree-graph release, the
pin both bindings are checked at (pixi.toml, pedigreegraph.pin).
