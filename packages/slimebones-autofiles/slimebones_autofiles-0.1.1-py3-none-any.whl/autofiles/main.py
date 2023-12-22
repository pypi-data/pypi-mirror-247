import argparse
from pathlib import Path

from autofiles.cli_action import AutoCLIAction
from autofiles.utils import AutoUtils


def main():
    parser = argparse.ArgumentParser()
    action_subparser = parser.add_subparsers(dest="action")

    clean_parser = action_subparser.add_parser("clean")
    clean_parser.add_argument(
        "targetpath", type=Path,
    )


    args = parser.parse_args()

    match args.action:
        case AutoCLIAction.Clean.value:
            AutoUtils.clean(args.targetpath)
        case _:
            raise ValueError(f"action {args.action} not found")


if __name__ == "__main__":
    main()
