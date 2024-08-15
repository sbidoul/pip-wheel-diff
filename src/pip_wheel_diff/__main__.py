# SPDX-FileCopyrightText: 2023-present Stéphane Bidoul <stephane.bidoul@gmail.com>
#
# SPDX-License-Identifier: MIT

import subprocess
import sys
import tempfile
from pathlib import Path

from .clean import clean_unpacked_wheel
from .diff_tool import diff_tool
from .pip import has_pip, obtain_with_pip
from .uv import has_uv, obtain_with_uv

if has_uv():
    obtain = obtain_with_uv
elif has_pip():
    obtain = obtain_with_pip
else:
    msg = "Nor uv, nor pip were found, please install one of them."
    raise SystemExit(msg)


def main(spec1: str, spec2: str) -> int:
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            # build 1
            v1path = tmppath / "v1"
            v1path.mkdir()
            obtain(spec1, v1path)
            clean_unpacked_wheel(v1path)
            # build 2
            v2path = tmppath / "v2"
            v2path.mkdir()
            obtain(spec2, v2path)
            clean_unpacked_wheel(v2path)
            # diff
            diff_tool(v1path, v2path)
    except subprocess.CalledProcessError as e:
        return e.returncode
    return 0


sys.exit(main(sys.argv[1], sys.argv[2]))
