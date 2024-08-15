# SPDX-FileCopyrightText: 2023-present Stéphane Bidoul <stephane.bidoul@gmail.com>
#
# SPDX-License-Identifier: MIT

import shutil
import subprocess
from pathlib import Path


def diff_tool(v1path: Path, v2path: Path):
    if shutil.which("meld"):
        cmd = ["meld", v1path, v2path]
    else:
        cmd = ["diff", "-r", v1path, v2path]
    subprocess.run(cmd, check=True)  # noqa: S603
