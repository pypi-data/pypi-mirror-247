# Copyright (C) 2023 twyleg
import subprocess

from twyleg_kicad_utils.process import run


def diff(port: int, clean=False) -> None:
    run(
        f"podman run -it \
        -v./:/root/project \
        -w /root/project \
        -p {port}:8282 \
        docker.io/twyleg/kicad_toolchain:latest \
        kiri -p 8282 {'-r' if clean else ''}".split()
    )