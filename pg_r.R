# The pedigreegraph R binding on one case: pair_kinship at each pair set and inbreeding.
# Same interface as the oracles: Rscript pg_r.R <in.json> <out.json>, run from the repo root.
source("oracles/_io.R")
suppressPackageStartupMessages(library(pedigreegraph))
spec <- oracle_input()
p <- spec$ped
na0 <- function(x) ifelse(x == 0L, NA_integer_, x)
pg <- pedigree_graph(
  data.frame(id = p$id, mother = na0(p$mother), father = na0(p$father), twin = na0(p$twin), sex = p$sex),
  sex_encoding = "plink"
)
out <- list()
for (name in names(spec$pairs)) {
  set <- spec$pairs[[name]]
  out[[paste0("kinship:", name)]] <- pair_kinship(pg, match(read_i32(set$first), p$id), match(read_i32(set$second), p$id))
}
if (isTRUE(spec$want_f)) out$F <- inbreeding(pg)[match(read_i32(spec$f_ids), p$id)]
oracle_output(spec, out, "pedigreegraph")
