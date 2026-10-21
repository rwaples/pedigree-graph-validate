# ADR 0001: Oracles are rerun live; published values are INFO

**Status:** accepted
**Date:** 2026-10-21

## Context

pedigree-graph's own tests compare it with in-house references: retired
SciPy and numba kernels and hand recurrences under `tests/oracle/`. None of
them is independent software. pedsum-validate checks pedsum, which is built on
pedigree-graph, against numbers printed in papers, vignettes and package test
files; its Ne rows, for instance, are purgeR's printed values on purgeR's
bundled pedigrees.

A printed number cannot move, so it cannot show that the software that printed
it has changed, and it exists only for the pedigrees someone published. The
oracles here (kinship2, ribd, verbalisr, GENLIB, nadiv, pedigreeTools,
AGHmatrix, purgeR, visPedigree) are GPL; this repo is MIT. Only kinship2 and
GENLIB are on conda-forge.

## Decision

1. **Every scored reference is an Oracle rerun live** on the Case's input at
   a pinned version. A published value for the same quantity is kept as an
   INFO row beside it.
2. **Oracles are installed and called, never vendored.** conda-forge
   packages are pinned by `pixi.lock`; the others are CRAN source tarballs
   pinned by sha256 in `oracles.lock` and installed into `.r-lib/`, which
   refuses a hash mismatch.
3. **Ne and lineage checking lives here**, not in pedsum-validate. Its rows
   are removed from pedsum-validate only after this repo checks each of them.
4. **A Case over an Oracle's Cap writes a SKIP row**, never nothing.

## Consequences

- A FAIL means pedigree-graph moved, or an oracle did. Rows record every
  version, so a relock shows which.
- A Monte Carlo oracle (purgeR's `pop_Ng()`) needs a statistical acceptance
  rule, not a tolerance.
- The harness depends on GPL packages at run time only; nothing GPL is
  distributed.
