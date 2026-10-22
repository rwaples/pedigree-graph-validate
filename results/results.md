# pedigree-graph against other software

Written by `pixi run harness`; do not edit. Every non-PASS row is explained in
[`../differences.md`](../differences.md) or [`../status.md`](../status.md).

**PASS 550 · DIFF 19 · GAP 43 · INFO 54 · SKIP 31 · FAIL 0 · ERROR 0**

Versions: pedigree-graph (Python) 0.13.0, R R version 4.5.3 (2026-03-11), pedigreegraph 0.13.0, kinship2 1.9.6.2, GENLIB 1.1.10, ribd 1.7.2, verbalisr 0.7.2, nadiv 2.18.0, pedigreeTools 0.3, AGHmatrix 3.0.3, purgeR 1.8.3, visPedigree 1.10.1

| case | family | check | reference | status | n | max_abs_diff | tol | wall_s | note |
|---|---|---|---|---|---|---|---|---|---|
| double_first_cousins | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 171 | 0 | 0 | 2.05 |  |
| double_first_cousins | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 171 | 0 | 0 | 2.05 |  |
| double_first_cousins | bindings | F, Python = R | pedigreegraph (R) | PASS | 18 | 0 | 0 | 2.05 |  |
| double_first_cousins | kinship | kinship | kinship2 | PASS | 171 | 0 | 1e-06 | 2.5 | all pairs |
| double_first_cousins | inbreeding | F | kinship2 | PASS | 18 | 0 | 1e-10 | 2.5 |  |
| double_first_cousins | kinship | kinship | ribd | PASS | 171 | 0 | 1e-06 | 2.21 | all pairs |
| double_first_cousins | inbreeding | F | ribd | PASS | 18 | 0 | 1e-10 | 2.21 |  |
| double_first_cousins | kinship | kinship | GENLIB | PASS | 171 | 0 | 1e-06 | 2.81 | all pairs |
| double_first_cousins | inbreeding | F | GENLIB | PASS | 18 | 0 | 1e-10 | 2.81 |  |
| double_first_cousins | kinship | kinship | nadiv | PASS | 171 | 5.55e-17 | 1e-06 | 2.32 | A2PHI; all pairs |
| double_first_cousins | inbreeding | F | nadiv | PASS | 18 | 0 | 1e-10 | 2.32 |  |
| double_first_cousins | kinship | kinship | pedigreeTools | PASS | 171 | 0 | 1e-06 | 1.81 | A2PHI; all pairs |
| double_first_cousins | inbreeding | F | pedigreeTools | PASS | 18 | 0 | 1e-10 | 1.81 |  |
| double_first_cousins | kinship | kinship | AGHmatrix | PASS | 171 | 0 | 1e-06 | 0.707 | A2PHI; all pairs |
| double_first_cousins | inbreeding | F | AGHmatrix | PASS | 18 | 0 | 1e-10 | 0.707 |  |
| double_first_cousins | inbreeding | F | purgeR | PASS | 18 | 0 | 1e-10 | 0.983 |  |
| double_first_cousins | classification | closest category | verbalisr | PASS | 153 | 0 | 0 | 3.15 | VB; all pairs |
| double_first_cousins | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 153 | 0 |  | 3.15 | every pair agrees with the mated-pair definition too |
| double_first_cousins | classification | verbalisr's own first path | verbalisr | INFO | 153 | 0 |  | 3.15 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| double_first_cousins | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| double_first_cousins | classification | relationship_burden per person | verbalisr | PASS | 18 | 0 | 0 |  | VB |
| conventions | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 300 | 0 | 0 | 2.1 |  |
| conventions | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 300 | 0 | 0 | 2.1 |  |
| conventions | bindings | F, Python = R | pedigreegraph (R) | PASS | 24 | 0 | 0 | 2.1 |  |
| conventions | kinship | kinship | kinship2 | PASS | 300 | 0 | 1e-06 | 3.27 | all pairs |
| conventions | inbreeding | F | kinship2 | PASS | 24 | 0 | 1e-10 | 3.27 |  |
| conventions | kinship | kinship | ribd | PASS | 300 | 0 | 1e-06 | 3 | all pairs |
| conventions | inbreeding | F | ribd | PASS | 24 | 0 | 1e-10 | 3 |  |
| conventions | kinship | kinship | GENLIB | PASS | 300 | 0 | 1e-06 | 4.24 | all pairs |
| conventions | inbreeding | F | GENLIB | PASS | 24 | 0 | 1e-10 | 4.24 |  |
| conventions | kinship | kinship | nadiv | PASS | 300 | 5.55e-17 | 1e-06 | 2.71 | A2PHI; all pairs |
| conventions | inbreeding | F | nadiv | PASS | 24 | 0 | 1e-10 | 2.71 |  |
| conventions | kinship | kinship | pedigreeTools | PASS | 300 | 0 | 1e-06 | 2.96 | A2PHI; all pairs |
| conventions | inbreeding | F | pedigreeTools | PASS | 24 | 0 | 1e-10 | 2.96 |  |
| conventions | kinship | kinship | AGHmatrix | PASS | 300 | 0 | 1e-06 | 0.973 | A2PHI; all pairs |
| conventions | inbreeding | F | AGHmatrix | PASS | 24 | 0 | 1e-10 | 0.973 |  |
| conventions | inbreeding | F | purgeR | PASS | 24 | 0 | 1e-10 | 1.39 |  |
| conventions | classification | closest category | verbalisr | PASS | 276 | 0 | 0 | 3.03 | VB; all pairs |
| conventions | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 276 | 1 |  | 3.03 | D1; 23-24: pg 1C, mated pair H1C |
| conventions | classification | verbalisr's own first path | verbalisr | INFO | 276 | 3 |  | 3.03 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| conventions | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| conventions | classification | relationship_burden per person | verbalisr | PASS | 24 | 0 | 0 |  | VB |
| mz_family | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 45 | 0 | 0 | 2.6 |  |
| mz_family | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 45 | 0 | 0 | 2.6 |  |
| mz_family | bindings | F, Python = R | pedigreegraph (R) | PASS | 9 | 0 | 0 | 2.6 |  |
| mz_family | kinship | kinship | kinship2 | PASS | 45 | 0 | 1e-06 | 2.1 | all pairs |
| mz_family | inbreeding | F | kinship2 | PASS | 9 | 0 | 1e-10 | 2.1 |  |
| mz_family | kinship | kinship | ribd | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | inbreeding | F | ribd | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | kinship | kinship | GENLIB | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | inbreeding | F | GENLIB | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | kinship | kinship | nadiv | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | inbreeding | F | nadiv | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | kinship | kinship | pedigreeTools | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | inbreeding | F | pedigreeTools | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | kinship | kinship | AGHmatrix | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | inbreeding | F | AGHmatrix | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | inbreeding | F | purgeR | GAP |  |  |  |  | G1: no MZ twin input |
| mz_family | classification | closest category | verbalisr | GAP |  |  |  |  | G1: no MZ twin input |
| deep_chain | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 3240 | 0 | 0 | 2.53 |  |
| deep_chain | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 3240 | 0 | 0 | 2.53 |  |
| deep_chain | bindings | F, Python = R | pedigreegraph (R) | PASS | 80 | 0 | 0 | 2.53 |  |
| deep_chain | kinship | kinship | kinship2 | PASS | 3240 | 0 | 1e-06 | 2.57 | all pairs |
| deep_chain | inbreeding | F | kinship2 | PASS | 80 | 0 | 1e-10 | 2.57 |  |
| deep_chain | kinship | kinship | ribd | PASS | 3240 | 0 | 1e-06 | 2.53 | all pairs |
| deep_chain | inbreeding | F | ribd | PASS | 80 | 0 | 1e-10 | 2.53 |  |
| deep_chain | kinship | kinship | GENLIB | PASS | 3240 | 0 | 1e-06 | 3.26 | all pairs |
| deep_chain | inbreeding | F | GENLIB | PASS | 80 | 0 | 1e-10 | 3.26 |  |
| deep_chain | kinship | kinship | nadiv | PASS | 3240 | 1.11e-16 | 1e-06 | 1.95 | A2PHI; all pairs |
| deep_chain | inbreeding | F | nadiv | PASS | 80 | 0 | 1e-10 | 1.95 |  |
| deep_chain | kinship | kinship | pedigreeTools | PASS | 3240 | 0 | 1e-06 | 1.8 | A2PHI; all pairs |
| deep_chain | inbreeding | F | pedigreeTools | PASS | 80 | 0 | 1e-10 | 1.8 |  |
| deep_chain | kinship | kinship | AGHmatrix | PASS | 3240 | 0 | 1e-06 | 0.713 | A2PHI; all pairs |
| deep_chain | inbreeding | F | AGHmatrix | PASS | 80 | 0 | 1e-10 | 0.713 |  |
| deep_chain | inbreeding | F | purgeR | PASS | 80 | 0 | 1e-10 | 1.12 |  |
| deep_chain | classification | closest category | verbalisr | PASS | 3160 | 0 | 0 | 131 | VB; all pairs |
| deep_chain | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 3160 | 108 |  | 131 | D1; 20-27: pg 1C1R, mated pair H1C1R; 20-29: pg 1C1R, mated pair H1C1R; 20-32: pg 1C1R, mated pair H1C1R |
| deep_chain | classification | verbalisr's own first path | verbalisr | INFO | 3160 | 196 |  | 131 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| deep_chain | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| deep_chain | classification | relationship_burden per person | verbalisr | PASS | 80 | 0 | 0 |  | VB |
| deep_chain | ne | ne_idf_t1, reference = final_cohort | purgeR | PASS | 1 | 0 | 7.21e-08 | 1.05 | pg 7.208359353, purgeR 7.208359353 |
| deep_chain | ne | fe, reference = final_cohort | purgeR | PASS | 1 | 0 | 2.72e-06 | 1.05 | pg 2.716537488, purgeR 2.716537488 |
| wf_300 | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 45150 | 0 | 0 | 1.27 |  |
| wf_300 | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 45150 | 0 | 0 | 1.27 |  |
| wf_300 | bindings | F, Python = R | pedigreegraph (R) | PASS | 300 | 0 | 0 | 1.27 |  |
| wf_300 | kinship | kinship | kinship2 | PASS | 45150 | 0 | 1e-06 | 1.65 | all pairs |
| wf_300 | inbreeding | F | kinship2 | PASS | 300 | 0 | 1e-10 | 1.65 |  |
| wf_300 | kinship | kinship | ribd | PASS | 45150 | 0 | 1e-06 | 1.65 | all pairs |
| wf_300 | inbreeding | F | ribd | PASS | 300 | 0 | 1e-10 | 1.65 |  |
| wf_300 | kinship | kinship | GENLIB | PASS | 45150 | 0 | 1e-06 | 2.52 | all pairs |
| wf_300 | inbreeding | F | GENLIB | PASS | 300 | 0 | 1e-10 | 2.52 |  |
| wf_300 | kinship | kinship | nadiv | PASS | 45150 | 5.55e-17 | 1e-06 | 1.49 | A2PHI; all pairs |
| wf_300 | inbreeding | F | nadiv | PASS | 300 | 0 | 1e-10 | 1.49 |  |
| wf_300 | kinship | kinship | pedigreeTools | PASS | 45150 | 0 | 1e-06 | 1.5 | A2PHI; all pairs |
| wf_300 | inbreeding | F | pedigreeTools | PASS | 300 | 0 | 1e-10 | 1.5 |  |
| wf_300 | kinship | kinship | AGHmatrix | PASS | 45150 | 0 | 1e-06 | 0.628 | A2PHI; all pairs |
| wf_300 | inbreeding | F | AGHmatrix | PASS | 300 | 0 | 1e-10 | 0.628 |  |
| wf_300 | inbreeding | F | purgeR | PASS | 300 | 0 | 1e-10 | 0.712 |  |
| wf_300 | classification | closest category | verbalisr | PASS | 44850 | 0 | 0 | 73.3 | VB; all pairs |
| wf_300 | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 44850 | 1.84e+03 |  | 73.3 | D1; 121-173: pg 1C, mated pair H1C; 121-209: pg 1C1R, mated pair H1C1R; 121-214: pg 1C1R, mated pair H1C1R |
| wf_300 | classification | verbalisr's own first path | verbalisr | INFO | 44850 | 5.24e+03 |  | 73.3 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| wf_300 | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| wf_300 | classification | relationship_burden per person | verbalisr | PASS | 300 | 0 | 0 |  | VB |
| wf_300 | ne | ne_idf_t1, reference = final_cohort | purgeR | PASS | 1 | 0 | 7.21e-07 | 0.762 | pg 72.05122668, purgeR 72.05122668 |
| wf_300 | ne | fe, reference = final_cohort | purgeR | PASS | 1 | 1.42e-14 | 3.47e-05 | 0.762 | pg 34.70924977, purgeR 34.70924977 |
| deep_wf | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 4.86 |  |
| deep_wf | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 4.86 |  |
| deep_wf | bindings | F, Python = R | pedigreegraph (R) | PASS | 6000 | 0 | 0 | 4.86 |  |
| deep_wf | kinship | kinship | kinship2 | PASS | 202000 | 1.69e-07 | 1e-06 | 5.96 | 100000 uniform + 100000 related + 2000 self pairs |
| deep_wf | inbreeding | F | kinship2 | PASS | 6000 | 4.88e-15 | 1e-10 | 5.96 |  |
| deep_wf | kinship | kinship | ribd | PASS | 202000 | 1.69e-07 | 1e-06 | 9.47 | 100000 uniform + 100000 related + 2000 self pairs |
| deep_wf | inbreeding | F | ribd | PASS | 6000 | 4.88e-15 | 1e-10 | 9.47 |  |
| deep_wf | kinship | kinship | GENLIB | SKIP |  |  |  |  | over the 300 s wall limit |
| deep_wf | inbreeding | F | GENLIB | SKIP |  |  |  |  | over the 300 s wall limit |
| deep_wf | kinship | kinship | nadiv | SKIP |  |  |  |  | over the 300 s wall limit |
| deep_wf | inbreeding | F | nadiv | SKIP |  |  |  |  | over the 300 s wall limit |
| deep_wf | kinship | kinship | pedigreeTools | SKIP |  |  |  |  | over the 300 s wall limit |
| deep_wf | inbreeding | F | pedigreeTools | SKIP |  |  |  |  | over the 300 s wall limit |
| deep_wf | kinship | kinship | AGHmatrix | PASS | 202000 | 1.69e-07 | 1e-06 | 1.69 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| deep_wf | inbreeding | F | AGHmatrix | PASS | 6000 | 4.88e-15 | 1e-10 | 1.69 |  |
| deep_wf | inbreeding | F | purgeR | PASS | 6000 | 4.88e-15 | 1e-10 | 2.2 |  |
| deep_wf | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 42.9 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| deep_wf | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 76 |  | 42.9 | D1; 2302-2306: pg 1C, mated pair H1C; 2762-2775: pg 1C, mated pair H1C; 2372-2373: pg 1C, mated pair H1C |
| deep_wf | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 79 |  | 42.9 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| deep_wf | ne | ne_idf_t1, reference = final_cohort | purgeR | PASS | 1 | 1e-12 | 2e-07 | 3.5 | pg 19.95254716, purgeR 19.95254716 |
| deep_wf | ne | fe, reference = final_cohort | purgeR | PASS | 1 | 8.88e-15 | 8.34e-06 | 3.5 | pg 8.335108209, purgeR 8.335108209 |
| wf_10k | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 3.88 |  |
| wf_10k | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 3.88 |  |
| wf_10k | bindings | F, Python = R | pedigreegraph (R) | PASS | 10000 | 0 | 0 | 3.88 |  |
| wf_10k | kinship | kinship | kinship2 | PASS | 202000 | 0 | 1e-06 | 20.6 | 100000 uniform + 100000 related + 2000 self pairs |
| wf_10k | inbreeding | F | kinship2 | PASS | 10000 | 0 | 1e-10 | 20.6 |  |
| wf_10k | kinship | kinship | ribd | PASS | 202000 | 0 | 1e-06 | 21.3 | 100000 uniform + 100000 related + 2000 self pairs |
| wf_10k | inbreeding | F | ribd | PASS | 10000 | 0 | 1e-10 | 21.3 |  |
| wf_10k | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 33.6 | all pairs of 500 sampled probands |
| wf_10k | inbreeding | F | GENLIB | PASS | 10000 | 0 | 1e-10 | 33.6 |  |
| wf_10k | kinship | kinship | nadiv | PASS | 202000 | 1.11e-16 | 1e-06 | 134 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| wf_10k | inbreeding | F | nadiv | PASS | 10000 | 0 | 1e-10 | 134 |  |
| wf_10k | kinship | kinship | pedigreeTools | PASS | 202000 | 0 | 1e-06 | 26.7 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| wf_10k | inbreeding | F | pedigreeTools | PASS | 10000 | 0 | 1e-10 | 26.7 |  |
| wf_10k | kinship | kinship | AGHmatrix | PASS | 202000 | 0 | 1e-06 | 3.57 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| wf_10k | inbreeding | F | AGHmatrix | PASS | 10000 | 0 | 1e-10 | 3.57 |  |
| wf_10k | inbreeding | F | purgeR | PASS | 10000 | 0 | 1e-10 | 216 |  |
| wf_10k | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 20.5 | VB; 1000 sampled pairs (481 related by pg, stratified) |
| wf_10k | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 84 |  | 20.5 | D1; 7262-7463: pg 1C, mated pair H1C; 5884-5977: pg 1C, mated pair H1C; 5346-5853: pg 1C, mated pair H1C |
| wf_10k | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 157 |  | 20.5 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| wf_10k | ne | ne_idf_t1, reference = final_cohort | purgeR | PASS | 1 | 0 | 1.02e-05 | 222 | pg 1018.651184, purgeR 1018.651184 |
| wf_10k | ne | fe, reference = final_cohort | purgeR | PASS | 1 | 4.55e-13 | 0.0005 | 222 | pg 499.9308186, purgeR 499.9308186 |
| atlas | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 449826 | 0 | 0 | 1.69 |  |
| atlas | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 1.69 |  |
| atlas | bindings | F, Python = R | pedigreegraph (R) | PASS | 948 | 0 | 0 | 1.69 |  |
| atlas | kinship | kinship | kinship2 | PASS | 449826 | 3.73e-08 | 1e-06 | 2.73 | all pairs |
| atlas | inbreeding | F | kinship2 | PASS | 948 | 0 | 1e-10 | 2.73 |  |
| atlas | kinship | kinship | ribd | PASS | 449826 | 3.73e-08 | 1e-06 | 2.23 | all pairs |
| atlas | inbreeding | F | ribd | PASS | 948 | 0 | 1e-10 | 2.23 |  |
| atlas | kinship | kinship | GENLIB | PASS | 125250 | 3.73e-08 | 1e-06 | 70.1 | all pairs of 500 sampled probands |
| atlas | inbreeding | F | GENLIB | PASS | 948 | 0 | 1e-10 | 70.1 |  |
| atlas | kinship | kinship | nadiv | PASS | 449826 | 3.73e-08 | 1e-06 | 2.65 | A2PHI; all pairs |
| atlas | inbreeding | F | nadiv | PASS | 948 | 0 | 1e-10 | 2.65 |  |
| atlas | kinship | kinship | pedigreeTools | PASS | 449826 | 3.73e-08 | 1e-06 | 2.06 | A2PHI; all pairs |
| atlas | inbreeding | F | pedigreeTools | PASS | 948 | 0 | 1e-10 | 2.06 |  |
| atlas | kinship | kinship | AGHmatrix | PASS | 449826 | 3.73e-08 | 1e-06 | 0.643 | A2PHI; all pairs |
| atlas | inbreeding | F | AGHmatrix | PASS | 948 | 0 | 1e-10 | 0.643 |  |
| atlas | inbreeding | F | purgeR | PASS | 948 | 0 | 1e-10 | 0.87 |  |
| atlas | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 56.9 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| atlas | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 77 |  | 56.9 | D1; 476-523: pg 1C, mated pair H1C; 654-689: pg 1C, mated pair H1C; 658-689: pg 1C, mated pair H1C |
| atlas | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 189 |  | 56.9 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| atlas | ne | ne_idf_t1, reference = target: published value | published | INFO |  |  |  |  | 14.01041 (purgeR test_population_parameters.R:74; Heredity 2021 abstract (14)) |
| atlas | ne | ne_idf_t1, reference = all: published value | published | INFO |  |  |  |  | 8.184803 (purgeR test_population_parameters.R:67) |
| atlas | ne | fe, reference = target | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| atlas | ne | fe, reference = target: published value | published | INFO |  |  |  |  | 3.583086 (purgeR test_population_parameters.R:20) |
| atlas | ne | fa, reference = target | purgeR | GAP |  |  |  |  | B2: pedigree-graph has no such estimator |
| atlas | ne | fa, reference = target: published value | published | INFO |  |  |  |  | 3.583086 (purgeR test_population_parameters.R:21) |
| atlas | ne | ne_idf_t1, reference = final_cohort | purgeR | PASS | 1 | 0 | 1.65e-07 | 0.973 | pg 16.54349982, purgeR 16.54349982 |
| atlas | ne | fe, reference = final_cohort | purgeR | PASS | 1 | 8.88e-16 | 3.58e-06 | 0.973 | pg 3.580620381, purgeR 3.580620381 |
| atlas | ne | ne_idf_t1, reference = target | purgeR | PASS | 1 | 0 | 1.4e-07 | 0.973 | pg 14.01041454, purgeR 14.01041454; published 14.01041 |
| atlas | ne | ne_idf_t1, reference = all | purgeR | DIFF | 1 | 0.155 | 8.18e-08 | 0.973 | pg 8.029395279, purgeR 8.184802929; D2; published 8.184803 |
| dama | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 866586 | 0 | 0 | 2.23 |  |
| dama | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 2.23 |  |
| dama | bindings | F, Python = R | pedigreegraph (R) | PASS | 1316 | 0 | 0 | 2.23 |  |
| dama | kinship | kinship | kinship2 | PASS | 866586 | 3.73e-08 | 1e-06 | 3.65 | all pairs |
| dama | inbreeding | F | kinship2 | PASS | 1316 | 0 | 1e-10 | 3.65 |  |
| dama | kinship | kinship | ribd | PASS | 866586 | 3.73e-08 | 1e-06 | 3.78 | all pairs |
| dama | inbreeding | F | ribd | PASS | 1316 | 0 | 1e-10 | 3.78 |  |
| dama | kinship | kinship | GENLIB | PASS | 125250 | 2.98e-08 | 1e-06 | 31.9 | all pairs of 500 sampled probands |
| dama | inbreeding | F | GENLIB | PASS | 1316 | 0 | 1e-10 | 31.9 |  |
| dama | kinship | kinship | nadiv | PASS | 866586 | 3.73e-08 | 1e-06 | 3.81 | A2PHI; all pairs |
| dama | inbreeding | F | nadiv | PASS | 1316 | 0 | 1e-10 | 3.81 |  |
| dama | kinship | kinship | pedigreeTools | PASS | 866586 | 3.73e-08 | 1e-06 | 3.54 | A2PHI; all pairs |
| dama | inbreeding | F | pedigreeTools | PASS | 1316 | 0 | 1e-10 | 3.54 |  |
| dama | kinship | kinship | AGHmatrix | PASS | 866586 | 3.73e-08 | 1e-06 | 1.83 | A2PHI; all pairs |
| dama | inbreeding | F | AGHmatrix | PASS | 1316 | 0 | 1e-10 | 1.83 |  |
| dama | inbreeding | F | purgeR | PASS | 1316 | 0 | 1e-10 | 1.57 |  |
| dama | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 75.7 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| dama | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 116 |  | 75.7 | D1; 486-763: pg 1C, mated pair H1C; 257-300: pg 1C, mated pair H1C; 304-516: pg 1C, mated pair H1C |
| dama | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 275 |  | 75.7 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| dama | ne | ne_idf_t1, reference = target: published value | published | INFO |  |  |  |  | 11.09927 (purgeR vignette; Heredity 2021 abstract (11)) |
| dama | ne | fe, reference = target | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| dama | ne | fe, reference = target: published value | published | INFO |  |  |  |  | 2.61475 (purgeR tutorial vignette, pop_Nancestors table) |
| dama | ne | ne_idf_t1, reference = final_cohort | purgeR | PASS | 1 | 0 | 1.24e-07 | 1.69 | pg 12.37451663, purgeR 12.37451663 |
| dama | ne | fe, reference = final_cohort | purgeR | PASS | 1 | 0 | 2.58e-06 | 1.69 | pg 2.579214689, purgeR 2.579214689 |
| dama | ne | ne_idf_t1, reference = target | purgeR | PASS | 1 | 0 | 1.11e-07 | 1.69 | pg 11.09927429, purgeR 11.09927429; published 11.09927 |
| arrui | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 72390 | 0 | 0 | 1.58 |  |
| arrui | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 72390 | 0 | 0 | 1.58 |  |
| arrui | bindings | F, Python = R | pedigreegraph (R) | PASS | 380 | 0 | 0 | 1.58 |  |
| arrui | kinship | kinship | kinship2 | PASS | 72390 | 0 | 1e-06 | 2.73 | all pairs |
| arrui | inbreeding | F | kinship2 | PASS | 380 | 0 | 1e-10 | 2.73 |  |
| arrui | kinship | kinship | ribd | PASS | 72390 | 0 | 1e-06 | 2.5 | all pairs |
| arrui | inbreeding | F | ribd | PASS | 380 | 0 | 1e-10 | 2.5 |  |
| arrui | kinship | kinship | GENLIB | PASS | 72390 | 0 | 1e-06 | 3.59 | all pairs |
| arrui | inbreeding | F | GENLIB | PASS | 380 | 0 | 1e-10 | 3.59 |  |
| arrui | kinship | kinship | nadiv | PASS | 72390 | 2.22e-16 | 1e-06 | 2.42 | A2PHI; all pairs |
| arrui | inbreeding | F | nadiv | PASS | 380 | 0 | 1e-10 | 2.42 |  |
| arrui | kinship | kinship | pedigreeTools | PASS | 72390 | 0 | 1e-06 | 2 | A2PHI; all pairs |
| arrui | inbreeding | F | pedigreeTools | PASS | 380 | 0 | 1e-10 | 2 |  |
| arrui | kinship | kinship | AGHmatrix | PASS | 72390 | 0 | 1e-06 | 0.747 | A2PHI; all pairs |
| arrui | inbreeding | F | AGHmatrix | PASS | 380 | 0 | 1e-10 | 0.747 |  |
| arrui | inbreeding | F | purgeR | PASS | 380 | 0 | 1e-10 | 1.08 |  |
| arrui | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 58.8 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| arrui | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 146 |  | 58.8 | D1; 173-184: pg 1C, mated pair H1C; 128-143: pg 1C, mated pair H1C; 73-179: pg 1C, mated pair H1C |
| arrui | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 158 |  | 58.8 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| arrui | ne | ne_idf_t1, reference = target: published value | published | INFO |  |  |  |  | 3.83865 (purgeR vignette; Heredity 2021 abstract (4)) |
| arrui | ne | fe, reference = target | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| arrui | ne | fe, reference = target: published value | published | INFO |  |  |  |  | 1.769424 (purgeR tutorial vignette, pop_Nancestors table) |
| arrui | ne | ne_idf_t1, reference = final_cohort | purgeR | PASS | 1 | 0 | 4.73e-08 | 1.21 | pg 4.728673481, purgeR 4.728673481 |
| arrui | ne | fe, reference = final_cohort | purgeR | PASS | 1 | 0 | 1.78e-06 | 1.21 | pg 1.777819976, purgeR 1.777819976 |
| arrui | ne | ne_idf_t1, reference = target | purgeR | PASS | 1 | 0 | 3.84e-08 | 1.21 | pg 3.838646699, purgeR 3.838646699; published 3.83865 |
| dorcas | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 818560 | 0 | 0 | 1.56 |  |
| dorcas | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 1.56 |  |
| dorcas | bindings | F, Python = R | pedigreegraph (R) | PASS | 1279 | 0 | 0 | 1.56 |  |
| dorcas | kinship | kinship | kinship2 | PASS | 818560 | 2.98e-08 | 1e-06 | 4.13 | all pairs |
| dorcas | inbreeding | F | kinship2 | PASS | 1279 | 0 | 1e-10 | 4.13 |  |
| dorcas | kinship | kinship | ribd | PASS | 818560 | 2.98e-08 | 1e-06 | 4.82 | all pairs |
| dorcas | inbreeding | F | ribd | PASS | 1279 | 0 | 1e-10 | 4.82 |  |
| dorcas | kinship | kinship | GENLIB | PASS | 125250 | 2.98e-08 | 1e-06 | 12.7 | all pairs of 500 sampled probands |
| dorcas | inbreeding | F | GENLIB | PASS | 1279 | 0 | 1e-10 | 12.7 |  |
| dorcas | kinship | kinship | nadiv | PASS | 818560 | 2.98e-08 | 1e-06 | 4.07 | A2PHI; all pairs |
| dorcas | inbreeding | F | nadiv | PASS | 1279 | 0 | 1e-10 | 4.07 |  |
| dorcas | kinship | kinship | pedigreeTools | PASS | 818560 | 2.98e-08 | 1e-06 | 4.34 | A2PHI; all pairs |
| dorcas | inbreeding | F | pedigreeTools | PASS | 1279 | 0 | 1e-10 | 4.34 |  |
| dorcas | kinship | kinship | AGHmatrix | PASS | 818560 | 2.98e-08 | 1e-06 | 1.71 | A2PHI; all pairs |
| dorcas | inbreeding | F | AGHmatrix | PASS | 1279 | 0 | 1e-10 | 1.71 |  |
| dorcas | inbreeding | F | purgeR | PASS | 1279 | 0 | 1e-10 | 1.39 |  |
| dorcas | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 16.9 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| dorcas | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 68 |  | 16.9 | D1; 527-581: pg 1C, mated pair H1C; 378-409: pg 1C, mated pair H1C; 335-482: pg 1C, mated pair H1C |
| dorcas | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 220 |  | 16.9 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| dorcas | ne | ne_idf_t1, reference = final_cohort | purgeR | GAP |  |  |  |  | G3: pg gives no estimate (ne_long_term_contributions: 15 rows have exactly one represented parent (first: row 6)) |
| dorcas | ne | fe, reference = final_cohort | purgeR | GAP |  |  |  |  | G3: pg gives no estimate (ne_long_term_contributions: 15 rows have exactly one represented parent (first: row 6)) |
| dorcas | ne | ne_idf_t1, reference = target: published value | published | INFO |  |  |  |  | 39.32125 (purgeR vignette; Heredity 2021 abstract (39)) |
| dorcas | ne | fe, reference = target | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| dorcas | ne | fe, reference = target: published value | published | INFO |  |  |  |  | 13.38647 (purgeR test_population_parameters.R:29) |
| dorcas | ne | fa, reference = target | purgeR | GAP |  |  |  |  | B2: pedigree-graph has no such estimator |
| dorcas | ne | fa, reference = target: published value | published | INFO |  |  |  |  | 12.9906 (purgeR test_population_parameters.R:30) |
| dorcas | ne | ne_idf_t1, reference = target | purgeR | PASS | 1 | 0 | 3.93e-07 | 1.06 | pg 39.32124983, purgeR 39.32124983; published 39.32125 |
| deep_ped | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 2.68 |  |
| deep_ped | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 2.68 |  |
| deep_ped | bindings | F, Python = R | pedigreegraph (R) | PASS | 4399 | 0 | 0 | 2.68 |  |
| deep_ped | kinship | kinship | kinship2 | PASS | 202000 | 0 | 1e-06 | 5.21 | 100000 uniform + 100000 related + 2000 self pairs |
| deep_ped | inbreeding | F | kinship2 | PASS | 4399 | 0 | 1e-10 | 5.21 |  |
| deep_ped | kinship | kinship | ribd | PASS | 202000 | 0 | 1e-06 | 7.66 | 100000 uniform + 100000 related + 2000 self pairs |
| deep_ped | inbreeding | F | ribd | PASS | 4399 | 0 | 1e-10 | 7.66 |  |
| deep_ped | kinship | kinship | GENLIB | SKIP |  |  |  |  | over the 300 s wall limit |
| deep_ped | inbreeding | F | GENLIB | SKIP |  |  |  |  | over the 300 s wall limit |
| deep_ped | kinship | kinship | nadiv | PASS | 202000 | 1.11e-16 | 1e-06 | 23 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| deep_ped | inbreeding | F | nadiv | PASS | 4399 | 0 | 1e-10 | 23 |  |
| deep_ped | kinship | kinship | pedigreeTools | PASS | 202000 | 5.55e-17 | 1e-06 | 19.4 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| deep_ped | inbreeding | F | pedigreeTools | PASS | 4399 | 0 | 1e-10 | 19.4 |  |
| deep_ped | kinship | kinship | AGHmatrix | PASS | 202000 | 0 | 1e-06 | 1.91 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| deep_ped | inbreeding | F | AGHmatrix | PASS | 4399 | 0 | 1e-10 | 1.91 |  |
| deep_ped | inbreeding | F | purgeR | PASS | 4399 | 0 | 1e-10 | 1.55 |  |
| deep_ped | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 21.2 | VB; 1000 sampled pairs (468 related by pg, stratified) |
| deep_ped | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 1000 | 0 |  | 21.2 | every pair agrees with the mated-pair definition too |
| deep_ped | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 289 |  | 21.2 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| deep_ped | ne | ne_idf_t1, reference = final_cohort | purgeR | GAP |  |  |  |  | G3: pg gives no estimate (ne_long_term_contributions: 19 rows have exactly one represented parent (first: row 310)) |
| deep_ped | ne | fe, reference = final_cohort | purgeR | GAP |  |  |  |  | G3: pg gives no estimate (ne_long_term_contributions: 19 rows have exactly one represented parent (first: row 310)) |
| deep_ped | ne | fe, reference = Gen >= max-1 | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| deep_ped | ne | fe, reference = Gen >= max-1: published value | published | INFO |  |  |  |  | 64.73344 (visPedigree vignette, pediv summary) |
| deep_ped | ne | fa, reference = Gen >= max-1 | purgeR | GAP |  |  |  |  | B2: pedigree-graph has no such estimator |
| deep_ped | ne | fa, reference = Gen >= max-1: published value | published | INFO |  |  |  |  | 44.12033 (visPedigree vignette, pediv summary) |
| darwin | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 2016 | 0 | 0 | 2.26 |  |
| darwin | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 2016 | 0 | 0 | 2.26 |  |
| darwin | bindings | F, Python = R | pedigreegraph (R) | PASS | 63 | 0 | 0 | 2.26 |  |
| darwin | kinship | kinship | kinship2 | PASS | 2016 | 0 | 1e-06 | 2.56 | all pairs |
| darwin | inbreeding | F | kinship2 | PASS | 63 | 0 | 1e-10 | 2.56 |  |
| darwin | kinship | kinship | ribd | PASS | 2016 | 0 | 1e-06 | 2.86 | all pairs |
| darwin | inbreeding | F | ribd | PASS | 63 | 0 | 1e-10 | 2.86 |  |
| darwin | kinship | kinship | GENLIB | PASS | 2016 | 0 | 1e-06 | 3.35 | all pairs |
| darwin | inbreeding | F | GENLIB | PASS | 63 | 0 | 1e-10 | 3.35 |  |
| darwin | kinship | kinship | nadiv | PASS | 2016 | 5.55e-17 | 1e-06 | 2.14 | A2PHI; all pairs |
| darwin | inbreeding | F | nadiv | PASS | 63 | 0 | 1e-10 | 2.14 |  |
| darwin | kinship | kinship | pedigreeTools | PASS | 2016 | 5.55e-17 | 1e-06 | 1.82 | A2PHI; all pairs |
| darwin | inbreeding | F | pedigreeTools | PASS | 63 | 0 | 1e-10 | 1.82 |  |
| darwin | kinship | kinship | AGHmatrix | PASS | 2016 | 0 | 1e-06 | 0.706 | A2PHI; all pairs |
| darwin | inbreeding | F | AGHmatrix | PASS | 63 | 0 | 1e-10 | 0.706 |  |
| darwin | inbreeding | F | purgeR | PASS | 63 | 0 | 1e-10 | 0.997 |  |
| darwin | classification | closest category | verbalisr | PASS | 1953 | 0 | 0 | 6.44 | VB; all pairs |
| darwin | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 1953 | 0 |  | 6.44 | every pair agrees with the mated-pair definition too |
| darwin | classification | verbalisr's own first path | verbalisr | INFO | 1953 | 3 |  | 6.44 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| darwin | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| darwin | classification | relationship_burden per person | verbalisr | PASS | 63 | 0 | 0 |  | VB |
| genea140 | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 8.36 |  |
| genea140 | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 8.36 |  |
| genea140 | bindings | F, Python = R | pedigreegraph (R) | PASS | 41523 | 0 | 0 | 8.36 |  |
| genea140 | kinship | kinship | kinship2 | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | inbreeding | F | kinship2 | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | kinship | kinship | ribd | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | inbreeding | F | ribd | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 14.2 | all pairs of 500 sampled probands |
| genea140 | inbreeding | F | GENLIB | PASS | 41523 | 0 | 1e-10 | 14.2 |  |
| genea140 | kinship | kinship | nadiv | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | inbreeding | F | nadiv | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | kinship | kinship | pedigreeTools | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | inbreeding | F | pedigreeTools | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | kinship | kinship | AGHmatrix | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | inbreeding | F | AGHmatrix | SKIP |  |  |  |  | N = 41523 over the dense cap 12000 |
| genea140 | inbreeding | F | purgeR | SKIP |  |  |  |  | over the 300 s wall limit |
| genea140 | classification | closest category | verbalisr | SKIP |  |  |  |  | N = 41523 over the dense cap |
| mrode2 | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 21 | 0 | 0 | 1.75 |  |
| mrode2 | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 21 | 0 | 0 | 1.75 |  |
| mrode2 | bindings | F, Python = R | pedigreegraph (R) | PASS | 6 | 0 | 0 | 1.75 |  |
| mrode2 | kinship | kinship | kinship2 | PASS | 21 | 0 | 1e-06 | 2.51 | all pairs |
| mrode2 | inbreeding | F | kinship2 | PASS | 6 | 0 | 1e-10 | 2.51 |  |
| mrode2 | kinship | kinship | ribd | PASS | 21 | 0 | 1e-06 | 2.72 | all pairs |
| mrode2 | inbreeding | F | ribd | PASS | 6 | 0 | 1e-10 | 2.72 |  |
| mrode2 | kinship | kinship | GENLIB | PASS | 21 | 0 | 1e-06 | 2.65 | all pairs |
| mrode2 | inbreeding | F | GENLIB | PASS | 6 | 0 | 1e-10 | 2.65 |  |
| mrode2 | kinship | kinship | nadiv | PASS | 21 | 5.55e-17 | 1e-06 | 2.22 | A2PHI; all pairs |
| mrode2 | inbreeding | F | nadiv | PASS | 6 | 0 | 1e-10 | 2.22 |  |
| mrode2 | kinship | kinship | pedigreeTools | PASS | 21 | 5.55e-17 | 1e-06 | 2 | A2PHI; all pairs |
| mrode2 | inbreeding | F | pedigreeTools | PASS | 6 | 0 | 1e-10 | 2 |  |
| mrode2 | kinship | kinship | AGHmatrix | PASS | 21 | 0 | 1e-06 | 0.702 | A2PHI; all pairs |
| mrode2 | inbreeding | F | AGHmatrix | PASS | 6 | 0 | 1e-10 | 0.702 |  |
| mrode2 | inbreeding | F | purgeR | PASS | 6 | 0 | 1e-10 | 1.05 |  |
| mrode2 | classification | closest category | verbalisr | PASS | 15 | 0 | 0 | 2.89 | VB; all pairs |
| mrode2 | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 15 | 0 |  | 2.89 | every pair agrees with the mated-pair definition too |
| mrode2 | classification | verbalisr's own first path | verbalisr | INFO | 15 | 1 |  | 2.89 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| mrode2 | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| mrode2 | classification | relationship_burden per person | verbalisr | PASS | 6 | 0 | 0 |  | VB |
| btped | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 541320 | 0 | 0 | 2.43 |  |
| btped | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 2.43 |  |
| btped | bindings | F, Python = R | pedigreegraph (R) | PASS | 1040 | 0 | 0 | 2.43 |  |
| btped | kinship | kinship | kinship2 | PASS | 541320 | 0 | 1e-06 | 3 | all pairs |
| btped | inbreeding | F | kinship2 | PASS | 1040 | 0 | 1e-10 | 3 |  |
| btped | kinship | kinship | ribd | PASS | 541320 | 0 | 1e-06 | 3.06 | all pairs |
| btped | inbreeding | F | ribd | PASS | 1040 | 0 | 1e-10 | 3.06 |  |
| btped | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 2.7 | all pairs of 500 sampled probands |
| btped | inbreeding | F | GENLIB | PASS | 1040 | 0 | 1e-10 | 2.7 |  |
| btped | kinship | kinship | nadiv | PASS | 541320 | 5.55e-17 | 1e-06 | 2.49 | A2PHI; all pairs |
| btped | inbreeding | F | nadiv | PASS | 1040 | 0 | 1e-10 | 2.49 |  |
| btped | kinship | kinship | pedigreeTools | PASS | 541320 | 0 | 1e-06 | 2.77 | A2PHI; all pairs |
| btped | inbreeding | F | pedigreeTools | PASS | 1040 | 0 | 1e-10 | 2.77 |  |
| btped | kinship | kinship | AGHmatrix | PASS | 541320 | 0 | 1e-06 | 0.902 | A2PHI; all pairs |
| btped | inbreeding | F | AGHmatrix | PASS | 1040 | 0 | 1e-10 | 0.902 |  |
| btped | inbreeding | F | purgeR | PASS | 1040 | 0 | 1e-10 | 0.827 |  |
| btped | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 3.56 | VB; 1000 sampled pairs (498 related by pg, stratified) |
| btped | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 1000 | 0 |  | 3.56 | every pair agrees with the mated-pair definition too |
| btped | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 0 |  | 3.56 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| red_deer | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 1.72 |  |
| red_deer | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 1.72 |  |
| red_deer | bindings | F, Python = R | pedigreegraph (R) | PASS | 6048 | 0 | 0 | 1.72 |  |
| red_deer | kinship | kinship | kinship2 | PASS | 202000 | 0 | 1e-06 | 9.11 | 100000 uniform + 100000 related + 2000 self pairs |
| red_deer | inbreeding | F | kinship2 | PASS | 6048 | 0 | 1e-10 | 9.11 |  |
| red_deer | kinship | kinship | ribd | PASS | 202000 | 0 | 1e-06 | 15.2 | 100000 uniform + 100000 related + 2000 self pairs |
| red_deer | inbreeding | F | ribd | PASS | 6048 | 0 | 1e-10 | 15.2 |  |
| red_deer | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 3.2 | all pairs of 500 sampled probands |
| red_deer | inbreeding | F | GENLIB | PASS | 6048 | 0 | 1e-10 | 3.2 |  |
| red_deer | kinship | kinship | nadiv | PASS | 202000 | 2.22e-16 | 1e-06 | 9.76 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| red_deer | inbreeding | F | nadiv | PASS | 6048 | 0 | 1e-10 | 9.76 |  |
| red_deer | kinship | kinship | pedigreeTools | PASS | 202000 | 5.55e-17 | 1e-06 | 7.26 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| red_deer | inbreeding | F | pedigreeTools | PASS | 6048 | 0 | 1e-10 | 7.26 |  |
| red_deer | kinship | kinship | AGHmatrix | PASS | 202000 | 0 | 1e-06 | 2.27 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| red_deer | inbreeding | F | AGHmatrix | PASS | 6048 | 0 | 1e-10 | 2.27 |  |
| red_deer | inbreeding | F | purgeR | PASS | 6048 | 0 | 1e-10 | 1.71 |  |
| red_deer | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 20.4 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| red_deer | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 70 |  | 20.4 | D1; 2848-3313: pg 1C, mated pair H1C; 3265-3494: pg 1C, mated pair H1C; 242-453: pg 1C, mated pair H1C |
| red_deer | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 203 |  | 20.4 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| boichard2 | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 210 | 0 | 0 | 1.41 |  |
| boichard2 | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 210 | 0 | 0 | 1.41 |  |
| boichard2 | bindings | F, Python = R | pedigreegraph (R) | PASS | 20 | 0 | 0 | 1.41 |  |
| boichard2 | kinship | kinship | kinship2 | PASS | 210 | 0 | 1e-06 | 2.76 | all pairs |
| boichard2 | inbreeding | F | kinship2 | PASS | 20 | 0 | 1e-10 | 2.76 |  |
| boichard2 | kinship | kinship | ribd | PASS | 210 | 0 | 1e-06 | 2.68 | all pairs |
| boichard2 | inbreeding | F | ribd | PASS | 20 | 0 | 1e-10 | 2.68 |  |
| boichard2 | kinship | kinship | GENLIB | PASS | 210 | 0 | 1e-06 | 3.31 | all pairs |
| boichard2 | inbreeding | F | GENLIB | PASS | 20 | 0 | 1e-10 | 3.31 |  |
| boichard2 | kinship | kinship | nadiv | PASS | 210 | 5.55e-17 | 1e-06 | 2.26 | A2PHI; all pairs |
| boichard2 | inbreeding | F | nadiv | PASS | 20 | 0 | 1e-10 | 2.26 |  |
| boichard2 | kinship | kinship | pedigreeTools | PASS | 210 | 0 | 1e-06 | 2.18 | A2PHI; all pairs |
| boichard2 | inbreeding | F | pedigreeTools | PASS | 20 | 0 | 1e-10 | 2.18 |  |
| boichard2 | kinship | kinship | AGHmatrix | PASS | 210 | 0 | 1e-06 | 0.737 | A2PHI; all pairs |
| boichard2 | inbreeding | F | AGHmatrix | PASS | 20 | 0 | 1e-10 | 0.737 |  |
| boichard2 | inbreeding | F | purgeR | PASS | 20 | 0 | 1e-10 | 0.904 |  |
| boichard2 | classification | closest category | verbalisr | PASS | 190 | 0 | 0 | 2.24 | VB; all pairs |
| boichard2 | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 190 | 0 |  | 2.24 | every pair agrees with the mated-pair definition too |
| boichard2 | classification | verbalisr's own first path | verbalisr | INFO | 190 | 0 |  | 2.24 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| boichard2 | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| boichard2 | classification | relationship_burden per person | verbalisr | PASS | 20 | 0 | 0 |  | VB |
| boichard2 | ne | fe, reference = generation 3 | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| boichard2 | ne | fe, reference = generation 3: published value | published | INFO |  |  |  |  | 5.6 (Boichard et al. 1997 table II (p. 12); PyPedal pyp_tests.py:121) |
| boichard2 | ne | fa, reference = generation 3 | purgeR | GAP |  |  |  |  | B2: pedigree-graph has no such estimator |
| boichard2 | ne | fa, reference = generation 3: published value | published | INFO |  |  |  |  | 2.94 (Boichard et al. 1997 table II (p. 12); PyPedal pyp_tests.py:166) |
| boichard2 | ne | Ng, reference = generation 3 | purgeR | GAP |  |  |  |  | B3: pedigree-graph has no such estimator |
| boichard2 | ne | Ng, reference = generation 3: published value | published | INFO |  |  |  |  | 2.5 (Boichard et al. 1997 table II (p. 12)) |
| boichard2a | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 105 | 0 | 0 | 1.55 |  |
| boichard2a | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 105 | 0 | 0 | 1.55 |  |
| boichard2a | bindings | F, Python = R | pedigreegraph (R) | PASS | 14 | 0 | 0 | 1.55 |  |
| boichard2a | kinship | kinship | kinship2 | PASS | 105 | 0 | 1e-06 | 2.66 | all pairs |
| boichard2a | inbreeding | F | kinship2 | PASS | 14 | 0 | 1e-10 | 2.66 |  |
| boichard2a | kinship | kinship | ribd | PASS | 105 | 0 | 1e-06 | 2.33 | all pairs |
| boichard2a | inbreeding | F | ribd | PASS | 14 | 0 | 1e-10 | 2.33 |  |
| boichard2a | kinship | kinship | GENLIB | PASS | 105 | 0 | 1e-06 | 3 | all pairs |
| boichard2a | inbreeding | F | GENLIB | PASS | 14 | 0 | 1e-10 | 3 |  |
| boichard2a | kinship | kinship | nadiv | PASS | 105 | 5.55e-17 | 1e-06 | 2.21 | A2PHI; all pairs |
| boichard2a | inbreeding | F | nadiv | PASS | 14 | 0 | 1e-10 | 2.21 |  |
| boichard2a | kinship | kinship | pedigreeTools | PASS | 105 | 0 | 1e-06 | 1.9 | A2PHI; all pairs |
| boichard2a | inbreeding | F | pedigreeTools | PASS | 14 | 0 | 1e-10 | 1.9 |  |
| boichard2a | kinship | kinship | AGHmatrix | PASS | 105 | 0 | 1e-06 | 0.72 | A2PHI; all pairs |
| boichard2a | inbreeding | F | AGHmatrix | PASS | 14 | 0 | 1e-10 | 0.72 |  |
| boichard2a | inbreeding | F | purgeR | PASS | 14 | 0 | 1e-10 | 0.804 |  |
| boichard2a | classification | closest category | verbalisr | PASS | 91 | 0 | 0 | 2.18 | VB; all pairs |
| boichard2a | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 91 | 0 |  | 2.18 | every pair agrees with the mated-pair definition too |
| boichard2a | classification | verbalisr's own first path | verbalisr | INFO | 91 | 0 |  | 2.18 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| boichard2a | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| boichard2a | classification | relationship_burden per person | verbalisr | PASS | 14 | 0 | 0 |  | VB |
| boichard2a | ne | fe, reference = generation 3 | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| boichard2a | ne | fe, reference = generation 3: published value | published | INFO |  |  |  |  | 4.0 (Boichard et al. 1997 table II (p. 12); PyPedal pyp_tests.py:91) |
| boichard2a | ne | fa, reference = generation 3 | purgeR | GAP |  |  |  |  | B2: pedigree-graph has no such estimator |
| boichard2a | ne | fa, reference = generation 3: published value | published | INFO |  |  |  |  | 2.0 (Boichard et al. 1997 table II (p. 12); PyPedal pyp_tests.py:136) |
| boichard2a | ne | Ng, reference = generation 3 | purgeR | GAP |  |  |  |  | B3: pedigree-graph has no such estimator |
| boichard2a | ne | Ng, reference = generation 3: published value | published | INFO |  |  |  |  | 1.8 (Boichard et al. 1997 table II (p. 12)) |
| boichard2b | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 21 | 0 | 0 | 2.14 |  |
| boichard2b | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 21 | 0 | 0 | 2.14 |  |
| boichard2b | bindings | F, Python = R | pedigreegraph (R) | PASS | 6 | 0 | 0 | 2.14 |  |
| boichard2b | kinship | kinship | kinship2 | PASS | 21 | 0 | 1e-06 | 2.47 | all pairs |
| boichard2b | inbreeding | F | kinship2 | PASS | 6 | 0 | 1e-10 | 2.47 |  |
| boichard2b | kinship | kinship | ribd | PASS | 21 | 0 | 1e-06 | 1.97 | all pairs |
| boichard2b | inbreeding | F | ribd | PASS | 6 | 0 | 1e-10 | 1.97 |  |
| boichard2b | kinship | kinship | GENLIB | PASS | 21 | 0 | 1e-06 | 3 | all pairs |
| boichard2b | inbreeding | F | GENLIB | PASS | 6 | 0 | 1e-10 | 3 |  |
| boichard2b | kinship | kinship | nadiv | PASS | 21 | 5.55e-17 | 1e-06 | 1.99 | A2PHI; all pairs |
| boichard2b | inbreeding | F | nadiv | PASS | 6 | 0 | 1e-10 | 1.99 |  |
| boichard2b | kinship | kinship | pedigreeTools | PASS | 21 | 0 | 1e-06 | 2.35 | A2PHI; all pairs |
| boichard2b | inbreeding | F | pedigreeTools | PASS | 6 | 0 | 1e-10 | 2.35 |  |
| boichard2b | kinship | kinship | AGHmatrix | PASS | 21 | 0 | 1e-06 | 0.793 | A2PHI; all pairs |
| boichard2b | inbreeding | F | AGHmatrix | PASS | 6 | 0 | 1e-10 | 0.793 |  |
| boichard2b | inbreeding | F | purgeR | PASS | 6 | 0 | 1e-10 | 1.02 |  |
| boichard2b | classification | closest category | verbalisr | PASS | 15 | 0 | 0 | 2.19 | VB; all pairs |
| boichard2b | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 15 | 0 |  | 2.19 | every pair agrees with the mated-pair definition too |
| boichard2b | classification | verbalisr's own first path | verbalisr | INFO | 15 | 0 |  | 2.19 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| boichard2b | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| boichard2b | classification | relationship_burden per person | verbalisr | PASS | 6 | 0 | 0 |  | VB |
| boichard2b | ne | fe, reference = generation 3 | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| boichard2b | ne | fe, reference = generation 3: published value | published | INFO |  |  |  |  | 2.0 (Boichard et al. 1997 table II (p. 12); PyPedal pyp_tests.py:106) |
| boichard2b | ne | fa, reference = generation 3 | purgeR | GAP |  |  |  |  | B2: pedigree-graph has no such estimator |
| boichard2b | ne | fa, reference = generation 3: published value | published | INFO |  |  |  |  | 2.0 (Boichard et al. 1997 table II (p. 12); PyPedal pyp_tests.py:151) |
| boichard2b | ne | Ng, reference = generation 3 | purgeR | GAP |  |  |  |  | B3: pedigree-graph has no such estimator |
| boichard2b | ne | Ng, reference = generation 3: published value | published | INFO |  |  |  |  | 1.1 (Boichard et al. 1997 table II (p. 12)) |
| ancien_regime | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 2.35 |  |
| ancien_regime | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 2.35 |  |
| ancien_regime | bindings | F, Python = R | pedigreegraph (R) | PASS | 5891 | 0 | 0 | 2.35 |  |
| ancien_regime | kinship | kinship | kinship2 | PASS | 202000 | 0 | 1e-06 | 5.09 | 100000 uniform + 100000 related + 2000 self pairs |
| ancien_regime | inbreeding | F | kinship2 | PASS | 5891 | 0 | 1e-10 | 5.09 |  |
| ancien_regime | kinship | kinship | ribd | PASS | 202000 | 0 | 1e-06 | 7.68 | 100000 uniform + 100000 related + 2000 self pairs |
| ancien_regime | inbreeding | F | ribd | PASS | 5891 | 0 | 1e-10 | 7.68 |  |
| ancien_regime | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 3.57 | all pairs of 500 sampled probands |
| ancien_regime | inbreeding | F | GENLIB | PASS | 5891 | 0 | 1e-10 | 3.57 |  |
| ancien_regime | kinship | kinship | nadiv | PASS | 202000 | 1.11e-16 | 1e-06 | 3.44 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| ancien_regime | inbreeding | F | nadiv | PASS | 5891 | 0 | 1e-10 | 3.44 |  |
| ancien_regime | kinship | kinship | pedigreeTools | PASS | 202000 | 5.55e-17 | 1e-06 | 3.49 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| ancien_regime | inbreeding | F | pedigreeTools | PASS | 5891 | 0 | 1e-10 | 3.49 |  |
| ancien_regime | kinship | kinship | AGHmatrix | PASS | 202000 | 0 | 1e-06 | 1.19 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| ancien_regime | inbreeding | F | AGHmatrix | PASS | 5891 | 0 | 1e-10 | 1.19 |  |
| ancien_regime | inbreeding | F | purgeR | PASS | 5891 | 0 | 1e-10 | 0.745 |  |
| ancien_regime | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 9.66 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| ancien_regime | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 1000 | 0 |  | 9.66 | every pair agrees with the mated-pair definition too |
| ancien_regime | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 27 |  | 9.66 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| soay_ped1 | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 1.44 |  |
| soay_ped1 | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 1.44 |  |
| soay_ped1 | bindings | F, Python = R | pedigreegraph (R) | PASS | 5068 | 0 | 0 | 1.44 |  |
| soay_ped1 | kinship | kinship | kinship2 | PASS | 202000 | 0 | 1e-06 | 4.72 | 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped1 | inbreeding | F | kinship2 | PASS | 5068 | 0 | 1e-10 | 4.72 |  |
| soay_ped1 | kinship | kinship | ribd | PASS | 202000 | 0 | 1e-06 | 8.16 | 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped1 | inbreeding | F | ribd | PASS | 5068 | 0 | 1e-10 | 8.16 |  |
| soay_ped1 | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 2.23 | all pairs of 500 sampled probands |
| soay_ped1 | inbreeding | F | GENLIB | PASS | 5068 | 0 | 1e-10 | 2.23 |  |
| soay_ped1 | kinship | kinship | nadiv | PASS | 202000 | 5.55e-17 | 1e-06 | 2.77 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped1 | inbreeding | F | nadiv | PASS | 5068 | 0 | 1e-10 | 2.77 |  |
| soay_ped1 | kinship | kinship | pedigreeTools | PASS | 202000 | 5.55e-17 | 1e-06 | 2.08 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped1 | inbreeding | F | pedigreeTools | PASS | 5068 | 0 | 1e-10 | 2.08 |  |
| soay_ped1 | kinship | kinship | AGHmatrix | PASS | 202000 | 0 | 1e-06 | 1 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped1 | inbreeding | F | AGHmatrix | PASS | 5068 | 0 | 1e-10 | 1 |  |
| soay_ped1 | inbreeding | F | purgeR | PASS | 5068 | 0 | 1e-10 | 0.737 |  |
| soay_ped1 | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 7.7 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| soay_ped1 | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 52 |  | 7.7 | D1; 2722-3256: pg 1C, mated pair H1C; 2548-3402: pg 1C, mated pair H1C; 3452-3488: pg 1C, mated pair H1C |
| soay_ped1 | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 71 |  | 7.7 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| soay_ped2 | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 2.02 |  |
| soay_ped2 | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 2.02 |  |
| soay_ped2 | bindings | F, Python = R | pedigreegraph (R) | PASS | 6740 | 0 | 0 | 2.02 |  |
| soay_ped2 | kinship | kinship | kinship2 | PASS | 202000 | 0 | 1e-06 | 10.3 | 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped2 | inbreeding | F | kinship2 | PASS | 6740 | 0 | 1e-10 | 10.3 |  |
| soay_ped2 | kinship | kinship | ribd | PASS | 202000 | 0 | 1e-06 | 14.9 | 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped2 | inbreeding | F | ribd | PASS | 6740 | 0 | 1e-10 | 14.9 |  |
| soay_ped2 | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 4.36 | all pairs of 500 sampled probands |
| soay_ped2 | inbreeding | F | GENLIB | PASS | 6740 | 0 | 1e-10 | 4.36 |  |
| soay_ped2 | kinship | kinship | nadiv | PASS | 202000 | 1.11e-16 | 1e-06 | 9.38 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped2 | inbreeding | F | nadiv | PASS | 6740 | 0 | 1e-10 | 9.38 |  |
| soay_ped2 | kinship | kinship | pedigreeTools | PASS | 202000 | 5.55e-17 | 1e-06 | 5.84 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped2 | inbreeding | F | pedigreeTools | PASS | 6740 | 0 | 1e-10 | 5.84 |  |
| soay_ped2 | kinship | kinship | AGHmatrix | PASS | 202000 | 0 | 1e-06 | 2.44 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| soay_ped2 | inbreeding | F | AGHmatrix | PASS | 6740 | 0 | 1e-10 | 2.44 |  |
| soay_ped2 | inbreeding | F | purgeR | PASS | 6740 | 0 | 1e-10 | 1.56 |  |
| soay_ped2 | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 16.1 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| soay_ped2 | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 73 |  | 16.1 | D1; 5464-5841: pg 1C, mated pair H1C; 5044-6069: pg 1C, mated pair H1C; 4921-4956: pg 1C, mated pair H1C |
| soay_ped2 | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 128 |  | 16.1 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| helgeland | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 1.67 |  |
| helgeland | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 1.67 |  |
| helgeland | bindings | F, Python = R | pedigreegraph (R) | PASS | 3556 | 0 | 0 | 1.67 |  |
| helgeland | kinship | kinship | kinship2 | PASS | 202000 | 0 | 1e-06 | 4.78 | 100000 uniform + 100000 related + 2000 self pairs |
| helgeland | inbreeding | F | kinship2 | PASS | 3556 | 0 | 1e-10 | 4.78 |  |
| helgeland | kinship | kinship | ribd | PASS | 202000 | 0 | 1e-06 | 6.5 | 100000 uniform + 100000 related + 2000 self pairs |
| helgeland | inbreeding | F | ribd | PASS | 3556 | 0 | 1e-10 | 6.5 |  |
| helgeland | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 3.86 | all pairs of 500 sampled probands |
| helgeland | inbreeding | F | GENLIB | PASS | 3556 | 0 | 1e-10 | 3.86 |  |
| helgeland | kinship | kinship | nadiv | PASS | 202000 | 2.22e-16 | 1e-06 | 3.31 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| helgeland | inbreeding | F | nadiv | PASS | 3556 | 0 | 1e-10 | 3.31 |  |
| helgeland | kinship | kinship | pedigreeTools | PASS | 202000 | 5.55e-17 | 1e-06 | 2.7 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| helgeland | inbreeding | F | pedigreeTools | PASS | 3556 | 0 | 1e-10 | 2.7 |  |
| helgeland | kinship | kinship | AGHmatrix | PASS | 202000 | 0 | 1e-06 | 1.24 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| helgeland | inbreeding | F | AGHmatrix | PASS | 3556 | 0 | 1e-10 | 1.24 |  |
| helgeland | inbreeding | F | purgeR | PASS | 3556 | 0 | 1e-10 | 1.21 |  |
| helgeland | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 9.67 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| helgeland | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 12 |  | 9.67 | D1; 1182-2642: pg 1C1R, mated pair H1C1R; 1349-1772: pg 1C1R, mated pair H1C1R; 1071-1543: pg 1C1R, mated pair H1C1R |
| helgeland | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 41 |  | 9.67 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| sosp_fitness | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 2.42 |  |
| sosp_fitness | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 2.42 |  |
| sosp_fitness | bindings | F, Python = R | pedigreegraph (R) | PASS | 3062 | 0 | 0 | 2.42 |  |
| sosp_fitness | kinship | kinship | kinship2 | PASS | 202000 | 3.73e-08 | 1e-06 | 4.55 | 100000 uniform + 100000 related + 2000 self pairs |
| sosp_fitness | inbreeding | F | kinship2 | PASS | 3062 | 0 | 1e-10 | 4.55 |  |
| sosp_fitness | kinship | kinship | ribd | PASS | 202000 | 3.73e-08 | 1e-06 | 5.21 | 100000 uniform + 100000 related + 2000 self pairs |
| sosp_fitness | inbreeding | F | ribd | PASS | 3062 | 0 | 1e-10 | 5.21 |  |
| sosp_fitness | kinship | kinship | GENLIB | SKIP |  |  |  |  | over the 300 s wall limit |
| sosp_fitness | inbreeding | F | GENLIB | SKIP |  |  |  |  | over the 300 s wall limit |
| sosp_fitness | kinship | kinship | nadiv | PASS | 202000 | 3.73e-08 | 1e-06 | 10.5 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| sosp_fitness | inbreeding | F | nadiv | PASS | 3062 | 0 | 1e-10 | 10.5 |  |
| sosp_fitness | kinship | kinship | pedigreeTools | PASS | 202000 | 3.73e-08 | 1e-06 | 12.6 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| sosp_fitness | inbreeding | F | pedigreeTools | PASS | 3062 | 0 | 1e-10 | 12.6 |  |
| sosp_fitness | kinship | kinship | AGHmatrix | PASS | 202000 | 3.73e-08 | 1e-06 | 1.09 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| sosp_fitness | inbreeding | F | AGHmatrix | PASS | 3062 | 0 | 1e-10 | 1.09 |  |
| sosp_fitness | inbreeding | F | purgeR | PASS | 3062 | 0 | 1e-10 | 1.11 |  |
| sosp_fitness | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 25.5 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| sosp_fitness | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 35 |  | 25.5 | D1; 141-674: pg 1C, mated pair H1C; 2903-3059: pg 1C1R, mated pair H1C1R; 150-758: pg 1C1R, mated pair H1C1R |
| sosp_fitness | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 217 |  | 25.5 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| black_robin | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 909226 | 0 | 0 | 1.27 |  |
| black_robin | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 1.27 |  |
| black_robin | bindings | F, Python = R | pedigreegraph (R) | PASS | 1348 | 0 | 0 | 1.27 |  |
| black_robin | kinship | kinship | kinship2 | PASS | 909226 | 0 | 1e-06 | 2.45 | all pairs |
| black_robin | inbreeding | F | kinship2 | PASS | 1348 | 0 | 1e-10 | 2.45 |  |
| black_robin | kinship | kinship | ribd | SKIP |  |  |  |  | it refuses the input: ids 18, 19 are recorded as both a mother and a father |
| black_robin | inbreeding | F | ribd | SKIP |  |  |  |  | it refuses the input: ids 18, 19 are recorded as both a mother and a father |
| black_robin | kinship | kinship | GENLIB | SKIP |  |  |  |  | it refuses the input: ids 18, 19 are recorded as both a mother and a father |
| black_robin | inbreeding | F | GENLIB | SKIP |  |  |  |  | it refuses the input: ids 18, 19 are recorded as both a mother and a father |
| black_robin | kinship | kinship | nadiv | PASS | 909226 | 1.11e-16 | 1e-06 | 2.33 | A2PHI; all pairs |
| black_robin | inbreeding | F | nadiv | PASS | 1348 | 0 | 1e-10 | 2.33 |  |
| black_robin | kinship | kinship | pedigreeTools | PASS | 909226 | 0 | 1e-06 | 2.38 | A2PHI; all pairs |
| black_robin | inbreeding | F | pedigreeTools | PASS | 1348 | 0 | 1e-10 | 2.38 |  |
| black_robin | kinship | kinship | AGHmatrix | PASS | 909226 | 0 | 1e-06 | 1.08 | A2PHI; all pairs |
| black_robin | inbreeding | F | AGHmatrix | PASS | 1348 | 0 | 1e-10 | 1.08 |  |
| black_robin | inbreeding | F | purgeR | PASS | 1348 | 0 | 1e-10 | 0.811 |  |
| black_robin | classification | closest category | verbalisr | SKIP |  |  |  |  | it refuses the input: ids 18, 19 are recorded as both a mother and a father |
| scrub_jay | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 241860 | 0 | 0 | 1.45 |  |
| scrub_jay | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 1.45 |  |
| scrub_jay | bindings | F, Python = R | pedigreegraph (R) | PASS | 695 | 0 | 0 | 1.45 |  |
| scrub_jay | kinship | kinship | kinship2 | PASS | 241860 | 0 | 1e-06 | 2.98 | all pairs |
| scrub_jay | inbreeding | F | kinship2 | PASS | 695 | 0 | 1e-10 | 2.98 |  |
| scrub_jay | kinship | kinship | ribd | PASS | 241860 | 0 | 1e-06 | 3.01 | all pairs |
| scrub_jay | inbreeding | F | ribd | PASS | 695 | 0 | 1e-10 | 3.01 |  |
| scrub_jay | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 3.36 | all pairs of 500 sampled probands |
| scrub_jay | inbreeding | F | GENLIB | PASS | 695 | 0 | 1e-10 | 3.36 |  |
| scrub_jay | kinship | kinship | nadiv | PASS | 241860 | 1.11e-16 | 1e-06 | 2.63 | A2PHI; all pairs |
| scrub_jay | inbreeding | F | nadiv | PASS | 695 | 0 | 1e-10 | 2.63 |  |
| scrub_jay | kinship | kinship | pedigreeTools | PASS | 241860 | 5.55e-17 | 1e-06 | 2.01 | A2PHI; all pairs |
| scrub_jay | inbreeding | F | pedigreeTools | PASS | 695 | 0 | 1e-10 | 2.01 |  |
| scrub_jay | kinship | kinship | AGHmatrix | PASS | 241860 | 0 | 1e-06 | 0.779 | A2PHI; all pairs |
| scrub_jay | inbreeding | F | AGHmatrix | PASS | 695 | 0 | 1e-10 | 0.779 |  |
| scrub_jay | inbreeding | F | purgeR | PASS | 695 | 0 | 1e-10 | 0.992 |  |
| scrub_jay | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 6.06 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| scrub_jay | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 3 |  | 6.06 | D1; 72-506: pg 1C1R, mated pair H1C1R; 96-667: pg 1C2R, mated pair None; 257-539: pg 2C, mated pair None |
| scrub_jay | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 99 |  | 6.06 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| scrub_jay | ne | share of founder ancestry from RLS-K + WSA-K, reference = 2017 population | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| scrub_jay | ne | share of founder ancestry from RLS-K + WSA-K, reference = 2017 population: published value | published | INFO |  |  |  |  | 0.32 (Linderoth et al. 2025, Results; Dryad T_IE_20230512_2017_pop_contribution.pedstat1 gives 0.3223) |
| scrub_jay | ne | mean share from RLS-K + WSA-K, reference = 2008-2022 | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| scrub_jay | ne | mean share from RLS-K + WSA-K, reference = 2008-2022: published value | published | INFO |  |  |  |  | 0.24 (Linderoth et al. 2025, Results; the deposited pedstat1 files give 0.2379 (SD 0.0645)) |
| scrub_jay | ne | founders contributing, reference = 2022 cohort | purgeR | GAP |  |  |  |  | B1: pedigree-graph has no such estimator |
| scrub_jay | ne | founders contributing, reference = 2022 cohort: published value | published | INFO |  |  |  |  | 24 (Linderoth et al. 2025, Dryad number_contributing_lineages_to_cohorts_cr_ped_20230512.tsv) |
| seychelles_warbler | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 1098903 | 0 | 0 | 1.91 |  |
| seychelles_warbler | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 1.91 |  |
| seychelles_warbler | bindings | F, Python = R | pedigreegraph (R) | PASS | 1482 | 0 | 0 | 1.91 |  |
| seychelles_warbler | kinship | kinship | kinship2 | PASS | 1098903 | 0 | 1e-06 | 3.52 | all pairs |
| seychelles_warbler | inbreeding | F | kinship2 | PASS | 1482 | 0 | 1e-10 | 3.52 |  |
| seychelles_warbler | kinship | kinship | ribd | PASS | 1098903 | 0 | 1e-06 | 3.99 | all pairs |
| seychelles_warbler | inbreeding | F | ribd | PASS | 1482 | 0 | 1e-10 | 3.99 |  |
| seychelles_warbler | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 2.98 | all pairs of 500 sampled probands |
| seychelles_warbler | inbreeding | F | GENLIB | PASS | 1482 | 0 | 1e-10 | 2.98 |  |
| seychelles_warbler | kinship | kinship | nadiv | PASS | 1098903 | 1.11e-16 | 1e-06 | 3.04 | A2PHI; all pairs |
| seychelles_warbler | inbreeding | F | nadiv | PASS | 1482 | 0 | 1e-10 | 3.04 |  |
| seychelles_warbler | kinship | kinship | pedigreeTools | PASS | 1098903 | 5.55e-17 | 1e-06 | 2.39 | A2PHI; all pairs |
| seychelles_warbler | inbreeding | F | pedigreeTools | PASS | 1482 | 0 | 1e-10 | 2.39 |  |
| seychelles_warbler | kinship | kinship | AGHmatrix | PASS | 1098903 | 0 | 1e-06 | 1.35 | A2PHI; all pairs |
| seychelles_warbler | inbreeding | F | AGHmatrix | PASS | 1482 | 0 | 1e-10 | 1.35 |  |
| seychelles_warbler | inbreeding | F | purgeR | PASS | 1482 | 0 | 1e-10 | 0.832 |  |
| seychelles_warbler | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 6.36 | VB; 1000 sampled pairs (484 related by pg, stratified) |
| seychelles_warbler | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 14 |  | 6.36 | D1; 967-1310: pg 1C1R, mated pair H1C1R; 726-822: pg 1C1R, mated pair H1C1R; 369-1085: pg 1C1R, mated pair HGGAv |
| seychelles_warbler | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 60 |  | 6.36 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| arctic_fox | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 31878 | 0 | 0 | 1.3 |  |
| arctic_fox | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 31878 | 0 | 0 | 1.3 |  |
| arctic_fox | bindings | F, Python = R | pedigreegraph (R) | PASS | 252 | 0 | 0 | 1.3 |  |
| arctic_fox | kinship | kinship | kinship2 | PASS | 31878 | 0 | 1e-06 | 2.4 | all pairs |
| arctic_fox | inbreeding | F | kinship2 | PASS | 252 | 0 | 1e-10 | 2.4 |  |
| arctic_fox | kinship | kinship | ribd | PASS | 31878 | 0 | 1e-06 | 2.52 | all pairs |
| arctic_fox | inbreeding | F | ribd | PASS | 252 | 0 | 1e-10 | 2.52 |  |
| arctic_fox | kinship | kinship | GENLIB | PASS | 31878 | 0 | 1e-06 | 3.08 | all pairs |
| arctic_fox | inbreeding | F | GENLIB | PASS | 252 | 0 | 1e-10 | 3.08 |  |
| arctic_fox | kinship | kinship | nadiv | PASS | 31878 | 5.55e-17 | 1e-06 | 1.69 | A2PHI; all pairs |
| arctic_fox | inbreeding | F | nadiv | PASS | 252 | 0 | 1e-10 | 1.69 |  |
| arctic_fox | kinship | kinship | pedigreeTools | PASS | 31878 | 5.55e-17 | 1e-06 | 2.22 | A2PHI; all pairs |
| arctic_fox | inbreeding | F | pedigreeTools | PASS | 252 | 0 | 1e-10 | 2.22 |  |
| arctic_fox | kinship | kinship | AGHmatrix | PASS | 31878 | 0 | 1e-06 | 0.754 | A2PHI; all pairs |
| arctic_fox | inbreeding | F | AGHmatrix | PASS | 252 | 0 | 1e-10 | 0.754 |  |
| arctic_fox | inbreeding | F | purgeR | PASS | 252 | 0 | 1e-10 | 1 |  |
| arctic_fox | classification | closest category | verbalisr | PASS | 31626 | 0 | 0 | 120 | VB; all pairs |
| arctic_fox | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 31626 | 0 |  | 120 | every pair agrees with the mated-pair definition too |
| arctic_fox | classification | verbalisr's own first path | verbalisr | INFO | 31626 | 6 |  | 120 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| arctic_fox | classification | relationship_counts | verbalisr | PASS | 22 | 0 | 0 |  | VB |
| arctic_fox | classification | relationship_burden per person | verbalisr | PASS | 252 | 0 | 0 |  | VB |
| steelhead | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 2.28 |  |
| steelhead | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 2.28 |  |
| steelhead | bindings | F, Python = R | pedigreegraph (R) | PASS | 6177 | 0 | 0 | 2.28 |  |
| steelhead | kinship | kinship | kinship2 | PASS | 202000 | 0 | 1e-06 | 8.35 | 100000 uniform + 100000 related + 2000 self pairs |
| steelhead | inbreeding | F | kinship2 | PASS | 6177 | 0 | 1e-10 | 8.35 |  |
| steelhead | kinship | kinship | ribd | PASS | 202000 | 0 | 1e-06 | 9.41 | 100000 uniform + 100000 related + 2000 self pairs |
| steelhead | inbreeding | F | ribd | PASS | 6177 | 0 | 1e-10 | 9.41 |  |
| steelhead | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 3.8 | all pairs of 500 sampled probands |
| steelhead | inbreeding | F | GENLIB | PASS | 6177 | 0 | 1e-10 | 3.8 |  |
| steelhead | kinship | kinship | nadiv | PASS | 202000 | 5.55e-17 | 1e-06 | 3.52 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| steelhead | inbreeding | F | nadiv | PASS | 6177 | 0 | 1e-10 | 3.52 |  |
| steelhead | kinship | kinship | pedigreeTools | PASS | 202000 | 5.55e-17 | 1e-06 | 3.3 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| steelhead | inbreeding | F | pedigreeTools | PASS | 6177 | 0 | 1e-10 | 3.3 |  |
| steelhead | kinship | kinship | AGHmatrix | PASS | 202000 | 0 | 1e-06 | 1.79 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| steelhead | inbreeding | F | AGHmatrix | PASS | 6177 | 0 | 1e-10 | 1.79 |  |
| steelhead | inbreeding | F | purgeR | PASS | 6177 | 0 | 1e-10 | 1.12 |  |
| steelhead | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 8.65 | VB; 1000 sampled pairs (496 related by pg, stratified) |
| steelhead | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 1000 | 40 |  | 8.65 | D1; 4123-4343: pg 1C, mated pair H1C; 4371-4597: pg 1C, mated pair H1C; 3948-4716: pg 1C, mated pair H1C |
| steelhead | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 40 |  | 8.65 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| peromyscus | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 202000 | 0 | 0 | 6.81 |  |
| peromyscus | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 6.81 |  |
| peromyscus | bindings | F, Python = R | pedigreegraph (R) | PASS | 11483 | 0 | 0 | 6.81 |  |
| peromyscus | kinship | kinship | kinship2 | PASS | 202000 | 4.63e-08 | 1e-06 | 30.1 | 100000 uniform + 100000 related + 2000 self pairs |
| peromyscus | inbreeding | F | kinship2 | PASS | 11483 | 0 | 1e-10 | 30.1 |  |
| peromyscus | kinship | kinship | ribd | SKIP |  |  |  |  | over the 6 GB memory limit |
| peromyscus | inbreeding | F | ribd | SKIP |  |  |  |  | over the 6 GB memory limit |
| peromyscus | kinship | kinship | GENLIB | SKIP |  |  |  |  | over the 300 s wall limit |
| peromyscus | inbreeding | F | GENLIB | SKIP |  |  |  |  | over the 300 s wall limit |
| peromyscus | kinship | kinship | nadiv | PASS | 202000 | 4.63e-08 | 1e-06 | 56.4 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| peromyscus | inbreeding | F | nadiv | PASS | 11483 | 0 | 1e-10 | 56.4 |  |
| peromyscus | kinship | kinship | pedigreeTools | PASS | 202000 | 4.63e-08 | 1e-06 | 43.5 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| peromyscus | inbreeding | F | pedigreeTools | PASS | 11483 | 0 | 1e-10 | 43.5 |  |
| peromyscus | kinship | kinship | AGHmatrix | PASS | 202000 | 4.63e-08 | 1e-06 | 3.52 | A2PHI; 100000 uniform + 100000 related + 2000 self pairs |
| peromyscus | inbreeding | F | AGHmatrix | PASS | 11483 | 0 | 1e-10 | 3.52 |  |
| peromyscus | inbreeding | F | purgeR | PASS | 11483 | 0 | 1e-10 | 2.15 |  |
| peromyscus | classification | closest category | verbalisr | PASS | 1000 | 0 | 0 | 42.7 | VB; 1000 sampled pairs (500 related by pg, stratified) |
| peromyscus | classification | closest category, GLOSSARY mated-pair rule | verbalisr | PASS | 1000 | 0 |  | 42.7 | every pair agrees with the mated-pair definition too |
| peromyscus | classification | verbalisr's own first path | verbalisr | INFO | 1000 | 21 |  | 42.7 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| red_squirrel | bindings | kinship:pairs, Python = R | pedigreegraph (R) | PASS | 431056 | 0 | 0 | 1.13 |  |
| red_squirrel | bindings | kinship:probands, Python = R | pedigreegraph (R) | PASS | 125250 | 0 | 0 | 1.13 |  |
| red_squirrel | bindings | F, Python = R | pedigreegraph (R) | PASS | 928 | 0 | 0 | 1.13 |  |
| red_squirrel | kinship | kinship | kinship2 | PASS | 431056 | 0 | 1e-06 | 1.82 | all pairs |
| red_squirrel | inbreeding | F | kinship2 | PASS | 928 | 0 | 1e-10 | 1.82 |  |
| red_squirrel | kinship | kinship | ribd | PASS | 431056 | 0 | 1e-06 | 1.97 | all pairs |
| red_squirrel | inbreeding | F | ribd | PASS | 928 | 0 | 1e-10 | 1.97 |  |
| red_squirrel | kinship | kinship | GENLIB | PASS | 125250 | 0 | 1e-06 | 1.99 | all pairs of 500 sampled probands |
| red_squirrel | inbreeding | F | GENLIB | PASS | 928 | 0 | 1e-10 | 1.99 |  |
| red_squirrel | kinship | kinship | nadiv | PASS | 431056 | 5.55e-17 | 1e-06 | 1.52 | A2PHI; all pairs |
| red_squirrel | inbreeding | F | nadiv | PASS | 928 | 0 | 1e-10 | 1.52 |  |
| red_squirrel | kinship | kinship | pedigreeTools | PASS | 431056 | 5.55e-17 | 1e-06 | 1.37 | A2PHI; all pairs |
| red_squirrel | inbreeding | F | pedigreeTools | PASS | 928 | 0 | 1e-10 | 1.37 |  |
| red_squirrel | kinship | kinship | AGHmatrix | PASS | 431056 | 0 | 1e-06 | 0.602 | A2PHI; all pairs |
| red_squirrel | inbreeding | F | AGHmatrix | PASS | 928 | 0 | 1e-10 | 0.602 |  |
| red_squirrel | inbreeding | F | purgeR | PASS | 928 | 0 | 1e-10 | 0.602 |  |
| red_squirrel | classification | closest category | verbalisr | PASS | 999 | 0 | 0 | 2.77 | VB; 999 sampled pairs (452 related by pg, stratified) |
| red_squirrel | classification | closest category, GLOSSARY mated-pair rule | verbalisr | DIFF | 999 | 32 |  | 2.77 | D1; 699-872: pg 1C, mated pair H1C; 699-715: pg 1C, mated pair H1C; 744-818: pg 1C, mated pair H1C |
| red_squirrel | classification | verbalisr's own first path | verbalisr | INFO | 999 | 32 |  | 2.77 | pairs whose first verbalisr path names another category than pg's closest one; not scored |
| (all) | ne | ne_individual_delta_f.ne | purgeR, visPedigree | GAP |  |  |  |  | G2: purgeR pop_Ne divides by t - 1 only; checked through ne_unrelated_founders instead |
| (all) | ne | ne_inbreeding | purgeR, visPedigree | GAP |  |  |  |  | G2: no cohort log-regression of mean F in purgeR 1.8.3 or visPedigree 1.10.1 |
| (all) | ne | ne_coancestry | purgeR, visPedigree | GAP |  |  |  |  | G2: visPedigree pedne(method = "coancestry") averages pairwise rates over ECG, a different estimator |
| (all) | ne | ne_variance_family_size | purgeR, visPedigree | GAP |  |  |  |  | G2: no family-size-variance Ne in either package |
| (all) | ne | ne_sex_ratio | purgeR, visPedigree | GAP |  |  |  |  | G2: visPedigree pedne(method = "demographic") counts contributing parents, pg counts cohort members |
| (all) | ne | ne_hill_overlapping | purgeR, visPedigree | GAP |  |  |  |  | G2: no overlapping-generations Hill Ne in either package |
| (all) | ne | ne_group_coancestry | purgeR, visPedigree | GAP |  |  |  |  | G2: visPedigree pediv() MeanCoan is the cohort moment only, not pg's regression Ne |
