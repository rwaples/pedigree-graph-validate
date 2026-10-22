# purgeR::ip_F: the inbreeding coefficient Fi of every individual.
source("oracles/_io.R")  # the driver runs every script from the repo root
suppressPackageStartupMessages(library(purgeR))
spec <- oracle_input()
p <- spec$ped
x <- ip_F(data.frame(id = p$id, dam = p$mother, sire = p$father))
oracle_output(spec, list(F = x$Fi[match(read_i32(spec$f_ids), x$id)]), "purgeR")
