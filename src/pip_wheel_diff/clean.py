# SPDX-FileCopyrightText: 2023-present Stéphane Bidoul <stephane.bidoul@gmail.com>
#
# SPDX-License-Identifier: MIT

from pathlib import Path


def clean_unpacked_wheel(path: Path) -> None:
    distinfo_path = next(path.glob("*.dist-info"))
    # remove metadata files that are not useful for diffing
    distinfo_path.joinpath("RECORD").unlink(missing_ok=True)
    distinfo_path.joinpath("direct_url.json").unlink(missing_ok=True)
    distinfo_path.joinpath("uv_cache.json").unlink(missing_ok=True)
    # rename dist-info to name without version for comparability
    name = distinfo_path.stem.split("-")[0]
    distinfo_path.rename(path / f"{name}.dist-info")
