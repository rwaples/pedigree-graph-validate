# pedigreeTools::getA (A = 2 kinship; conversion A2PHI) and pedigreeTools::inbreeding.
source("oracles/_io.R")  # the driver runs every script from the repo root
suppressPackageStartupMessages(library(pedigreeTools))
spec <- oracle_input()
p <- spec$ped
x <- pedigree(sire = ifelse(p$father == 0, NA, p$father), dam = ifelse(p$mother == 0, NA, p$mother), label = p$id)
out <- list()
if (length(spec$pairs) > 0) {
  A <- as.matrix(getA(x))
  for (name in names(spec$pairs)) out[[paste0("kinship:", name)]] <- at_pairs(A, spec$pairs[[name]])
}
if (isTRUE(spec$want_f)) out$F <- unname(inbreeding(x)[match(read_i32(spec$f_ids), p$id)])
oracle_output(spec, out, "pedigreeTools")
