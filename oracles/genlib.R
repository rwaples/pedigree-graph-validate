# GENLIB::gen.phi (Karigl, among the probands of each pair set) and GENLIB::gen.f.
source("oracles/_io.R")  # the driver runs every script from the repo root
suppressPackageStartupMessages(library(GENLIB))
spec <- oracle_input()
p <- spec$ped
# GENLIB takes only sex 1 or 2; autosomal kinship does not depend on the sex of
# a non-parent, so unknown sex becomes 1 (parents already carry their role's sex).
gen <- gen.genealogy(data.frame(ind = p$id, father = p$father, mother = p$mother, sex = ifelse(p$sex == 0L, 1L, p$sex)))
out <- list()
for (name in names(spec$pairs)) {
  set <- spec$pairs[[name]]
  pro <- sort(unique(c(read_i32(set$first), read_i32(set$second))))
  phi <- gen.phi(gen, pro = pro)
  out[[paste0("kinship:", name)]] <- at_pairs(phi, set)
}
if (isTRUE(spec$want_f)) {
  ids <- read_i32(spec$f_ids)
  f <- gen.f(gen, pro = ids)
  out$F <- unname(as.numeric(f[as.character(ids)]))
}
oracle_output(spec, out, "GENLIB")
