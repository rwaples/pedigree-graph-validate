# Known differences

Each id is a difference between pedigree-graph and an oracle that the harness
reports as DIFF instead of FAIL, because the cause is understood. A row stays
FAIL for any mismatch its rule does not cover.

## D1: the cousin categories are not "full = mated pair"

**Rows:** "closest category, GLOSSARY mated-pair rule" (classification,
against verbalisr). Tracked in pedigree-graph#47.

pedigree-graph's GLOSSARY ("Relationship category") defines a full category as
one whose connecting ancestors are a mated pair. Its engine follows that for
the sibs and the avuncular categories only. First cousins are full with at
least two distinct shared grandparents, the removed cousins and second cousins
with at least two paths, each orientation of a removed-cousin pair on its own
(engine.rs `cousins`, `removed_cousins`, `second_cousins`). Its ADR 0010 keeps
this split on purpose ("Categories are the 0.7.1 definitions").

The scored "closest category" rows apply the engine's rules to verbalisr's
paths (`conversions.py::path_categories`, `rule="engine"`) and agree on every
pair checked. The D1 row applies the GLOSSARY rule (`rule="mated_pair"`) and
counts the pairs where the label would change:

- `conventions` 23-24, double half first cousins (shared grandparents 13 and
  16 are not mates): engine 1C, mated pair H1C.
- `deep_chain` 20-27, connected only through ancestor 1 by four routes:
  engine 1C1R, mated pair H1C1R.

Kinship is unaffected. In every differing pair on `conventions`,
`deep_chain` and `atlas` (263 pairs), the engine label's nominal kinship is
nearer the pair's `pair_kinship` than the mated-pair label's.

## D2: Ne_iΔF over all rows, t <= 1

**Rows:** atlas "ne_idf_t1, reference = all" (moved from pedsum-validate).

purgeR's `pop_Ne` computes 1 - (1 - F)^(1/(t - 1)) for every row it is given
(cran/purgeR `R/Ne.R`, `delta_Fi`), so a row with t <= 1 and F = 0, such as a
founder, enters the mean as a rate of 0; pedigree-graph's
`ne_unrelated_founders` drops rows with t <= 1. On target rows (all t > 1)
the two agree to 1e-8.
