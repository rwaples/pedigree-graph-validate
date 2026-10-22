# purgeR on one pedigree, one value per task:
#   ne_idf_t1  pop_Ne(ref, "Fi", "t") with Fi from ip_F and t from pop_t over the
#              whole pedigree, averaged over the reference rows (purgeR divides by t - 1)
#   fe, fa     pop_Nfe / pop_Nae with the reference rows marked
source("oracles/_io.R")  # the driver runs every script from the repo root
suppressPackageStartupMessages(library(purgeR))
spec <- oracle_input()
p <- spec$ped
ped <- data.frame(id = p$id, dam = p$mother, sire = p$father)
ped <- pop_t(ip_F(ped))
out <- list()
for (k in seq_len(nrow(spec$tasks))) {
  task <- spec$tasks[k, ]
  ref <- ped$id %in% read_i32(task$reference)
  out[[task$name]] <- switch(task$stat,
    ne_idf_t1 = pop_Ne(ped[ref, ], "Fi", "t")$Ne,
    fe = pop_Nfe(transform(ped, reference = ref), "reference"),
    fa = pop_Nae(transform(ped, reference = ref), "reference"),
    stop("unknown stat ", task$stat)
  )
}
oracle_output(spec, out, "purgeR")
