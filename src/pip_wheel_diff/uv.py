# SPDX-FileCopyrightText: 2024-present Stéphane Bidoul <stephane.bidoul@gmail.com>
#
# SPDX-License-Identifier: MIT

import shutil
import subprocess
from pathlib import Path


def has_uv() -> bool:
    return bool(shutil.which("uv"))


def obtain_with_uv(spec: str, path: Path) -> None:
    cmd = ["uv", "pip", "install", "--no-deps", "--target", path, spec]
    subprocess.run(cmd, check=True)  # noqa: S603
