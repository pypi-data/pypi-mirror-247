# Copyright (C) 2023 twyleg
import logging

from pathlib import Path
from typing import List
from twyleg_kicad_utils.process import run


def build(working_dir: Path, output_dir: Path, targets: List[str]):

    logging.info("Output directory: %s", output_dir)

    if working_dir in output_dir.parents:
        run(f"podman run \
            -v {working_dir}/:/root/project/ \
            -w /root/project \
            ghcr.io/inti-cmnb/kicad7_auto_full:latest \
            kibot -d {output_dir.relative_to(working_dir)}".split() + targets
        )
    else:
        logging.error("Output dir outside of working dir. Unable to access output dir in container.")
