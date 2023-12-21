# Copyright (C) 2023 twyleg
import subprocess


def diff(port: int, clean=False) -> None:
    subprocess.run(
        f"podman run -it \
        -v./:/root/project \
        -w /root/project \
        -p {port}:8282 \
        docker.io/twyleg/kicad_toolchain:latest \
        kiri -p 8282 {'-r' if clean else ''}".split()
    )