# SPDX-FileCopyrightText: 2023-present Stéphane Bidoul <stephane.bidoul@gmail.com>
#
# SPDX-License-Identifier: MIT

import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


def has_pip() -> bool:
    return bool(shutil.which("pip"))


def obtain_with_pip(spec: str, path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = ["pip", "wheel", "--use-pep517", "--no-deps", spec, "--wheel-dir", tmpdir]
        subprocess.run(cmd, check=True)  # noqa: S603
        wheelfile = next(Path(tmpdir).glob("*.whl"))
        zipfile.ZipFile(wheelfile).extractall(path)
