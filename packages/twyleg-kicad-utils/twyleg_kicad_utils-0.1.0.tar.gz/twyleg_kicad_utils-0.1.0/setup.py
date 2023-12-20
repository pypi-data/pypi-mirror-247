# Copyright (C) 2023 twyleg
import versioneer
from pathlib import Path
from setuptools import find_packages, setup


def read(relative_filepath):
    return open(Path(__file__).parent / relative_filepath).read()


def read_long_description() -> str:
    return read("README.md")


setup(
    name="twyleg_kicad_utils",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Torsten Wylegala",
    author_email="mail@twyleg.de",
    description=("Personal utilities to automate KiCad projects"),
    license="GPL 3.0",
    keywords="KiCad automation cicd",
    url="https://github.com/twyleg/twyleg_kicad_utils",
    packages=find_packages(),
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "twyleg_kicad_utils = twyleg_kicad_utils.main:main",
            "kicad_utils = twyleg_kicad_utils.main:main",
        ]
    },
)
