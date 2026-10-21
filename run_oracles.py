"""Check pedigree-graph's two bindings against the same methods in other software.

Step 1 of the plan: R setup and the preflight. The cases come later.

    python run_oracles.py --install-r   # install pedigreegraph.pin and oracles.lock into .r-lib/
    python run_oracles.py --preflight   # both bindings report the pin; every oracle loads
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from importlib.metadata import version as dist_version
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
R_LIB = ROOT / ".r-lib"
DOWNLOAD = R_LIB / "_download"
#: Set to a local pedigreegraph source tarball to check a checkout (not committed).
OVERRIDE_ENV = "PGV_R_TARBALL"
#: Every oracle package the R scripts load, conda-forge and CRAN alike.
ORACLES = ("kinship2", "GENLIB", "ribd", "verbalisr", "nadiv", "pedigreeTools", "AGHmatrix", "purgeR", "visPedigree")


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
        # No binding exports its core rev yet, so the override is unchecked (plan D2).
        print(f"preflight: override {os.environ[OVERRIDE_ENV]}; core rev UNCHECKED")
    elif {versions["pedigree-graph (Python)"], r_binding} != {pin}:
        sys.exit(
            f"preflight: pinned {pin}, but Python {versions['pedigree-graph (Python)']} and R {r_binding};"
            " run `pixi install` and `pixi run r-setup`"
        )
    return versions


def main() -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--install-r", action="store_true", help="install the pinned R tarballs and exit")
    parser.add_argument("--preflight", action="store_true", help="check the pin and load every oracle, then exit")
    args = parser.parse_args()
    if args.install_r:
        install_r()
        return 0
    if args.preflight:
        for name, v in preflight().items():
            print(f"{name}\t{v}")
        return 0
    parser.error("no cases yet; use --install-r or --preflight")
    return 2


if __name__ == "__main__":
    sys.exit(main())
