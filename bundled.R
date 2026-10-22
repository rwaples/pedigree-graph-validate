# Export a pedigree bundled with an R package as raw TSV, for pedigrees.normalize():
#   Rscript bundled.R <package> <dataset> <out.tsv>
# Columns id, mother, father, sex as the package stores them (any id type,
# its own missing-parent token), plus any of target and yob it has.
args <- commandArgs(TRUE)
e <- new.env()
data(list = args[[2]], package = args[[1]], envir = e)
x <- as.data.frame(e[[args[[2]]]])
pick <- function(...) {
  for (name in c(...)) if (name %in% names(x)) return(as.character(x[[name]]))
  stop("no column among ", paste(c(...), collapse = ", "))
}
out <- data.frame(
  id = pick("id", "Ind"), mother = pick("dam", "Dam"), father = pick("sire", "Sire"),
  sex = if (any(c("sex", "Sex") %in% names(x))) pick("sex", "Sex") else ""
)
for (col in c("target", "yob")) if (col %in% names(x)) out[[col]] <- as.character(x[[col]])
utils::write.table(out, args[[3]], sep = "\t", quote = FALSE, row.names = FALSE, na = "")
