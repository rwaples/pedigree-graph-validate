# Known differences

Each id is a difference between pedigree-graph and an oracle that the harness
reports as DIFF instead of FAIL, because the cause is understood. A row stays
FAIL for any mismatch its rule does not cover.

## D1: full and half are path counts, not "full = mated pair"

**Rows:** "closest category, genealogical mated-pair rule" (classification,
against verbalisr). Decided in pedigree-graph ADR 0018 (#47, #48): intended.

pedigree-graph decides full against half by path count for every collateral
category: full when at least two paths of the category's shape join the
pair, summed over both orientations, half with one. A sib link is one path
per shared parent id, so a mated pair of shared ancestors gives two, and so
do one ancestor reached by two routes and two unmated ancestors. verbalisr,
like genealogy texts, calls a path full only when it runs through a mated
pair.

The scored "closest category" rows apply pedigree-graph's rule to verbalisr's
paths (`conversions.py::path_categories`, `rule="engine"`: a mated-pair path
counts two, a single-ancestor path one) and agree on every pair checked. The
D1 row applies the genealogical rule (`rule="mated_pair"`) and counts the
pairs whose label would change, for example:

- `conventions` 23-24, double half first cousins (shared grandparents 13 and
  16 are not mates): pg 1C, mated pair H1C.
- `deep_chain` 9-17: an aunt joined by two half paths, pg Av, mated pair HAv.
- `deep_ped` 465-2683: two half great-great-avuncular paths, pg G3Av; the
  mated-pair half code would be degree 6, which pedigree-graph does not
  register, so the genealogical label is none.

With exactly two paths through represented ancestors, pedigree-graph's label
carries the pair's kinship as its nominal kinship; the exact value is
`pair_kinship`, which every oracle here agrees with.

## D2: Ne_iΔF over all rows, t <= 1

**Rows:** atlas "ne_idf_t1, reference = all" (moved from pedsum-validate).

purgeR's `pop_Ne` computes 1 - (1 - F)^(1/(t - 1)) for every row it is given
(cran/purgeR `R/Ne.R`, `delta_Fi`), so a row with t <= 1 and F = 0, such as a
founder, enters the mean as a rate of 0; pedigree-graph's
`ne_unrelated_founders` drops rows with t <= 1. On target rows (all t > 1)
the two agree to 1e-8.
