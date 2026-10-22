# Shared I/O for the oracle scripts. Every script runs as
#   Rscript oracles/<name>.R <in.json> <out.json>
# in.json names a pedigree TSV (id, mother, father, sex, twin; 0 = missing),
# the id file F is wanted for, and pair sets as int32 id files; out.json maps
# each requested output to a float64 file the script wrote, plus versions.
# Bulk numbers go through raw little-endian files, not JSON, so doubles keep
# all 17 digits and a 10^5-pair set stays small.

suppressPackageStartupMessages(library(jsonlite))

oracle_input <- function() {
  args <- commandArgs(TRUE)
  spec <- fromJSON(args[[1]], simplifyVector = TRUE)
  spec$out_json <- args[[2]]
  spec$ped <- utils::read.delim(spec$pedigree, colClasses = "integer")
  spec
}

read_i32 <- function(path) {
  con <- file(path, "rb")
  on.exit(close(con))
  readBin(con, "integer", n = file.size(path) / 4L, size = 4L, endian = "little")
}

write_f64 <- function(x, path) {
  con <- file(path, "wb")
  on.exit(close(con))
  writeBin(as.double(x), con, size = 8L, endian = "little")
  path
}

#' Values of matrix `m` (dimnames are ids) at the pairs of `set`.
at_pairs <- function(m, set) {
  first <- as.character(read_i32(set$first))
  second <- as.character(read_i32(set$second))
  m[cbind(match(first, rownames(m)), match(second, colnames(m)))]
}

#' Write each output of `outputs` (name -> double vector) and the versions of `packages`.
oracle_output <- function(spec, outputs, packages) {
  paths <- list()
  for (name in names(outputs)) {
    paths[[name]] <- write_f64(outputs[[name]], file.path(spec$out_dir, paste0(spec$oracle, ".", sub(":", ".", name), ".f64")))
  }
  versions <- c(R = R.version.string, vapply(packages, function(p) as.character(utils::packageVersion(p)), ""))
  write_json(list(outputs = paths, versions = as.list(versions)), spec$out_json, auto_unbox = TRUE, digits = NA)
}

#' The kinship matrix's value at each requested pair set, and F from its diagonal.
kinship_outputs <- function(spec, phi) {
  out <- list()
  for (name in names(spec$pairs)) out[[paste0("kinship:", name)]] <- at_pairs(phi, spec$pairs[[name]])
  if (isTRUE(spec$want_f)) {
    ids <- as.character(read_i32(spec$f_ids))
    out$F <- 2 * phi[cbind(match(ids, rownames(phi)), match(ids, colnames(phi)))] - 1
  }
  out
}
