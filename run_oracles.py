"""Check pedigree-graph's two bindings against the same methods in other software.

For each case in cases.yaml: load its pedigree, run the Python binding here
and the R binding through pg_r.R, run each oracle's R script under the caps of
cases.yaml's `budget`, and compare. Writes results/results.md and
results/results.tsv; exits 1 on any FAIL or ERROR.

    python run_oracles.py                     # every case
    python run_oracles.py --only conventions,wf_300
    python run_oracles.py --install-r         # install pedigreegraph.pin and oracles.lock into .r-lib/
    python run_oracles.py --preflight         # both bindings report the pin; every oracle loads
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import resource
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from importlib.metadata import version as dist_version
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np
import yaml
from pedigree_graph import RELATIONSHIPS, MissingMetadataError
from pedigree_graph.effective_size import ne_individual_delta_f, ne_long_term_contributions

from conversions import CONVERSIONS, path_categories, verbalisr_first_path
from pedigrees import load

if TYPE_CHECKING:
    from concurrent.futures import Future

    from pedigrees import Pedigree

ROOT = Path(__file__).resolve().parent
R_LIB = ROOT / ".r-lib"
DOWNLOAD = R_LIB / "_download"
WORK = ROOT / ".work"
RESULTS = ROOT / "results"
#: Set to a local pedigreegraph source tarball to check a checkout (not committed).
OVERRIDE_ENV = "PGV_R_TARBALL"
#: Every oracle package the R scripts load, conda-forge and CRAN alike.
ORACLES = ("kinship2", "GENLIB", "ribd", "verbalisr", "nadiv", "pedigreeTools", "AGHmatrix", "purgeR", "visPedigree")
STATUSES = ("PASS", "DIFF", "GAP", "INFO", "SKIP", "FAIL", "ERROR")


# ---------------------------------------------------------------- R setup


def sha256(path: Path) -> str:
    """The file's sha256, hex."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_pin() -> dict[str, str]:
    """pedigreegraph.pin: the R tarball's version, url and sha256."""
    return yaml.safe_load((ROOT / "pedigreegraph.pin").read_text())


def read_lock() -> list[dict[str, str]]:
    """oracles.lock: the CRAN tarballs, dependencies first."""
    return yaml.safe_load((ROOT / "oracles.lock").read_text())["packages"]


def _fetch(url: str, dest: Path, want: str) -> None:
    """Download `url` to `dest` unless a file with sha256 `want` is already there."""
    if dest.exists() and sha256(dest) == want:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"r-setup: downloading {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "pedigree-graph-validate"})
    with urllib.request.urlopen(request, timeout=120) as response, dest.open("wb") as out:
        shutil.copyfileobj(response, out)


def _install(name: str, tarball: Path, want: str) -> None:
    """R CMD INSTALL `tarball` into .r-lib/, once per sha256; refuse a hash mismatch."""
    got = sha256(tarball)
    if got != want:
        sys.exit(f"r-setup: {tarball} has sha256 {got}, pinned {want}; refusing it")
    stamp = R_LIB / f".{name}.sha256"
    if stamp.exists() and stamp.read_text().strip() == want and (R_LIB / name / "DESCRIPTION").exists():
        print(f"r-setup: {name} already installed from {want[:12]}")
        return
    subprocess.run(["R", "CMD", "INSTALL", f"--library={R_LIB}", str(tarball)], check=True)
    stamp.write_text(want + "\n")
    print(f"r-setup: installed {name} from {want[:12]}")


def install_r() -> None:
    """Install every oracles.lock tarball, then the pedigreegraph pin (or the override)."""
    R_LIB.mkdir(exist_ok=True)
    for pkg in read_lock():
        tarball = DOWNLOAD / Path(pkg["url"]).name
        try:
            _fetch(pkg["url"], tarball, pkg["sha256"])
        except urllib.error.HTTPError:
            # CRAN moves a superseded release to Archive/; the sha256 still pins it.
            _fetch(f"{Path(pkg['url']).parent}/Archive/{pkg['name']}/{tarball.name}", tarball, pkg["sha256"])
        _install(pkg["name"], tarball, pkg["sha256"])
    if override := os.environ.get(OVERRIDE_ENV):
        tarball = Path(override).resolve()
        _install("pedigreegraph", tarball, sha256(tarball))
        return
    pin = read_pin()
    tarball = DOWNLOAD / f"pedigreegraph_{pin['version']}.tar.gz"
    _fetch(pin["url"], tarball, pin["sha256"])
    _install("pedigreegraph", tarball, pin["sha256"])


# ---------------------------------------------------------------- preflight


def r_versions() -> dict[str, str]:
    """R's version and the packageVersion() of pedigreegraph and every oracle, loaded."""
    script = (
        "pk <- commandArgs(TRUE); "
        "for (p in pk) suppressPackageStartupMessages(library(p, character.only = TRUE)); "
        "v <- c(R = R.version.string, sapply(pk, function(p) as.character(packageVersion(p)))); "
        "cat(jsonlite::toJSON(as.list(v), auto_unbox = TRUE))"
    )
    out = subprocess.run(
        ["Rscript", "-e", script, "pedigreegraph", *ORACLES], check=True, capture_output=True, text=True
    )
    return json.loads(out.stdout)


def preflight() -> dict[str, str]:
    """Refuse to run unless both bindings report the pin (or the R override is set)."""
    pin = read_pin()["version"]
    versions = {"pedigree-graph (Python)": dist_version("pedigree-graph"), **r_versions()}
    r_binding = versions["pedigreegraph"]
    if os.environ.get(OVERRIDE_ENV):
        # No binding exports its core rev yet (pedigree-graph#46), so the override is unchecked.
        print(f"preflight: override {os.environ[OVERRIDE_ENV]}; core rev UNCHECKED")
    elif {versions["pedigree-graph (Python)"], r_binding} != {pin}:
        sys.exit(
            f"preflight: pinned {pin}, but Python {versions['pedigree-graph (Python)']} and R {r_binding};"
            " run `pixi install` and `pixi run r-setup`"
        )
    return versions


# ---------------------------------------------------------------- rows


@dataclass
class Row:
    """One row of results: one check of one case against one reference."""

    case: str
    family: str
    check: str
    reference: str
    status: str
    n: int | None = None
    max_abs_diff: float | None = None
    tol: float | None = None
    wall_s: float | None = None
    note: str = ""


def _fmt(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:.3g}"
    return str(v)


# ---------------------------------------------------------------- running R


class BudgetExceeded(Exception):
    """An oracle call hit a Cap (wall time or memory)."""


@dataclass
class Call:
    """The outputs of one R script run on one case."""

    outputs: dict[str, np.ndarray]
    versions: dict[str, str]
    wall_s: float


def run_r(script: str, name: str, ped: Pedigree, work: Path, spec: dict[str, Any], budget: dict[str, Any]) -> Call:
    """Run `script` on `ped` with the inputs in `spec`, under the per-call wall and memory limits."""
    out_dir = work / name
    out_dir.mkdir(parents=True, exist_ok=True)
    request = {
        "pedigree": str(ped.write_tsv(out_dir / "pedigree.tsv")),
        "oracle": name,
        "out_dir": str(out_dir),
        **spec,
    }
    in_json, out_json = out_dir / "in.json", out_dir / "out.json"
    in_json.write_text(json.dumps(request))
    mem = int(budget["mem_gb"] * 2**30)

    def limit() -> None:
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))

    start = time.perf_counter()
    try:
        done = subprocess.run(
            ["Rscript", script, str(in_json), str(out_json)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=budget["timeout_s"],
            preexec_fn=limit,
            check=False,
        )
    except subprocess.TimeoutExpired as err:
        raise BudgetExceeded(f"over the {budget['timeout_s']} s wall limit") from err
    wall = time.perf_counter() - start
    if done.returncode != 0:
        if "cannot allocate" in done.stderr or "std::bad_alloc" in done.stderr:
            raise BudgetExceeded(f"over the {budget['mem_gb']} GB memory limit")
        tail = " | ".join(done.stderr.strip().splitlines()[-3:])
        raise RuntimeError(f"{script} exited {done.returncode}: {tail}")
    result = json.loads(out_json.read_text())
    outputs = {k: np.fromfile(v, dtype="<f8") for k, v in result["outputs"].items()}
    return Call(outputs, result["versions"], wall)


# ---------------------------------------------------------------- pair sets


def write_pairs(first: np.ndarray, second: np.ndarray, work: Path, name: str) -> dict[str, str]:
    """Write a pair set (ids) as two int32 files; return their paths."""
    paths = {}
    for side, ids in (("first", first), ("second", second)):
        path = work / f"pairs.{name}.{side}.i32"
        ids.astype("<i4").tofile(path)
        paths[side] = str(path)
    return paths


def all_pairs(ids: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Every pair i <= j of `ids`, the diagonal included."""
    i, j = np.triu_indices(len(ids))
    return ids[i], ids[j]


def kinship_pairs(
    ped: Pedigree, graph: Any, budget: dict[str, Any], rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray, str]:
    """The pair set the dense oracles are compared on, and how it was drawn.

    Every pair when N is at most `all_pairs_max_n`. Otherwise a uniform sample
    of `sample_pairs`, a sample of `related_pairs` among the pairs pedigree-graph
    classifies to degree 5 (most uniform pairs are unrelated), and a sample of
    the diagonal. Which pairs are compared is pedigree-graph's choice; the
    values compared are the oracle's.
    """
    if ped.n <= budget["all_pairs_max_n"]:
        first, second = all_pairs(ped.id)
        return first, second, "all pairs"
    k = budget["sample_pairs"]
    uniform = rng.integers(1, ped.n + 1, size=(2, k))
    blocks = graph.relationship_pairs(max_degree=5)
    related = np.concatenate([np.stack([np.asarray(f), np.asarray(s)]) + 1 for f, s in blocks.values()], axis=1)
    if related.shape[1] > budget["related_pairs"]:
        related = related[:, rng.choice(related.shape[1], budget["related_pairs"], replace=False)]
    diagonal = rng.choice(ped.id, size=min(ped.n, 2000), replace=False)
    first = np.concatenate([uniform[0], related[0], diagonal])
    second = np.concatenate([uniform[1], related[1], diagonal])
    return first, second, f"{k} uniform + {related.shape[1]} related + {len(diagonal)} self pairs"


def proband_pairs(
    ped: Pedigree, budget: dict[str, Any], rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray, str]:
    """Every pair among a seeded sample of at most `genlib_max_probands` ids (GENLIB's pair set)."""
    k = budget["genlib_max_probands"]
    if ped.n <= k:
        first, second = all_pairs(ped.id)
        return first, second, "all pairs"
    probands = np.sort(rng.choice(ped.id, size=k, replace=False))
    first, second = all_pairs(probands)
    return first, second, f"all pairs of {k} sampled probands"


# ---------------------------------------------------------------- kinship and inbreeding


@dataclass
class CaseContext:
    """What every family of one case shares."""

    id: str
    ped: Pedigree
    graph: Any
    #: What the oracles read: `ped` with each parent's sex set to its role, or
    #: `ped` itself when `refused` says why that copy cannot be made.
    oracle_ped: Pedigree
    refused: str
    work: Path
    budget: dict[str, Any]
    expect: list[dict[str, Any]]
    ne_checks: list[dict[str, Any]] = field(default_factory=list)
    versions: dict[str, dict[str, str]] = field(default_factory=dict)


def _expected(ctx: CaseContext, family: str, reference: str, check: str) -> dict[str, Any] | None:
    for e in ctx.expect:
        if e["family"] == family and e["reference"] == reference and e.get("check", check) == check:
            return e
    return None


def compare(
    ctx: CaseContext,
    family: str,
    check: str,
    reference: str,
    pg: np.ndarray,
    ref: np.ndarray,
    tol: float,
    wall: float | None,
    note: str = "",
) -> Row:
    """Score `pg` against `ref` at absolute `tol`, honouring a declared DIFF for this row."""
    gap = np.abs(pg - ref)
    worst = float(np.nanmax(gap)) if len(gap) else 0.0
    bad_nan = int(np.isnan(ref).sum())
    within = bad_nan == 0 and worst <= tol
    declared = _expected(ctx, family, reference, check)
    if declared is not None and declared["status"] == "diff":
        # A declared DIFF that now matches is a FAIL, so a stale declaration surfaces.
        status = "FAIL" if within else "DIFF"
        note = f"{declared['id']}; {note}".strip("; ")
    else:
        status = "PASS" if within else "FAIL"
    if bad_nan:
        note = f"{bad_nan} NaN in the reference; {note}".strip("; ")
    return Row(ctx.id, family, check, reference, status, len(pg), worst, tol, wall, note)


def kinship_family(ctx: CaseContext, cfg: dict[str, Any], rng: np.random.Generator) -> list[Row]:
    """Pairwise kinship and F, both bindings, against every oracle in cases.yaml's `kinship_oracles`."""
    ped, budget, tol = ctx.ped, ctx.budget, cfg["tolerances"]
    k_first, k_second, k_how = kinship_pairs(ped, ctx.graph, budget, rng)
    g_first, g_second, g_how = proband_pairs(ped, budget, rng)
    sets = {
        "pairs": write_pairs(k_first, k_second, ctx.work, "pairs"),
        "probands": write_pairs(g_first, g_second, ctx.work, "probands"),
    }
    f_ids = ctx.work / "f_ids.i32"
    ped.id.astype("<i4").tofile(f_ids)
    rows_of = {"pairs": (k_first - 1, k_second - 1), "probands": (g_first - 1, g_second - 1)}
    how = {"pairs": k_how, "probands": g_how}
    py = {f"kinship:{s}": ctx.graph.pair_kinship(*rows_of[s]).astype(np.float64) for s in sets}
    py["F"] = np.asarray(ctx.graph.inbreeding(), dtype=np.float64)

    rows: list[Row] = []
    try:
        r_call = run_r("pg_r.R", "pg_r", ped, ctx.work, {"pairs": sets, "want_f": True, "f_ids": str(f_ids)}, budget)
        ctx.versions["pg_r"] = r_call.versions
        for key, values in py.items():
            same = np.array_equal(values, r_call.outputs[key])
            worst = float(np.max(np.abs(values - r_call.outputs[key]))) if len(values) else 0.0
            rows.append(
                Row(
                    ctx.id,
                    "bindings",
                    f"{key}, Python = R",
                    "pedigreegraph (R)",
                    "PASS" if same else "FAIL",
                    len(values),
                    worst,
                    0.0,
                    r_call.wall_s,
                )
            )
    except (RuntimeError, BudgetExceeded) as err:
        rows.append(Row(ctx.id, "bindings", "Python = R", "pedigreegraph (R)", "ERROR", note=str(err)))

    # Every oracle call of the case runs at once (`workers` at a time): each is
    # its own Rscript process under its own wall and memory limit.
    jobs: dict[str, Future[Call]] = {}
    with ThreadPoolExecutor(max_workers=budget["workers"]) as pool:
        for name, oracle in cfg["kinship_oracles"].items():
            pair_set = oracle.get("pairs")
            if (
                (ped.has_twins and not oracle.get("mz"))
                or (oracle.get("dense") and ped.n > budget["dense_max_n"])
                or (oracle.get("role_sex") and ctx.refused)
            ):
                continue
            oracle_ped = ctx.oracle_ped.with_phantom_parents() if oracle.get("complete_parents") else ctx.oracle_ped
            spec = {
                "pairs": {pair_set: sets[pair_set]} if pair_set else {},
                "want_f": bool(oracle.get("F")),
                "f_ids": str(f_ids),
            }
            jobs[name] = pool.submit(run_r, oracle["script"], name, oracle_ped, ctx.work, spec, budget)
    for name, oracle in cfg["kinship_oracles"].items():
        pair_set = oracle.get("pairs")
        conversion = CONVERSIONS[oracle["conversion"]] if "conversion" in oracle else None
        checks = ([("kinship", f"kinship:{pair_set}")] if pair_set else []) + (
            [("inbreeding", "F")] if oracle.get("F") else []
        )

        def emit(status: str, note: str, checks: list[tuple[str, str]] = checks, name: str = name) -> None:
            for family, key in checks:
                rows.append(Row(ctx.id, family, key.split(":")[0], name, status, note=note))

        if ped.has_twins and not oracle.get("mz"):
            emit("GAP", "G1: no MZ twin input")
            continue
        if oracle.get("role_sex") and ctx.refused:
            emit("SKIP", f"it refuses the input: {ctx.refused}")
            continue
        if name not in jobs:
            emit("SKIP", f"N = {ped.n} over the dense cap {budget['dense_max_n']}")
            continue
        try:
            call = jobs[name].result()
        except BudgetExceeded as err:
            emit("SKIP", str(err))
            continue
        except RuntimeError as err:
            emit("ERROR", str(err))
            continue
        ctx.versions[name] = call.versions
        for family, key in checks:
            ref = call.outputs[key]
            note = how[pair_set] if family == "kinship" else ""
            if conversion is not None and family == "kinship":
                ref = conversion.apply(ref)
                note = f"{conversion.id}; {note}"
            tol_key = "kinship" if family == "kinship" else "F"
            rows.append(compare(ctx, family, key.split(":")[0], name, py[key], ref, tol[tol_key], call.wall_s, note))
    return rows


# ---------------------------------------------------------------- classification


def pg_categories(graph: Any) -> dict[tuple[int, int], str]:
    """Each related pair's closest category, keyed by its (lower, higher) id."""
    out = {}
    for code, (first, second) in graph.relationship_pairs(max_degree=5).items():
        a, b = np.asarray(first) + 1, np.asarray(second) + 1
        for x, y in zip(np.minimum(a, b).tolist(), np.maximum(a, b).tolist(), strict=True):
            out[(x, y)] = code
    return out


def closest(found: set[str]) -> str | None:
    """pedigree-graph's closest category of `found`: lowest degree, then registry order."""
    if not found:
        return None
    order = list(RELATIONSHIPS)
    return min(found, key=lambda c: (RELATIONSHIPS[c].degree, order.index(c)))


def classify_pairs(
    ped: Pedigree, pg: dict[tuple[int, int], str], budget: dict[str, Any], rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray, str]:
    """Every pair i < j up to `classify_all_pairs_max_n`; otherwise a seeded sample.

    The sample is half pairs pedigree-graph relates, the same quota from each
    category it reports, and half uniform pairs, so pairs it calls unrelated
    are checked too.
    """
    if ped.n <= budget["classify_all_pairs_max_n"]:
        i, j = np.triu_indices(ped.n, k=1)
        return ped.id[i], ped.id[j], "all pairs"
    k = budget["classify_sample_pairs"]
    by_code: dict[str, list[tuple[int, int]]] = {}
    for pair, code in pg.items():
        by_code.setdefault(code, []).append(pair)
    quota = max(1, (k // 2) // max(1, len(by_code)))
    chosen = []
    for code in sorted(by_code):
        pairs = by_code[code]
        chosen += [pairs[t] for t in rng.choice(len(pairs), min(quota, len(pairs)), replace=False)]
    uniform = rng.integers(1, ped.n + 1, size=(k - len(chosen), 2))
    chosen += [(int(min(a, b)), int(max(a, b))) for a, b in uniform if a != b]
    arr = np.array(chosen, dtype=np.int64)
    return arr[:, 0], arr[:, 1], f"{len(arr)} sampled pairs ({len(arr) - len(uniform)} related by pg, stratified)"


def classification_family(ctx: CaseContext, cfg: dict[str, Any], rng: np.random.Generator) -> list[Row]:
    """Closest category of each pair, and on all-pair cases the counts and burden, against verbalisr."""
    ped, budget = ctx.ped, ctx.budget
    if ped.has_twins:
        return [Row(ctx.id, "classification", "closest category", "verbalisr", "GAP", note="G1: no MZ twin input")]
    if ped.n > budget["dense_max_n"]:
        # verbalise() builds ribd's kinship matrix of the whole pedigree on every call.
        return [
            Row(
                ctx.id,
                "classification",
                "closest category",
                "verbalisr",
                "SKIP",
                note=f"N = {ped.n} over the dense cap",
            )
        ]
    if ctx.refused:
        return [
            Row(
                ctx.id,
                "classification",
                "closest category",
                "verbalisr",
                "SKIP",
                note=f"it refuses the input: {ctx.refused}",
            )
        ]
    pg = pg_categories(ctx.graph)
    first, second, how = classify_pairs(ped, pg, budget, rng)
    spec = {"pairs": {"classify": write_pairs(first, second, ctx.work, "classify")}}
    full_ped = ctx.oracle_ped.with_phantom_parents()
    try:
        call = run_r("oracles/verbalisr.R", "verbalisr", full_ped, ctx.work, spec, budget)
    except BudgetExceeded as err:
        return [Row(ctx.id, "classification", "closest category", "verbalisr", "SKIP", note=str(err))]
    except RuntimeError as err:
        return [Row(ctx.id, "classification", "closest category", "verbalisr", "ERROR", note=str(err))]
    ctx.versions["verbalisr"] = call.versions
    paths = json.loads((ctx.work / "verbalisr" / "verbalisr.paths.json").read_text())
    sex = dict(zip(full_ped.id.tolist(), full_ped.sex.tolist(), strict=True))

    mismatches, glossary_splits, first_path_splits = [], [], 0
    reference: dict[tuple[int, int], str] = {}
    for a, b, pair_paths in zip(first.tolist(), second.tolist(), paths, strict=True):
        ours = pg.get((a, b))
        theirs = closest(path_categories(pair_paths, sex))
        if (mated := closest(path_categories(pair_paths, sex, rule="mated_pair"))) != ours:
            glossary_splits.append(f"{a}-{b}: pg {ours}, mated pair {mated}")
        if theirs is not None:
            reference[(a, b)] = theirs
        if ours != theirs:
            mismatches.append(f"{a}-{b}: pg {ours}, verbalisr {theirs}")
        if pair_paths and verbalisr_first_path(pair_paths, sex) != ours:
            first_path_splits += 1
    rows = [
        _scored(
            ctx,
            "classification",
            "closest category",
            "verbalisr",
            len(first),
            len(mismatches),
            call.wall_s,
            f"VB; {how}",
            mismatches,
        ),
        Row(
            ctx.id,
            "classification",
            "closest category, GLOSSARY mated-pair rule",
            "verbalisr",
            "DIFF" if glossary_splits else "PASS",
            len(first),
            float(len(glossary_splits)),
            None,
            call.wall_s,
            ("D1; " + "; ".join(glossary_splits[:3]))
            if glossary_splits
            else "every pair agrees with the mated-pair definition too",
        ),
        Row(
            ctx.id,
            "classification",
            "verbalisr's own first path",
            "verbalisr",
            "INFO",
            len(first),
            float(first_path_splits),
            None,
            call.wall_s,
            "pairs whose first verbalisr path names another category than pg's closest one; not scored",
        ),
    ]
    if how == "all pairs":
        counts = ctx.graph.relationship_counts(max_degree=5)
        theirs = dict.fromkeys(RELATIONSHIPS, 0)
        for code in reference.values():
            theirs[code] += 1
        bad = [
            f"{c}: pg {counts[c]}, verbalisr {theirs[c]}" for c in RELATIONSHIPS if c != "MZ" and counts[c] != theirs[c]
        ]
        rows.append(
            _scored(
                ctx,
                "classification",
                "relationship_counts",
                "verbalisr",
                len(RELATIONSHIPS) - 1,
                len(bad),
                None,
                "VB",
                bad,
            )
        )
        burden = np.zeros((ped.n, 5), dtype=np.int64)
        for (a, b), code in reference.items():
            d = RELATIONSHIPS[code].degree
            if d >= 1:
                burden[a - 1, d - 1] += 1
                burden[b - 1, d - 1] += 1
        per_person = np.asarray(ctx.graph.relationship_burden().per_person)
        bad_rows = np.flatnonzero((per_person != burden).any(axis=1))
        detail = [f"id {r + 1}: pg {per_person[r].tolist()}, verbalisr {burden[r].tolist()}" for r in bad_rows]
        rows.append(
            _scored(
                ctx,
                "classification",
                "relationship_burden per person",
                "verbalisr",
                ped.n,
                len(bad_rows),
                None,
                "VB",
                detail,
            )
        )
    return rows


def _scored(
    ctx: CaseContext,
    family: str,
    check: str,
    reference: str,
    n: int,
    n_bad: int,
    wall: float | None,
    note: str,
    detail: list[str],
) -> Row:
    """A count-of-mismatches row: PASS at zero, else FAIL; the first mismatches go in the note."""
    if n_bad:
        note = f"{note}; {n_bad} mismatched, e.g. " + "; ".join(detail[:3])
    return Row(ctx.id, family, check, reference, "PASS" if n_bad == 0 else "FAIL", n, float(n_bad), 0.0, wall, note)


# ---------------------------------------------------------------- Ne and lineage


def reference_ids(ctx: CaseContext, reference: str, final_generation: int | None) -> np.ndarray:
    """The ids of a named reference subpopulation: target rows, all rows, or pg's final cohort."""
    if reference == "target":
        return ctx.ped.id[ctx.ped.extra["target"] == 1]
    if reference == "all":
        return ctx.ped.id
    if reference == "final_cohort":
        return ctx.ped.id[np.asarray(ctx.graph.depth) == final_generation]
    raise ValueError(f"unknown reference {reference!r}")


def ne_family(ctx: CaseContext, cfg: dict[str, Any], rng: np.random.Generator) -> list[Row]:
    """Ne and lineage statistics against purgeR, rerun live, with each published value as an INFO row."""
    del rng
    try:
        ltc = ne_long_term_contributions(ctx.graph)
        final, no_estimate = (None, ltc.no_estimate_code) if ltc.no_estimate_code else (int(ltc.final_generation), None)
    except MissingMetadataError as err:
        # Raised, not returned as a no-estimate code, for one-parent rows.
        ltc, final, no_estimate = None, None, str(err)
    tol = cfg["tolerances"]
    tasks, pg_values, rows, scored = [], {}, [], []
    for k, check in enumerate(ctx.ne_checks):
        name, stat, ref = f"t{k}", check["stat"], check["reference"]
        label = f"{stat}, reference = {ref}"
        if "gap" in check:
            rows.append(
                Row(ctx.id, "ne", label, "purgeR", "GAP", note=f"{check['gap']}: pedigree-graph has no such estimator")
            )
        elif ref == "final_cohort" and final is None:
            rows.append(Row(ctx.id, "ne", label, "purgeR", "GAP", note=f"G3: pg gives no estimate ({no_estimate})"))
        else:
            ids = reference_ids(ctx, ref, final)
            path = ctx.work / f"reference.{name}.i32"
            ids.astype("<i4").tofile(path)
            tasks.append({"name": name, "stat": stat, "reference": str(path)})
            if stat == "ne_idf_t1":
                pg_values[name] = float(ne_individual_delta_f(ctx.graph, reference=ids - 1).ne_unrelated_founders)
            elif stat == "fe":
                if ref != "final_cohort":
                    raise ValueError(f"{ctx.id}: pg's fe is fixed to its final cohort, not {ref!r}")
                pg_values[name] = float(ltc.n_effective_founders)
            scored.append((name, check, label))
        if "published" in check:
            rows.append(
                Row(
                    ctx.id,
                    "ne",
                    f"{label}: published value",
                    "published",
                    "INFO",
                    note=f"{check['published']} ({check['source']})",
                )
            )
    if not tasks:
        return rows
    try:
        call = run_r("oracles/purger_ne.R", "purger_ne", ctx.oracle_ped, ctx.work, {"tasks": tasks}, ctx.budget)
    except (RuntimeError, BudgetExceeded) as err:
        status = "SKIP" if isinstance(err, BudgetExceeded) else "ERROR"
        return rows + [Row(ctx.id, "ne", label, "purgeR", status, note=str(err)) for _, _, label in scored]
    ctx.versions["purger_ne"] = call.versions
    for name, check, label in scored:
        ref_value = float(call.outputs[name][0])
        rel = tol["ne_relative"] if check["stat"] == "ne_idf_t1" else tol["fe_relative"]
        row = compare(
            ctx,
            "ne",
            label,
            "purgeR",
            np.array([pg_values[name]]),
            np.array([ref_value]),
            rel * abs(ref_value),
            call.wall_s,
        )
        row.note = f"pg {pg_values[name]:.10g}, purgeR {ref_value:.10g}; {row.note}".rstrip("; ")
        if "published" in check:
            row.note += f"; published {check['published']}"
        rows.append(row)
    return rows


FAMILIES = {"kinship": kinship_family, "classification": classification_family, "ne": ne_family}


# ---------------------------------------------------------------- results


def write_results(rows: list[Row], versions: dict[str, str]) -> str:
    """Write results/results.md and results/results.tsv; return the totals line."""
    RESULTS.mkdir(exist_ok=True)
    counts = {s: sum(r.status == s for r in rows) for s in STATUSES}
    totals = " · ".join(f"{s} {n}" for s, n in counts.items())
    fields = ["case", "family", "check", "reference", "status", "n", "max_abs_diff", "tol", "wall_s", "note"]
    with (RESULTS / "results.tsv").open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(fields)
        for r in rows:
            writer.writerow(
                [_fmt(getattr(r, f)) if isinstance(getattr(r, f), float) else getattr(r, f) for f in fields]
            )
    lines = [
        "# pedigree-graph against other software",
        "",
        "Written by `pixi run harness`; do not edit. Every non-PASS row is explained in",
        "[`../differences.md`](../differences.md) or [`../status.md`](../status.md).",
        "",
        f"**{totals}**",
        "",
        "Versions: " + ", ".join(f"{k} {v}" for k, v in versions.items()),
        "",
        "| " + " | ".join(fields) + " |",
        "|" + "---|" * len(fields),
    ]
    lines += ["| " + " | ".join(_fmt(getattr(r, f)) for f in fields) + " |" for r in rows]
    (RESULTS / "results.md").write_text("\n".join(lines) + "\n")
    return totals


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--install-r", action="store_true", help="install the pinned R tarballs and exit")
    parser.add_argument("--preflight", action="store_true", help="check the pin and load every oracle, then exit")
    parser.add_argument("--only", help="comma-separated case ids")
    args = parser.parse_args()
    if args.install_r:
        install_r()
        return 0
    versions = preflight()
    if args.preflight:
        for name, v in versions.items():
            print(f"{name}\t{v}")
        return 0
    cfg = yaml.safe_load((ROOT / "cases.yaml").read_text())
    only = set(args.only.split(",")) if args.only else None
    rows: list[Row] = []
    for case in cfg["cases"]:
        if only and case["id"] not in only:
            continue
        work = WORK / case["id"]
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        started = time.perf_counter()
        try:
            ped = load(case["input"], work)
        except (ValueError, subprocess.CalledProcessError) as err:
            rows.append(Row(case["id"], "input", "load", "", "ERROR", note=str(err)))
            continue
        try:
            oracle_ped, refused = ped.with_role_sex(), ""
        except ValueError as err:
            oracle_ped, refused = ped, str(err)
        ctx = CaseContext(
            case["id"],
            ped,
            ped.graph(),
            oracle_ped,
            refused,
            work,
            cfg["budget"],
            case.get("expect", []),
            case.get("ne", []),
        )
        # The families of a case run at once, each with its own seeded stream,
        # so no family's sample depends on another's or on thread timing.
        with ThreadPoolExecutor(max_workers=len(case["families"])) as pool:
            jobs = [
                pool.submit(FAMILIES[f], ctx, cfg, np.random.default_rng([cfg["seed"], list(FAMILIES).index(f)]))
                for f in case["families"]
            ]
            for job in jobs:
                rows += job.result()
        print(f"{case['id']}: N = {ped.n}, {time.perf_counter() - started:.1f} s", flush=True)
    if not only:
        rows += [
            Row("(all)", "ne", name, "purgeR, visPedigree", "GAP", note=f"G2: {why}")
            for name, why in cfg["ne_gaps"].items()
        ]
    totals = write_results(rows, versions)
    print(totals)
    return 1 if any(r.status in ("FAIL", "ERROR") for r in rows) else 0


if __name__ == "__main__":
    sys.exit(main())
