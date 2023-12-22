# Copyright (C) 2023 twyleg
import logging
import subprocess

from typing import List


def run(command: List[str]):
    logging.debug("Running command: %s", command)
    subprocess.run(command)
