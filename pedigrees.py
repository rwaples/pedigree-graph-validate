"""Load a case's pedigree into one shape, and write it for the R scripts.

Every source (a committed seeded file, a dataset bundled in an R package, a
downloaded public pedigree) becomes a Pedigree: ids 1..N in row order, parents
before children, 0 for a missing parent or no co-twin, sex 1 male, 2 female,
0 unknown. Graph rows are therefore id - 1 in both bindings.
"""

from __future__ import annotations

import gzip
import hashlib
import subprocess
from dataclasses import dataclass, field, replace
from pathlib import Path

import numpy as np
import yaml
from pedigree_graph import PedigreeGraph

ROOT = Path(__file__).resolve().parent
COLUMNS = ("id", "mother", "father", "sex", "twin")


@dataclass
class Pedigree:
    """One case's pedigree; `extra` holds the integer columns some cases read (target, yob)."""

    id: np.ndarray
    mother: np.ndarray
    father: np.ndarray
    sex: np.ndarray
    twin: np.ndarray
    extra: dict[str, np.ndarray] = field(default_factory=dict)

    @property
    def n(self) -> int:
        """The number of individuals."""
        return len(self.id)

    @property
    def has_twins(self) -> bool:
        """Whether any row has an MZ co-twin."""
        return bool((self.twin > 0).any())

    @property
    def n_half_founders(self) -> int:
        """Rows with exactly one known parent."""
        return int(((self.mother > 0) ^ (self.father > 0)).sum())

    def graph(self) -> PedigreeGraph:
        """The pedigree-graph Python binding's graph of this pedigree."""

        def missing(x: np.ndarray) -> np.ndarray:
            return np.where(x == 0, -1, x).astype(np.int64)

        return PedigreeGraph.from_arrays(
            ids=self.id.astype(np.int64),
            mother_ids=missing(self.mother),
            father_ids=missing(self.father),
            twin_ids=missing(self.twin),
            sex=self.sex.astype(np.int8),
            sex_encoding="plink",
        )

    def with_phantom_parents(self) -> Pedigree:
        """A copy where each missing parent of a one-parent row is a new founder.

        For oracles that refuse one-parent rows (pedtools). A phantom founder is
        unrelated and not inbred, so no kinship, F or relationship category among
        the real rows changes. Phantoms take ids above N and come first, so
        parents still precede children.
        """
        half = np.flatnonzero((self.mother > 0) ^ (self.father > 0))
        if len(half) == 0:
            return self
        mother, father = self.mother.copy(), self.father.copy()
        phantom_ids = np.arange(self.n + 1, self.n + 1 + len(half), dtype=self.id.dtype)
        phantom_sex = np.where(mother[half] == 0, 2, 1).astype(self.sex.dtype)
        mother[half] = np.where(mother[half] == 0, phantom_ids, mother[half])
        father[half] = np.where(father[half] == 0, phantom_ids, father[half])
        zeros = np.zeros(len(half), dtype=self.id.dtype)
        return Pedigree(
            id=np.concatenate([phantom_ids, self.id]),
            mother=np.concatenate([zeros, mother]),
            father=np.concatenate([zeros, father]),
            sex=np.concatenate([phantom_sex, self.sex]),
            twin=np.concatenate([zeros, self.twin]),
        )

    def with_role_sex(self) -> Pedigree:
        """A copy where each parent's sex is its role's: 2 for a mother, 1 for a father.

        For oracles that refuse a mother recorded as male (pedtools, GENLIB).
        Kinship and F do not depend on sex, and the MHS/PHS reading of a path
        follows the parent's role, so nothing compared changes. Raises
        ValueError when an id is the mother of one row and the father of another.
        """
        mothers, fathers = self.mother[self.mother > 0], self.father[self.father > 0]
        if len(both := np.intersect1d(mothers, fathers)):
            raise ValueError(f"ids {', '.join(map(str, both))} are recorded as both a mother and a father")
        sex = self.sex.copy()
        sex[mothers - 1] = 2
        sex[fathers - 1] = 1
        return replace(self, sex=sex)

    def write_tsv(self, path: Path) -> Path:
        """Write the five pedigree columns as TSV for the R scripts."""
        table = np.column_stack([self.id, self.mother, self.father, self.sex, self.twin])
        np.savetxt(path, table, fmt="%d", delimiter="\t", header="\t".join(COLUMNS), comments="")
        return path


def _from_table(header: list[str], rows: list[list[str]]) -> Pedigree:
    cols = {name: [r[k] for r in rows] for k, name in enumerate(header)}

    def ints(name: str) -> np.ndarray:
        return np.array([int(v) if v != "" else -1 for v in cols[name]], dtype=np.int32)

    ped = Pedigree(*(ints(c) for c in COLUMNS), extra={c: ints(c) for c in header if c not in COLUMNS})
    if not np.array_equal(ped.id, np.arange(1, ped.n + 1)):
        raise ValueError("ids must be 1..N in row order")
    if ((ped.mother >= ped.id) | (ped.father >= ped.id)).any():
        raise ValueError("a parent must precede its children")
    return ped


def read_tsv(path: Path) -> Pedigree:
    """Read a pedigree TSV (gzip or plain) with the five columns and any extras."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as handle:
        lines = [line.rstrip("\n").split("\t") for line in handle if line.strip()]
    return _from_table(lines[0], lines[1:])


def sha256(path: Path) -> str:
    """The file's sha256, hex."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


#: Parent tokens that mean "missing", after stripping; compared case-insensitively.
MISSING = frozenset({"", "0", "na", "nan", "unknown", "unk", "-1", "."})
_SEX = {"1": 1, "m": 1, "male": 1, "2": 2, "f": 2, "female": 2}


def normalize(table: dict[str, list[str]]) -> tuple[Pedigree, list[str]]:
    """A Pedigree from raw columns id, mother, father, sex (strings) and integer extras.

    Original ids become 1..N; a parent that has no row of its own is added as a
    founder; rows are sorted so parents come first (stable otherwise). Returns
    the pedigree and the original id of each row.
    """
    raw = [str(i).strip() for i in table["id"]]
    if len(set(raw)) != len(raw):
        raise ValueError("duplicate ids")
    mothers = [None if str(m).strip().lower() in MISSING else str(m).strip() for m in table["mother"]]
    fathers = [None if str(f).strip().lower() in MISSING else str(f).strip() for f in table["father"]]
    sexes = [_SEX.get(str(x).strip().lower(), 0) for x in table.get("sex", [""] * len(raw))]
    known = set(raw)
    extra_parents = []
    for parents, sex in ((mothers, 2), (fathers, 1)):
        for p in parents:
            if p is not None and p not in known:
                known.add(p)
                extra_parents.append((p, sex))
    rows = [(p, None, None, s) for p, s in extra_parents] + list(zip(raw, mothers, fathers, sexes, strict=True))
    index = {r[0]: k for k, r in enumerate(rows)}
    order: list[int] = []
    state = [0] * len(rows)  # 0 new, 1 on the stack, 2 placed
    for start in range(len(rows)):
        stack = [start]
        while stack:
            k = stack[-1]
            if state[k] == 2:
                stack.pop()
                continue
            state[k] = 1
            pending = [index[p] for p in rows[k][1:3] if p is not None and state[index[p]] != 2]
            if any(state[q] == 1 for q in pending):
                raise ValueError(f"pedigree loop through {rows[k][0]!r}")
            if pending:
                stack.extend(pending)
            else:
                state[k] = 2
                order.append(k)
                stack.pop()
    new_id = {rows[k][0]: n + 1 for n, k in enumerate(order)}
    ids = [rows[k][0] for k in order]

    def col(f) -> np.ndarray:
        return np.array([f(rows[k]) for k in order], dtype=np.int32)

    extras = {}
    for name, values in table.items():
        if name not in ("id", "mother", "father", "sex"):
            by_id = dict(zip(raw, values, strict=True))
            extras[name] = np.array(
                [int(by_id[i]) if by_id.get(i, "") not in ("", None) else -1 for i in ids], dtype=np.int32
            )
    sex = col(lambda r: r[3])
    # A parent with unknown sex takes the sex of its role: exact, and what the
    # MO/FO and MHS/PHS reading of verbalisr's paths needs.
    mother, father = col(lambda r: new_id[r[1]] if r[1] else 0), col(lambda r: new_id[r[2]] if r[2] else 0)
    unknown = sex == 0
    sex[np.intersect1d(mother[mother > 0], np.flatnonzero(unknown) + 1) - 1] = 2
    sex[np.intersect1d(father[father > 0], np.flatnonzero(unknown) + 1) - 1] = 1
    ped = Pedigree(
        id=np.arange(1, len(order) + 1, dtype=np.int32),
        mother=mother,
        father=father,
        sex=sex,
        twin=np.zeros(len(order), dtype=np.int32),
        extra=extras,
    )
    return ped, ids


def read_raw(path: Path) -> dict[str, list[str]]:
    """The columns of a raw TSV (gzip or plain) as strings."""
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as handle:
        lines = [line.rstrip("\n").split("\t") for line in handle if line.strip()]
    header = lines[0]
    return {name: [r[k] if k < len(r) else "" for r in lines[1:]] for k, name in enumerate(header)}


def load(spec: dict[str, str], work: Path) -> Pedigree:
    """The pedigree of a case's `input`: a committed `file`, a `bundled` R dataset, or a public `dataset`.

    A committed file is sha256-checked here; a public dataset is downloaded
    once into .cache/ and sha256-checked by datasets.fetch.
    """
    if "dataset" in spec:
        import datasets  # rdata, openpyxl and network access are needed only here

        entry = yaml.safe_load((ROOT / "datasets.yaml").read_text())["datasets"][spec["dataset"]]
        path = datasets.fetch(entry, ROOT / ".cache")
        return normalize(datasets.raw_table(datasets.load_table(path, entry), entry))[0]
    if "file" in spec:
        path = ROOT / spec["file"]
        if (got := sha256(path)) != spec["sha256"]:
            raise ValueError(f"{spec['file']} has sha256 {got}, pinned {spec['sha256']}; run make_inputs.py --verify")
        return read_tsv(path)
    if "bundled" in spec:
        package, dataset = spec["bundled"].split("::")
        out = work / "bundled.tsv"
        subprocess.run(["Rscript", "bundled.R", package, dataset, str(out)], cwd=ROOT, check=True)
        return normalize(read_raw(out))[0]
    raise ValueError(f"unknown input {spec}")
