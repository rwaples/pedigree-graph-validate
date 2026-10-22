"""Write the seeded synthetic pedigrees to inputs/*.tsv.gz.

Each file has the columns id, mother, father, sex, twin: ids are 1..N in row
order, parents come before their children, 0 marks a missing parent or no
co-twin, and sex is 1 male, 2 female. gzip's mtime is fixed at 0, so a rerun
reproduces each file byte for byte and its sha256 in cases.yaml.

    python make_inputs.py            # write inputs/
    python make_inputs.py --verify   # regenerate into a temp dir and compare sha256 with cases.yaml
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import sys
import tempfile
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parent
INPUTS = ROOT / "inputs"
MALE, FEMALE = 1, 2

Rows = list[tuple[int, int, int, int, int]]


def double_first_cousins() -> Rows:
    """Double first cousins, two cousin marriages and their inbred child, and a half-sib.

    Brothers 5, 6 (of 2 x 1) marry sisters 7, 8 (of 4 x 3), so 9, 10 and 11, 12
    are double first cousins. 9 x 12 and 10 x 11 are cousin marriages; their
    children 13 and 15 have a child 16. 18 is a maternal half-sib of 5 and 6.
    """
    return [
        (1, 0, 0, MALE, 0),
        (2, 0, 0, FEMALE, 0),
        (3, 0, 0, MALE, 0),
        (4, 0, 0, FEMALE, 0),
        (5, 2, 1, MALE, 0),
        (6, 2, 1, MALE, 0),
        (7, 4, 3, FEMALE, 0),
        (8, 4, 3, FEMALE, 0),
        (9, 7, 5, MALE, 0),
        (10, 7, 5, FEMALE, 0),
        (11, 8, 6, MALE, 0),
        (12, 8, 6, FEMALE, 0),
        (13, 12, 9, MALE, 0),
        (14, 12, 9, FEMALE, 0),
        (15, 10, 11, FEMALE, 0),
        (16, 15, 13, MALE, 0),
        (17, 0, 0, MALE, 0),
        (18, 2, 17, FEMALE, 0),
    ]


def conventions() -> Rows:
    """Pairs that satisfy two categories, where reporting conventions can split.

    3 and 6 share mother 1, and 3 is 6's grandfather (3 -> 5 -> 6): MHS and GP.
    9 and 12 share father 8, and 9 is 12's grandmother (9 -> 11 -> 12): PHS and GP.
    23 and 24 are double half first cousins: their mothers 19, 21 are maternal
    half-sibs (of 13) and their fathers 20, 22 paternal half-sibs (of 16), so
    they share two grandparents, 13 and 16, who are not mates.
    """
    return [
        (1, 0, 0, FEMALE, 0),
        (2, 0, 0, MALE, 0),
        (3, 1, 2, MALE, 0),
        (4, 0, 0, FEMALE, 0),
        (5, 4, 3, MALE, 0),
        (6, 1, 5, FEMALE, 0),
        (7, 0, 0, FEMALE, 0),
        (8, 0, 0, MALE, 0),
        (9, 7, 8, FEMALE, 0),
        (10, 0, 0, MALE, 0),
        (11, 9, 10, FEMALE, 0),
        (12, 11, 8, MALE, 0),
        (13, 0, 0, FEMALE, 0),
        (14, 0, 0, MALE, 0),
        (15, 0, 0, MALE, 0),
        (16, 0, 0, MALE, 0),
        (17, 0, 0, FEMALE, 0),
        (18, 0, 0, FEMALE, 0),
        (19, 13, 14, FEMALE, 0),
        (20, 17, 16, MALE, 0),
        (21, 13, 15, FEMALE, 0),
        (22, 18, 16, MALE, 0),
        (23, 19, 20, MALE, 0),
        (24, 21, 22, FEMALE, 0),
    ]


def mz_family() -> Rows:
    """MZ co-twins 3 and 4, each with a child by a different mate (7 and 8, genetic half-sibs)."""
    return [
        (1, 0, 0, FEMALE, 0),
        (2, 0, 0, MALE, 0),
        (3, 1, 2, MALE, 4),
        (4, 1, 2, MALE, 3),
        (5, 0, 0, FEMALE, 0),
        (6, 0, 0, FEMALE, 0),
        (7, 5, 3, FEMALE, 0),
        (8, 6, 4, MALE, 0),
        (9, 7, 8, FEMALE, 0),
    ]


def random_mating(seed: int, n_gen: int, per_gen: int) -> Rows:
    """Discrete generations of `per_gen`, half of each sex; each child draws a mother and a father at random."""
    rng = np.random.default_rng(seed)
    rows: Rows = []
    previous: list[tuple[int, int]] = []
    for g in range(n_gen):
        start = len(rows) + 1
        sexes = [MALE if k % 2 == 0 else FEMALE for k in range(per_gen)]
        mothers = [i for i, s in previous if s == FEMALE]
        fathers = [i for i, s in previous if s == MALE]
        for k, sex in enumerate(sexes):
            if g == 0:
                rows.append((start + k, 0, 0, sex, 0))
            else:
                rows.append((start + k, int(rng.choice(mothers)), int(rng.choice(fathers)), sex, 0))
        previous = [(start + k, s) for k, s in enumerate(sexes)]
    return rows


GENERATORS = {
    "double_first_cousins": double_first_cousins,
    "conventions": conventions,
    "mz_family": mz_family,
    "deep_chain": lambda: random_mating(seed=11, n_gen=10, per_gen=8),
    "wf_300": lambda: random_mating(seed=12, n_gen=5, per_gen=60),
    "deep_wf": lambda: random_mating(seed=13, n_gen=300, per_gen=20),
    "wf_10k": lambda: random_mating(seed=14, n_gen=10, per_gen=1000),
}


def encode(rows: Rows) -> bytes:
    """The gzip bytes of `rows` as TSV, with mtime 0."""
    text = "id\tmother\tfather\tsex\ttwin\n" + "".join("\t".join(map(str, r)) + "\n" for r in rows)
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb", mtime=0) as gz:
        gz.write(text.encode())
    return buffer.getvalue()


def check(rows: Rows) -> None:
    """Ids are 1..N in order, parents precede children, twins are mutual."""
    ids = [r[0] for r in rows]
    assert ids == list(range(1, len(rows) + 1)), "ids must be 1..N in row order"
    for i, m, f, _, t in rows:
        assert m < i, f"row {i}: the mother must come first"
        assert f < i, f"row {i}: the father must come first"
        assert t == 0 or rows[t - 1][4] == i, f"row {i}: twin link must be mutual"


def write_all(out: Path) -> dict[str, str]:
    """Write every generator's file into `out`; return name -> sha256."""
    out.mkdir(parents=True, exist_ok=True)
    digests = {}
    for name, make in GENERATORS.items():
        rows = make()
        check(rows)
        data = encode(rows)
        (out / f"{name}.tsv.gz").write_bytes(data)
        digests[name] = hashlib.sha256(data).hexdigest()
    return digests


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--verify", action="store_true", help="compare regenerated sha256 with cases.yaml")
    args = parser.parse_args()
    if not args.verify:
        for name, digest in write_all(INPUTS).items():
            print(f"{name}\t{digest}")
        return 0
    pinned = {
        Path(c["input"]["file"]).name.removesuffix(".tsv.gz"): c["input"]["sha256"]
        for c in yaml.safe_load((ROOT / "cases.yaml").read_text())["cases"]
        if "file" in c.get("input", {})
    }
    with tempfile.TemporaryDirectory() as tmp:
        fresh = write_all(Path(tmp))
    bad = [n for n, d in pinned.items() if fresh.get(n) != d]
    for n in bad:
        print(f"verify-inputs: {n}: regenerated {fresh.get(n)}, pinned {pinned[n]}")
    print(f"verify-inputs: {len(pinned) - len(bad)}/{len(pinned)} match")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
