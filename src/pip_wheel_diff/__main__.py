# SPDX-FileCopyrightText: 2023-present Stéphane Bidoul <stephane.bidoul@gmail.com>
#
# SPDX-License-Identifier: MIT

import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def _build_wheel(spec: str, path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = ["pip", "wheel", "--use-pep517", "--no-deps", spec, "--wheel-dir", tmpdir]
        subprocess.run(cmd, check=True)  # noqa: S603
        wheelfile = next(Path(tmpdir).glob("*.whl"))
        zipfile.ZipFile(wheelfile).extractall(path)


def _clean_unpacked_wheel(path: Path) -> None:
    distinfo_path = next(path.glob("*.dist-info"))
    # remove RECORD file, it's not useful for diffing
    distinfo_path.joinpath("RECORD").unlink()
    # rename dist-info to name without version for comparability
    name = distinfo_path.stem.split("-")[0]
    distinfo_path.rename(path / f"{name}.dist-info")


def _diff_tool(v1path: Path, v2path: Path):
    if shutil.which("meld"):
        cmd = ["meld", v1path, v2path]
    else:
        cmd = ["diff", "-r", v1path, v2path]
    subprocess.run(cmd, check=True)  # noqa: S603


def main(spec1: str, spec2: str):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            # build 1
            v1path = tmppath / "v1"
            v1path.mkdir()
            _build_wheel(spec1, v1path)
            _clean_unpacked_wheel(v1path)
            # build 2
            v2path = tmppath / "v2"
            v2path.mkdir()
            _build_wheel(spec2, v2path)
            _clean_unpacked_wheel(v2path)
            # diff
            _diff_tool(v1path, v2path)
    except subprocess.CalledProcessError as e:
        return e.returncode
    return 0


sys.exit(main(sys.argv[1], sys.argv[2]))
