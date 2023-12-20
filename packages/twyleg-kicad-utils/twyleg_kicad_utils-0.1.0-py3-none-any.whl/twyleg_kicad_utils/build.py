# Copyright (C) 2023 twyleg
import subprocess

from pathlib import Path

def build_all(working_dir: Path):
    subprocess.run(
        f"podman run \
        -v {working_dir}/:/root/project/ \
        -w /root/project \
        ghcr.io/inti-cmnb/kicad7_auto_full:latest \
        kibot -c /root/project/external/twyleg_kicad_utils/kibot/default.kibot.yaml".split()
    )