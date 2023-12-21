# Copyright (C) 2023 twyleg
import subprocess

from pathlib import Path
from typing import List


def build(working_dir: Path, output_dir: Path, targets: List[str]):

    subprocess.run(
        f"podman run \
        -v {working_dir}/:/root/project/ \
        -w /root/project \
        ghcr.io/inti-cmnb/kicad7_auto_full:latest \
        kibot -d {output_dir} -c /root/project/external/twyleg_kicad_utils/kibot/default.kibot.yaml".split() + targets
    )