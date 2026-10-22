# pedigree-graph against other software

Runs both bindings of [pedigree-graph](https://github.com/rwaples/pedigree-graph)
(the Python wheel and the `pedigreegraph` R package) and compares each result
with the same method in other software (an *oracle*), rerun live on the same
pedigree: kinship2, ribd, verbalisr, GENLIB, nadiv, pedigreeTools, AGHmatrix,
purgeR and visPedigree.

The latest results are in [`results/results.md`](results/results.md); every
row that is not PASS is explained in [`differences.md`](differences.md), and
where each one stands is tracked in [`status.md`](status.md).

## Run it

With [pixi](https://pixi.sh):

```bash
pixi run r-setup     # install the pinned R tarballs into .r-lib/ (a few minutes the first time)
pixi run preflight   # both bindings report the pin; every oracle loads
pixi run harness    # every case; exits 1 on any FAIL or ERROR
pixi run harness --only conventions,wf_300
pixi run verify-inputs
pixi run lint
```

`r-setup` installs the pedigreegraph v0.13.0 source tarball
([`pedigreegraph.pin`](pedigreegraph.pin)) and the CRAN-only oracles
([`oracles.lock`](oracles.lock)), and refuses any tarball whose sha256
differs. kinship2 and GENLIB come from conda-forge. `pixi run lock-oracles`
re-resolves `oracles.lock` from CRAN.

### Checking a local pedigree-graph checkout

1. In `pixi.toml`, replace the `pedigree-graph` entry with
   `pedigree-graph = { path = "../pedigree-graph", editable = true }` and run
   `pixi install`.
2. Build the R tarball in the checkout (`pixi run -e r tools/r_build_tarball.sh`)
   and run `PGV_R_TARBALL=/path/to/pedigreegraph_<ver>.tar.gz pixi run harness`
   (it installs that tarball first; `pixi run preflight` with the variable set
   only checks that everything loads).

Neither binding reports its core revision yet, so under the override the
preflight cannot check that both were built from the same tree.

## What it does

For each case in [`cases.yaml`](cases.yaml), `run_oracles.py`:

1. **Loads the pedigree**: a seeded file in `inputs/` (written by
   [`make_inputs.py`](make_inputs.py), sha256-checked), a dataset bundled in
   an R package (purgeR, visPedigree), or a public pedigree pinned in
   [`datasets.yaml`](datasets.yaml) and downloaded into `.cache/` (the
   downloader and readers are copied from pedsum-validate; Dryad files need
   credentials, see `dryad.py`).
2. **Runs both bindings**: Python in-process, R through [`pg_r.R`](pg_r.R).
   They must agree exactly.
3. **Runs the oracles**, one R script each in [`oracles/`](oracles), every
   call under the wall and memory caps of `cases.yaml`'s `budget`. A case over
   a cap gets a SKIP row naming it.
4. **Compares** and writes `results/results.md` and `results/results.tsv`.

| Family | pedigree-graph | Oracles |
|---|---|---|
| Kinship | `pair_kinship` | kinship2, ribd, GENLIB (sampled probands), nadiv, pedigreeTools, AGHmatrix |
| Inbreeding | `inbreeding` | the same, and purgeR `ip_F` |
| Classification | `relationship_pairs`, `relationship_counts`, `relationship_burden` | verbalisr: every path of each pair, mapped to registry categories by pedigree-graph's own rules (`conversions.py`) |
| Ne and lineage | `ne_individual_delta_f`, `ne_long_term_contributions` | purgeR `pop_Ne`, `pop_Nfe`; the other estimators are GAP rows |

Published values (purgeR's tests and vignettes, papers) are INFO rows beside
the live oracle row; they are never scored (ADR 0001).

## License

MIT. The oracles are GPL; they are installed and called at run time, never
copied here.
