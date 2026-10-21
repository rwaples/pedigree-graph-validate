# pedigree-graph against other software

Runs both bindings of [pedigree-graph](https://github.com/rwaples/pedigree-graph)
(the Python wheel and the `pedigreegraph` R package) and compares each result
with the same method in other software (an *oracle*), rerun live on the same
pedigree: kinship2, ribd, verbalisr, GENLIB, nadiv, pedigreeTools, AGHmatrix,
purgeR and visPedigree.

Status: scaffold. The environment and the preflight work; the cases are not
written yet.

## Run it

With [pixi](https://pixi.sh):

```bash
pixi run r-setup     # install the pinned R tarballs into .r-lib/ (a few minutes the first time)
pixi run preflight   # both bindings report the pin; every oracle loads
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
   and run `PGV_R_TARBALL=/path/to/pedigreegraph_<ver>.tar.gz pixi run preflight`.

Neither binding reports its core revision yet, so under the override the
preflight cannot check that both were built from the same tree.

## License

MIT. The oracles are GPL; they are installed and called at run time, never
copied here.
