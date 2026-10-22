# ribd::kinship and ribd::inbreeding on a pedtools ped (complete parents: phantoms filled by the driver).
source("oracles/_io.R")  # the driver runs every script from the repo root
suppressPackageStartupMessages({library(pedtools); library(ribd)})
spec <- oracle_input()
p <- spec$ped
x <- ped(id = p$id, fid = p$father, mid = p$mother, sex = p$sex, validate = TRUE, detectLoops = FALSE)
phi <- kinship(x)
out <- kinship_outputs(spec, phi)
if (isTRUE(spec$want_f)) out$F <- unname(inbreeding(x, ids = as.character(read_i32(spec$f_ids))))
oracle_output(spec, out, c("ribd", "pedtools"))
