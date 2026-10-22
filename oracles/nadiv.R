# nadiv::makeA (the relationship matrix A = 2 kinship; conversion A2PHI) and nadiv::makeAinv's f.
source("oracles/_io.R")  # the driver runs every script from the repo root
suppressPackageStartupMessages(library(nadiv))
spec <- oracle_input()
p <- spec$ped
pedigree <- data.frame(id = p$id, dam = ifelse(p$mother == 0, NA, p$mother), sire = ifelse(p$father == 0, NA, p$father))
out <- list()
if (length(spec$pairs) > 0) {
  A <- as.matrix(makeA(pedigree))
  for (name in names(spec$pairs)) out[[paste0("kinship:", name)]] <- at_pairs(A, spec$pairs[[name]])
}
if (isTRUE(spec$want_f)) {
  inv <- makeAinv(pedigree)
  out$F <- unname(inv$f[match(read_i32(spec$f_ids), p$id)])
}
oracle_output(spec, out, "nadiv")
