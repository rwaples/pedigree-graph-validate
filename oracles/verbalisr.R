# verbalisr::verbalise: every pedigree path between each pair of the "classify" set.
# Writes <out_dir>/verbalisr.paths.json: one entry per pair, a list of paths
# [l1, l2, full, ancestors...] (l1, l2 meioses from the ancestor(s) down to the
# pair's first and second member; full 1, 0, or -1 for a lineal path). A pair
# whose ribd kinship is 0 gets no paths without calling verbalise, which would
# find none (verbalisr R/verbalise.R returns "unrelated" when kinship is 0).
#
# verbalise() lists every path, which explodes in deep inbred pedigrees. Every
# pedigree-graph category is at most 5 meioses up from either member (G3GP,
# G3Av), so each pair is run on the sub-pedigree of its ancestors at most 5
# meioses up: a node at most 4 up keeps both parents, a node 5 up becomes a
# founder. Every path with both legs at most 5 meioses long survives intact,
# with the parents verbalisr's full/half test reads; longer paths, which map
# to no category, are cut.
source("oracles/_io.R")  # the driver runs every script from the repo root
suppressPackageStartupMessages({library(pedtools); library(ribd); library(verbalisr)})
spec <- oracle_input()
p <- spec$ped
x <- ped(id = p$id, fid = p$father, mid = p$mother, sex = p$sex, validate = TRUE, detectLoops = FALSE)
phi <- kinship(x)
set <- spec$pairs$classify
first <- as.character(read_i32(set$first))
second <- as.character(read_i32(set$second))
related <- phi[cbind(match(first, rownames(phi)), match(second, colnames(phi)))] > 0
row <- setNames(seq_along(p$id), p$id)
depth_up <- function(start, max_up = 5L) {
  depth <- setNames(0L, start)
  frontier <- start
  for (d in seq_len(max_up)) {
    rows <- row[frontier]
    up <- setdiff(as.character(c(p$mother[rows], p$father[rows])), c("0", names(depth)))
    if (length(up) == 0L) break
    depth[up] <- d
    frontier <- up
  }
  depth
}
window <- function(a, b) {
  da <- depth_up(a)
  db <- depth_up(b)
  keep <- union(names(da), names(db))
  d <- pmin(ifelse(keep %in% names(da), da[keep], 99L), ifelse(keep %in% names(db), db[keep], 99L))
  rows <- row[keep]
  inner <- d <= 4L
  ped(
    id = keep, fid = ifelse(inner, p$father[rows], 0L), mid = ifelse(inner, p$mother[rows], 0L),
    sex = p$sex[rows], validate = FALSE, detectLoops = FALSE
  )
}
paths <- vector("list", length(first))
for (k in which(related)) {
  rel <- verbalise(window(first[[k]], second[[k]]), c(first[[k]], second[[k]]))
  # Related only through ancestors over 5 meioses up: no path survives the window.
  rel <- Filter(function(r) r$type != "unrelated", rel)
  paths[[k]] <- lapply(rel, function(r) {
    full <- if (is.na(r$full)) -1L else as.integer(r$full)
    c(as.integer(r$nSteps), full, as.integer(r$anc))
  })
}
paths <- lapply(paths, function(p) if (is.null(p)) list() else p)
out <- file.path(spec$out_dir, "verbalisr.paths.json")
write_json(paths, out)
versions <- c(R = R.version.string, vapply(c("verbalisr", "ribd", "pedtools"), function(p) as.character(utils::packageVersion(p)), ""))
write_json(list(outputs = structure(list(), names = character(0)), paths = out, n_related = sum(related), versions = as.list(versions)), spec$out_json, auto_unbox = TRUE, digits = NA)
