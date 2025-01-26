# SPDX-FileCopyrightText: 2023-present Stéphane Bidoul <stephane.bidoul@gmail.com>
#
# SPDX-License-Identifier: MIT

import shutil
import subprocess
from pathlib import Path


def has_pip() -> bool:
    return bool(shutil.which("pip"))


def obtain_with_pip(spec: str, path: Path) -> None:
    cmd = ["pip", "install", "--use-pep517", "--no-deps", "--target", path, spec]
    subprocess.run(cmd, check=True)  # noqa: S603
