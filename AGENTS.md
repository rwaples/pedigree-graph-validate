# pedigree-graph-validate

Checks pedigree-graph's Python and R bindings against the same methods in
other software. Terms are in GLOSSARY.md, decisions in docs/adr/.

- Everything runs through pixi: `pixi run preflight`, `pixi run lint`.
  `pixi.lock` and `oracles.lock` change only on purpose; review their diffs.
- Never copy oracle code (GPL); call it from `oracles/*.R` (ADR 0001).
- A scored reference is an oracle rerun live; a published value is an INFO
  row (ADR 0001).
- Never widen a tolerance to make a row pass.
- Don't commit the local-checkout override in pixi.toml.
- Before reporting, quote `pixi run lint` and `pixi run preflight` with
  their exit codes.
