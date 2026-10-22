# kinship2::kinship: Lange's recursion, a dense kinship matrix; MZ twins via a pedigree relation.
source("oracles/_io.R")  # the driver runs every script from the repo root
suppressPackageStartupMessages(library(kinship2))
spec <- oracle_input()
p <- spec$ped
twins <- p[p$twin > 0 & p$id < p$twin, c("id", "twin")]
if (nrow(twins) > 0) {
  ped <- pedigree(p$id, p$father, p$mother, p$sex, relation = cbind(twins$id, twins$twin, 1L))
  phi <- as.matrix(kinship(ped))
} else {
  phi <- as.matrix(kinship(p$id, p$father, p$mother, p$sex))
}
oracle_output(spec, kinship_outputs(spec, phi), "kinship2")
