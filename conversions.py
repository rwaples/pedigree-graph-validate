"""The closed list of conversions from an oracle's convention to pedigree-graph's.

A row that needs one names its id; the results show it. A gap that no listed
conversion explains is a FAIL, never a new entry here without an exact rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    import numpy as np


@dataclass(frozen=True)
class Conversion:
    """One declared convention gap and the exact rule that closes it."""

    id: str
    description: str
    apply: Callable[[np.ndarray], np.ndarray]


CONVERSIONS = {
    c.id: c
    for c in (
        Conversion(
            "A2PHI",
            "the oracle returns the additive relationship A = 2 x kinship (nadiv, pedigreeTools, AGHmatrix)",
            lambda a: a / 2.0,
        ),
    )
}


# ---------------------------------------------------------------- relationship categories

#: (up, down) of a collateral path group -> (full code, half code); None where pedigree-graph has no code.
_COLLATERAL = {
    (1, 1): ("FS", None),  # half: MHS or PHS, by the shared parent's sex
    (2, 1): ("Av", "HAv"),
    (3, 1): ("GAv", "HGAv"),
    (4, 1): ("GGAv", "HGGAv"),
    (5, 1): ("G3Av", None),
    (2, 2): ("1C", "H1C"),
    (3, 2): ("1C1R", "H1C1R"),
    (4, 2): ("1C2R", None),
    (3, 3): ("2C", None),
}
_LINEAL = {2: "GP", 3: "GGP", 4: "GGGP", 5: "G3GP"}


def path_categories(paths: list[list[int]], sex: dict[int, int] | list[int], rule: str = "engine") -> set[str]:
    """Every pedigree-graph category that verbalisr's paths of one pair satisfy (conversion VB).

    `paths` holds [l1, l2, full, ancestors...] per path (oracles/verbalisr.R);
    `sex` maps an id to 1 male or 2 female. A lineal path of length 1 is MO or
    FO by the parent's sex, longer ones GP to G3GP. Collateral paths are
    grouped by (up, down), and the group is the full or the half category by
    `rule`:

    - "engine": pedigree-graph's definitions as its ADR 0018 states them. A
      verbalisr path through a mated pair is two paths, one through a single
      ancestor is one, and the paths of both orientations of a pair (which
      member is the niece, or the junior cousin) are summed; the group is full
      with at least two and half with one. Sibs keep their rule: full when the
      two share both parents.
    - "mated_pair": the genealogical rule verbalisr follows: full exactly when
      the connecting ancestors are a mated pair, for every category (D1).
    """
    groups: dict[tuple[int, int], list[tuple[bool, list[int]]]] = {}
    found: set[str] = set()
    for l1, l2, full, *ancestors in paths:
        up, down = max(l1, l2), min(l1, l2)
        if down == 0:
            if up == 1:
                found.add("MO" if sex[ancestors[0]] == 2 else "FO")
            elif up in _LINEAL:
                found.add(_LINEAL[up])
            continue
        groups.setdefault((up, down), []).append((full == 1, ancestors))
    for key, group in groups.items():
        if key not in _COLLATERAL:
            continue
        full_code, half_code = _COLLATERAL[key]
        if rule == "mated_pair" or key == (1, 1):
            if any(full for full, _ in group):
                found.add(full_code)
            if not all(full for full, _ in group):
                if key == (1, 1):
                    found |= {"MHS" if sex[anc[0]] == 2 else "PHS" for full, anc in group if not full}
                elif half_code is not None:
                    found.add(half_code)
            continue
        count = sum(len(anc) for _, anc in group)
        if count >= 2:
            found.add(full_code)
        elif half_code is not None:
            found.add(half_code)
    return found


def verbalisr_first_path(paths: list[list[int]], sex: dict[int, int] | list[int]) -> str | None:
    """The category of verbalisr's own first path alone (its ordering: degree, steps, then removal)."""
    if not paths:
        return None
    found = path_categories(paths[:1], sex)
    return next(iter(found)) if found else "none"


CONVERSIONS["VB"] = Conversion(
    "VB",
    "verbalisr's paths of a pair are mapped to pedigree-graph categories by path_categories() "
    "under pedigree-graph's ADR 0018 definitions, and the closest one (lowest degree, then "
    "registry order) is the reference",
    lambda a: a,
)
