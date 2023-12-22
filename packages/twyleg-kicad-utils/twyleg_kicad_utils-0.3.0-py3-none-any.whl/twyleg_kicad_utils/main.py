# Copyright (C) 2023 twyleg
import sys
import argparse
import logging
import subprocess
import twyleg_kicad_utils.build
import twyleg_kicad_utils.diff

from pathlib import Path

from twyleg_kicad_utils import __version__
from twyleg_kicad_utils.submodules import SubmoduleProtocol, set_submodules_protocol, list_submodules

FORMAT = "[%(asctime)s][%(levelname)s][%(name)s]: %(message)s"


def init(args: argparse.Namespace):
    logging.error("Not yet implemented!")


def submodules(args: argparse.Namespace):
    gitmodules_file_path = Path(args.working_dir) / ".gitmodules"
    list_submodules(gitmodules_file_path)


def submodules_set_protocol(args: argparse.Namespace):
    gitmodules_file_path = Path(args.working_dir) / ".gitmodules"
    target_submodule_protocol = SubmoduleProtocol.HTTPS if "https" in args.protocol else SubmoduleProtocol.SSH

    set_submodules_protocol(target_submodule_protocol, gitmodules_file_path)


def build(args: argparse.Namespace):
    twyleg_kicad_utils.build.build(args.working_dir, args.output_dir, args.targets)


def diff(args: argparse.Namespace):
    twyleg_kicad_utils.diff.diff(args.port, args.clean)


def main():
    #
    # Top-level parser
    #
    parser = argparse.ArgumentParser(description="foo")
    parser.add_argument(
        "-v",
        "--version",
        help="Show version and exit",
        action="version",
        version=__version__,
    )

    parser.add_argument(
        "-vv",
        "--verbose",
        help="Run with verbose output.",
        action='store_true',
    )

    parser.add_argument(
        "-w", "--working_dir", help="Use a specific working directory. Default=./", type=str, default=Path.cwd()
    )

    subparsers = parser.add_subparsers(required=True, title="subcommands")

    #
    # Subcommand: init
    #
    parser_build = subparsers.add_parser("init", description="Initialize a project.")
    parser_build.set_defaults(func=init)

    #
    # Subcommand: submodules
    #
    parser_build = subparsers.add_parser("submodules", description="Manage git submodules.")
    parser_build.set_defaults(func=submodules)

    subparsers_submodules = parser_build.add_subparsers(required=False, title="subcommands")
    parser_submodules_set_protocol = subparsers_submodules.add_parser("set_protocol")
    parser_submodules_set_protocol.set_defaults(func=submodules_set_protocol)
    parser_submodules_set_protocol.add_argument(
        dest="protocol", metavar="{ssh,https}", choices=["ssh", "https"], nargs=1, help='Chose "ssh" or "https"'
    )

    #
    # Subcommand: build
    #
    parser_build = subparsers.add_parser("build", description="Build project or specific parts of it.")
    parser_build.set_defaults(func=build)

    parser_build.add_argument(
        "-o",
        "--output_dir",
        help=f"Use a specific output dir for the results. Default=./export",
        type=str,
        default=Path.cwd() / "export",
    )

    parser_build.add_argument('targets', type=str, nargs='*',
                        help='Targets to build')

    #
    # Subcommand: diff
    #
    parser_diff = subparsers.add_parser("diff", description="Git diff.")
    parser_diff.add_argument('-c', '--clean', action='store_true', help="Clean files from previous run before running again.")
    parser_diff.add_argument('-p', '--port', type=int, default=8000, help="Port to start kiri on.")
    parser_diff.set_defaults(func=diff)

    #
    # Subcommands end
    #
    args = parser.parse_args(sys.argv[1:])

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(stream=sys.stdout, format=FORMAT, level=log_level)

    logging.info("twyleg_kicad_utils started!")
    logging.info("Log level: %s", logging.getLevelName(log_level))
    logging.info("Arguments: %s", args)
    logging.info("Command: %s", args.func.__name__.replace("_", " -> "))
    logging.info("Working dir: %s", args.working_dir)
    args.func(args)


if __name__ == "__main__":
    main()
