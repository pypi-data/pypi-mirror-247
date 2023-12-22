# Copyright (C) 2023 twyleg
import logging

from pathlib import Path
from typing import List
from twyleg_kicad_utils.process import run


def build(working_dir: Path, output_dir: Path, targets: List[str]):

    run(f"podman run \
        -v {working_dir}/:/root/project/ \
        -w /root/project \
        ghcr.io/inti-cmnb/kicad7_auto_full:latest \
        kibot -d {output_dir}".split() + targets
    )
