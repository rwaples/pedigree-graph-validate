# Status of every non-PASS row

| id | rows | status | next |
|---|---|---|---|
| G1 | MZ twin cases against every oracle but kinship2 | accepted | the other oracles take no MZ input |
| D1 | genealogical mated-pair rule vs pedigree-graph's path counts | accepted | intended, pedigree-graph ADR 0018 (#47, #48) |
| D2 | atlas Ne_iΔF over all rows | accepted | pg drops rows with t <= 1; purgeR counts them (moved from pedsum-validate) |
| B1, B2, B3 | fe (any reference but pg's final cohort), fa, Ng | open | pg has no such estimator; published values kept as INFO rows |
| G2 | pg Ne estimators with no oracle | open | see cases.yaml `ne_gaps` |
| G3 | Ne checks where pg returns no estimate | accepted | pg's no_estimate_code is in the row |
| S1 | SKIP: over a Cap (dense N, wall time, memory) | accepted | the caps are `budget` in cases.yaml; the row names the cap it hit |
| S2 | SKIP: black_robin, one `input`/`build` row | accepted | ids 18 and 19 are each recorded as a mother and as a father. From 0.15.0 pedigree-graph refuses that at construction (`parent_in_both_roles`, pedigree-graph #58), as ribd, GENLIB and verbalisr already did, so no oracle checks the case. cases.yaml names the code as `refuse`; any other refusal is an ERROR row |
