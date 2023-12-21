[![Build status](https://github.com/twyleg/twyleg_kicad_utils/actions/workflows/tests.yaml/badge.svg)]()
[![GitHub latest commit](https://badgen.net/github/last-commit/twyleg/twyleg_kicad_utils)](https://GitHub.com/twyleg/twyleg_kicad_utils/commit/)
[![PyPI download month](https://img.shields.io/pypi/dm/twyleg_kicad_utils)](https://pypi.python.org/pypi/twyleg_kicad_utils/)
[![PyPi version](https://badgen.net/pypi/v/twyleg_kicad_utils/)](https://pypi.org/project/twyleg_kicad_utils)


# twyleg_kicad_utils

Personal utilities to automate build process for KiCad projects.

## Install

    python -m venv venv
    source venv/bin/activate
    pip install twyleg-kicad-utils

## Usage

Use the help output for detailed information:

    kicad_utils -h

### init

Init KiCad project.

    kicad_utils init

### submodules

Manage submodules like listing modules, switching protocol (HTTPS/SSH) and upgrading submpdules.

    kicad_utils submodules

### build

Build documentation and exports of KiCad project.

    kicad_utils build

### diff

Show interactive git diff based on [kiri](https://github.com/leoheck/kiri).

    kicad_utils diff

## Examples

All examples can be found in the [examples/](https://github.com/twyleg/twyleg_kicad_utils/tree/master/examples) directory.
