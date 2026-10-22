"""Download, read and convert the public pedigrees of datasets.yaml.

Copied from pedsum-validate (run_published.py at 2682fb7: fetch, the format
readers, the A-inverse pedigree rebuild, parent overrides) and owned here
(plan D10); `raw_table` replaces its `convert`, handing pedigrees.normalize()
the id, mother, father, sex and target columns.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import tarfile
import urllib.request
import zipfile
from typing import TYPE_CHECKING, Any

import numpy as np

import dryad  # dryad.py, next to this module

if TYPE_CHECKING:
    from pathlib import Path


def fetch(spec: dict[str, Any], cache: Path) -> Path:
    """Download the dataset's ``url`` or ``dryad_file`` into ``cache`` once and verify its SHA-256."""
    sha256 = spec["sha256"]
    if "dryad_file" in spec:
        source, name = f"Dryad file {spec['dryad_file']}", f"dryad-{spec['dryad_file']}"
    else:
        source, name = spec["url"], spec["url"].rsplit("/", 1)[-1]
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / f"{sha256[:12]}-{name}"
    if not path.exists():
        if "dryad_file" in spec:
            data = dryad.download(spec["dryad_file"])
        else:
            with urllib.request.urlopen(spec["url"], timeout=60) as resp:
                data = resp.read()
        path.write_bytes(data)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != sha256:
        path.unlink()
        raise RuntimeError(f"{source}: SHA-256 {digest} does not match the pinned {sha256}")
    return path


def _read_bytes(path: Path, spec: dict[str, Any]) -> bytes:
    """Bytes of the source file: ``member`` of a tar or zip archive if given, gunzipped if gzipped."""
    if "member" in spec and zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            data = zf.read(spec["member"])
    elif "member" in spec:
        with tarfile.open(path) as tar:
            fh = tar.extractfile(spec["member"])
            if fh is None:
                raise ValueError(f"{path}: {spec['member']!r} is not a regular file")
            data = fh.read()
    else:
        data = path.read_bytes()
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data


def _read_text(path: Path, spec: dict[str, Any]) -> str:
    return _read_bytes(path, spec).decode()


def load_table(path: Path, spec: dict[str, Any]) -> dict[str, list[str | None]]:
    """Read the source table into string columns (None for R NA)."""
    fmt = spec.get("format")
    if fmt in ("whitespace_table", "csv", "tsv"):
        # `names` gives the columns of a file without a header row; `#` lines are comments.
        lines = [ln for ln in _read_text(path, spec).splitlines() if ln.strip() and not ln.startswith("#")]
        if fmt == "whitespace_table":
            rows = [ln.split() for ln in lines]
        else:  # csv, or tsv: tab-separated, keeping the empty fields that whitespace_table collapses
            rows = list(csv.reader(lines, delimiter="\t" if fmt == "tsv" else ","))
        header, body = (spec["names"], rows) if "names" in spec else (rows[0], rows[1:])
        cols = {name: [r[i] for r in body] for i, name in enumerate(header)}
        return {k: [None if v == "NA" else v for v in vals] for k, vals in cols.items()}
    if fmt == "iur_txt":
        return _load_iur(_read_text(path, spec))
    if fmt == "xlsx":
        return _load_xlsx(path, spec)
    if fmt == "ainv_list":
        return _pedigree_from_ainv(_ainv_triplets(path, spec))
    import rdata  # optional dependency; only the .rda inputs need it

    frame = rdata.read_rda(path)[spec["object"]]
    out: dict[str, list[str | None]] = {}
    for name in frame.columns:
        values = frame[name].astype(object).tolist()
        out[str(name)] = [None if _is_na(v) else _as_token(v) for v in values]
    return out


def _load_xlsx(path: Path, spec: dict[str, Any]) -> dict[str, list[str | None]]:
    """One worksheet of an Excel workbook: ``sheet`` by name, else the first. Blank rows are skipped.

    A repeated header (such as the two allele columns of a marker) keeps its first column.
    """
    import openpyxl  # optional dependency; only the .xlsx inputs need it

    # Read from memory: openpyxl checks the file extension, which cached files lack.
    book = openpyxl.load_workbook(io.BytesIO(_read_bytes(path, spec)), read_only=True, data_only=True)
    sheet = book[spec["sheet"]] if "sheet" in spec else book.worksheets[0]
    rows = [r for r in sheet.iter_rows(values_only=True) if any(v is not None for v in r)]
    cols: dict[str, list[str | None]] = {}
    for i, name in enumerate(str(h) for h in rows[0]):
        if name not in cols:
            cols[name] = [None if i >= len(r) or r[i] is None or r[i] == "NA" else _as_token(r[i]) for r in rows[1:]]
    return cols


def _ainv_triplets(path: Path, spec: dict[str, Any]) -> tuple[list[str], np.ndarray, np.ndarray, np.ndarray]:
    """Lower-triangle triplets (0-based row, column, value) of an inverse relationship matrix, and the row ids.

    ``format: ainv_rdata`` reads ASReml-R ``asreml.Ainverse`` output saved as
    ``.RData`` (``object`` names the data frame; row ids are in its
    ``rowNames`` attribute). ``ainv_list`` reads a whitespace text list
    ``row column value`` after a header line; its rows are numbered 1..n and
    those numbers are the ids.
    """
    if spec.get("format") == "ainv_rdata":
        import rdata  # optional dependency

        parsed = rdata.parser.parse_file(path)
        frame = rdata.conversion.convert(parsed)[spec["object"]]
        node, names = parsed.object.value[0].attributes, None
        while node is not None and node.info.type.name == "LIST":
            if node.tag.value.value == b"rowNames":
                names = [x.value.decode() for x in node.value[0].value]
            node = node.value[1] if len(node.value) > 1 else None
        if names is None:
            raise ValueError(f"{path}: no rowNames attribute")
        r, c, v = (frame[k].to_numpy() for k in frame.columns[:3])
    else:
        lines = [ln.split() for ln in _read_text(path, spec).splitlines()[1:] if ln.strip()]
        r, c, v = (np.array([float(x[i]) for x in lines]) for i in range(3))
        names = [str(i) for i in range(1, int(r.max()) + 1)]
    return names, r.astype(np.int64) - 1, c.astype(np.int64) - 1, v.astype(np.float64)


def _pedigree_from_ainv(triplets: tuple[list[str], np.ndarray, np.ndarray, np.ndarray]) -> dict[str, list[str | None]]:
    """Recover the parents behind a Henderson inverse relationship matrix by peeling rows from the last.

    A^-1 = sum_i b_i c_i c_i^T, with c_i = e_i - (e_dam + e_sire)/2 over i's
    known parents. When every parent precedes its offspring, the off-diagonal
    entries left in row i after peeling the rows below it are i's parents,
    each equal to -b_i/2. The matrix is refused if that does not hold or
    anything is left over.

    A^-1 does not say which parent is the dam, so parents are split by
    2-colouring the mate graph. F does not depend on which parent is called
    the dam: the tabular method treats the two parents symmetrically.
    Returns columns ``id, mother, father``; sex is left to ``validate``,
    which infers it from the parents' roles.
    """
    names, r, c, v = triplets
    n = len(names)
    m: list[dict[int, float]] = [{} for _ in range(n)]
    for i, j, x in zip(r.tolist(), c.tolist(), v.tolist(), strict=True):
        m[i][j] = m[i].get(j, 0.0) + x
        if i != j:
            m[j][i] = m[j].get(i, 0.0) + x
    parents: list[list[int]] = [[] for _ in range(n)]
    for i in range(n - 1, -1, -1):
        b = m[i].get(i, 0.0)
        par = sorted(j for j, x in m[i].items() if j != i and abs(x) > 1e-8)
        if any(j > i for j in par) or len(par) > 2 or any(abs(m[i][j] + b / 2) > 1e-7 for j in par):
            raise ValueError(f"A-inverse row {names[i]!r} is not a parent-before-offspring Henderson row")
        parents[i] = par
        coef = {i: 1.0, **dict.fromkeys(par, -0.5)}
        for x, cx in coef.items():
            for y, cy in coef.items():
                m[x][y] = m[x].get(y, 0.0) - b * cx * cy
    if max((abs(x) for row in m for x in row.values()), default=0.0) > 1e-8:
        raise ValueError("A-inverse is not fully explained by the recovered parents")
    mates: dict[int, set[int]] = {}
    for par in parents:
        if len(par) == 2:
            mates.setdefault(par[0], set()).add(par[1])
            mates.setdefault(par[1], set()).add(par[0])
    colour: dict[int, int] = {}
    for start in mates:
        if start in colour:
            continue
        colour[start], stack = 0, [start]
        while stack:
            x = stack.pop()
            for y in mates[x]:
                if y not in colour:
                    colour[y] = 1 - colour[x]
                    stack.append(y)
                elif colour[y] == colour[x]:
                    raise ValueError(f"{names[x]} and {names[y]} are mates but must share a sex")
    mother: list[str | None] = []
    father: list[str | None] = []
    for par in parents:
        if len(par) == 2:
            d, s = par if colour[par[0]] == 0 else par[::-1]
        elif len(par) == 1:
            d, s = (par[0], None) if colour.get(par[0], 0) == 0 else (None, par[0])
        else:
            d = s = None
        mother.append(None if d is None else names[d])
        father.append(None if s is None else names[s])
    return {"id": list(names), "mother": mother, "father": father}


def _load_iur(text: str) -> dict[str, list[str | None]]:
    """Kinsources IUR text: an individuals table, then a unions table listing each union's children.

    Returns columns ``Id, Gender, FatherId, MotherId``; a parent id of ``0`` means unknown.
    """
    blocks = {b.split("\t", 2)[1]: b.splitlines()[1:] for b in text.split("\n\n") if b.startswith("Id\t")}
    individuals = [line.split("\t") for line in blocks["Name"]]
    parents: dict[str, tuple[str, str]] = {}
    for line in blocks["Status"]:
        _, _, father, mother, children, *_ = line.split("\t")
        for child in filter(None, children.split(";")):
            if child in parents:
                raise ValueError(f"IUR: individual {child} is a child of two unions")
            parents[child] = (father, mother)
    ids = [row[0] for row in individuals]
    return {
        "Id": ids,
        "Gender": [row[2] for row in individuals],
        "FatherId": [parents.get(i, (None, None))[0] for i in ids],
        "MotherId": [parents.get(i, (None, None))[1] for i in ids],
    }


def _is_na(value: object) -> bool:
    if value is None:
        return True
    try:
        return bool(value != value)  # NaN and pandas NA compare unequal to themselves
    except TypeError:
        return True  # pandas NA raises on bool()


def _as_token(value: object) -> str:
    """Render R integers stored as float (``12.0``) the way R prints them (``12``)."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def apply_parent_overrides(table: dict[str, list[str | None]], spec: dict[str, Any]) -> None:
    """Apply ``parent_overrides: {id: {mother: ..., father: ...}}`` in place; null means unknown.

    For documented errors in a source file that ``validate`` cannot repair,
    such as an individual listed as its own parent.
    """
    cols = spec["columns"]
    for orig, fix in spec.get("parent_overrides", {}).items():
        rows = [i for i, v in enumerate(table[cols["id"]]) if v == str(orig)]
        if len(rows) != 1:
            raise ValueError(f"parent_overrides: id {orig!r} matched {len(rows)} rows")
        for role in ("mother", "father"):
            if role in fix:
                table[cols[role]][rows[0]] = None if fix[role] is None else str(fix[role])


def raw_table(table: dict[str, list[str | None]], spec: dict[str, Any]) -> dict[str, list[str]]:
    """The columns pedigrees.normalize() reads: id, mother, father, sex (1 or 2, else blank), target."""
    apply_parent_overrides(table, spec)
    cols = spec["columns"]
    missing = {str(v) for v in spec.get("missing_parent", [])}
    sex_map = {str(k): str(v) for k, v in spec.get("sex_map", {}).items()}

    def parent(values: list[str | None]) -> list[str]:
        return ["" if v is None or v in missing else v for v in values]

    n = len(table[cols["id"]])
    sexes = table[cols["sex"]] if cols.get("sex") else [None] * n
    out = {
        "id": [str(v) for v in table[cols["id"]]],
        "mother": parent(table[cols["mother"]]),
        "father": parent(table[cols["father"]]),
        "sex": [sex_map.get(s, "") if s is not None else "" for s in sexes],
    }
    if ref := spec.get("reference_column"):
        out["target"] = ["1" if v in ("1", "1.0") else "0" for v in table[ref]]
    return out
