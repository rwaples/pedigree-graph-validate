"""Write oracles.lock: the CRAN source tarballs the oracles need, in install order.

Resolves Depends, Imports and LinkingTo of each root package (crandb), and
splits the closure in two: packages conda-forge builds for r-base 4.5 are
printed for pixi.toml's [dependencies]; the rest are downloaded once, hashed,
and written to oracles.lock with the dependencies before the dependents.
Review the diff before committing; run_oracles.py --install-r installs it.

    python tools/lock_oracles.py
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ROOTS = ("ribd", "verbalisr", "nadiv", "pedigreeTools", "AGHmatrix", "purgeR", "visPedigree")
#: Shipped with every R build.
BASE = frozenset(
    [
        "R",
        "base",
        "compiler",
        "datasets",
        "graphics",
        "grDevices",
        "grid",
        "methods",
        "parallel",
        "splines",
        "stats",
        "stats4",
        "tcltk",
        "tools",
        "utils",
    ]
)
CRAN = "https://cran.r-project.org/src/contrib"


def _get(url: str) -> bytes:
    # crandb and anaconda.org answer 403 to urllib's default User-Agent.
    request = urllib.request.Request(url, headers={"User-Agent": "pedigree-graph-validate"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def crandb(name: str) -> dict:
    """The current CRAN release record of `name`."""
    return json.loads(_get(f"https://crandb.r-pkg.org/{name}"))


def deps(record: dict) -> list[str]:
    """Hard dependencies: Depends, Imports, LinkingTo."""
    out: list[str] = []
    for key in ("Depends", "Imports", "LinkingTo"):
        out.extend(record.get(key, {}))
    return [d for d in out if d not in BASE]


def on_conda_forge(name: str) -> str | None:
    """The latest conda-forge version with an r-base 4.5 build, or None."""
    try:
        meta = json.loads(_get(f"https://api.anaconda.org/package/conda-forge/r-{name.lower()}"))
    except urllib.error.HTTPError:
        return None
    versions = [
        f["version"]
        for f in meta.get("files", [])
        if f["attrs"].get("subdir") in ("linux-64", "noarch")
        and any(re.match(r"r-base\s*>=?4\.5", d) for d in f["attrs"].get("depends", []))
    ]
    return max(versions, key=lambda v: [int(p) for p in re.findall(r"\d+", v)]) if versions else None


def tarball(name: str, version: str) -> tuple[str, str]:
    """(url, sha256) of the source tarball, current or archived."""
    for url in (f"{CRAN}/{name}_{version}.tar.gz", f"{CRAN}/Archive/{name}/{name}_{version}.tar.gz"):
        try:
            return url, hashlib.sha256(_get(url)).hexdigest()
        except urllib.error.HTTPError:
            continue
    raise SystemExit(f"no tarball for {name} {version}")


def main() -> None:
    """Resolve the closure, print the conda-forge half, write oracles.lock."""
    records: dict[str, dict] = {}
    conda: dict[str, str] = {}
    order: list[str] = []

    def visit(name: str) -> None:
        if name in records or name in conda:
            return
        if (v := on_conda_forge(name)) is not None and name not in ROOTS:
            conda[name] = v
            return
        records[name] = crandb(name)
        for d in deps(records[name]):
            visit(d)
        order.append(name)

    for name in ROOTS:
        visit(name)
    packages = []
    for name in order:
        version = records[name]["Version"]
        url, digest = tarball(name, version)
        packages.append({"name": name, "version": version, "url": url, "sha256": digest})
        print(f"cran   {name} {version}")
    for name, v in sorted(conda.items()):
        print(f"conda  r-{name.lower()} {v}")
    header = (
        "# CRAN source tarballs for the oracles, in install order (dependencies first).\n"
        "# Written by tools/lock_oracles.py; run_oracles.py --install-r refuses a\n"
        "# tarball whose sha256 differs. Dependencies on conda-forge come from pixi.toml.\n"
    )
    (ROOT / "oracles.lock").write_text(header + yaml.safe_dump({"packages": packages}, sort_keys=False))


if __name__ == "__main__":
    main()
