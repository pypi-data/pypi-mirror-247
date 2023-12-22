# Copyright (C) 2023 twyleg
import fileinput
import logging

from pathlib import Path
from enum import Enum


class SubmoduleProtocol(Enum):
    SSH = 0
    HTTPS = 1


def replace_string_in_file(filepath: Path, text_to_search: str, replacement_text: str):
    with fileinput.FileInput(filepath, inplace=True) as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end="")


def set_submodules_protocol(submodule_protocol: SubmoduleProtocol, gitmodules_file_path: Path) -> None:
    if submodule_protocol == SubmoduleProtocol.HTTPS:
        replace_string_in_file(gitmodules_file_path, "git@github.com:", "https://github.com/")
    else:
        replace_string_in_file(gitmodules_file_path, "https://github.com/", "git@github.com:")


def list_submodules(gitmodules_file_path: Path) -> None:
    with open(gitmodules_file_path, "r") as gitmodules_file:
        for line in gitmodules_file:
            logging.info("%s", line.replace("\n", ""))
