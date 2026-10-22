# AGHmatrix::Amatrix at ploidy 2 (A = 2 kinship; conversion A2PHI); F from its diagonal.
source("oracles/_io.R")  # the driver runs every script from the repo root
suppressPackageStartupMessages(library(AGHmatrix))
spec <- oracle_input()
p <- spec$ped
A <- Amatrix(data.frame(ind = p$id, p1 = p$father, p2 = p$mother), ploidy = 2)
dimnames(A) <- list(as.character(p$id), as.character(p$id))
out <- list()
for (name in names(spec$pairs)) out[[paste0("kinship:", name)]] <- at_pairs(A, spec$pairs[[name]])
if (isTRUE(spec$want_f)) {
  ids <- as.character(read_i32(spec$f_ids))
  out$F <- A[cbind(match(ids, rownames(A)), match(ids, colnames(A)))] - 1
}
oracle_output(spec, out, "AGHmatrix")
