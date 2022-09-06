"""
This script is intended to be invoked by the db.sh script.
"""

import logging
import os
import sys
from argparse import (
    ArgumentParser,
    Namespace,
)

sys.path.insert(1, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "lib")))

from galaxy.model.migrations.dbscript import DbScript

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


def exec_upgrade(args: Namespace) -> None:
    # TODO this might need to be done twice: once for each branch.
    # because we upgrade tsi implicitly to hide complexity.
    #breakpoint()
    _exec_command("upgrade", args)


def exec_downgrade(args: Namespace) -> None:
    _exec_command("downgrade", args)


def exec_revision(args: Namespace) -> None:
    _exec_command("revision", args)


def exec_version(args: Namespace) -> None:
    _exec_command("version", args)


def exec_dbversion(args: Namespace) -> None:
    _exec_command("dbversion", args)


def exec_history(args: Namespace) -> None:
    _exec_command("history", args)


def exec_show(args: Namespace) -> None:
    _exec_command("show", args)


def _exec_command(command, args):
    dbscript = DbScript(args.config)
    getattr(dbscript, command)(args)


def main() -> None:
    def add_parser(command, func, help, aliases=None, parents=None):
        aliases = aliases or []
        parents = parents or []
        parser = subparsers.add_parser(command, aliases=aliases, help=help, parents=parents)
        parser.set_defaults(func=func)
        return parser

    config_arg_parser = ArgumentParser(add_help=False)
    # TODO: after refactoring legacy scripts, this can be changed to "-c, --config"
    config_arg_parser.add_argument("--galaxy-config", help="Alternate Galaxy configuration file", dest="config")

    verbose_arg_parser = ArgumentParser(add_help=False)
    verbose_arg_parser.add_argument("-v", "--verbose", action="store_true", help="Display more detailed output")

    sql_arg_parser = ArgumentParser(add_help=False)
    sql_arg_parser.add_argument(
        "--sql",
        action="store_true",
        help="Don't emit SQL to database - dump to standard output/file instead. See Alembic docs on offline mode.",
    )

    parser = ArgumentParser(
        description="Common database schema migration operations",
        epilog="Note: these operations are applied to the Galaxy model only (stored in the `gxy` branch)."
        " For migrating the `tsi` branch, use the `run_alembic.sh` script.",
    )

    subparsers = parser.add_subparsers(required=True)

    upgrade_cmd_parser = add_parser(
        "upgrade",
        exec_upgrade,
        "Upgrade to a later version",
        aliases=["u"],
        parents=[config_arg_parser, sql_arg_parser],
    )
    upgrade_cmd_parser.add_argument("revision", help="Revision identifier", nargs="?", default="heads")

    downgrade_cmd_parser = add_parser(
        "downgrade",
        exec_downgrade,
        "Revert to a previous version",
        aliases=["d"],
        parents=[config_arg_parser, sql_arg_parser],
    )
    downgrade_cmd_parser.add_argument("revision", help="Revision identifier")

    add_parser(
        "version",
        exec_version,
        "Show the head revision in the migrations script directory",
        aliases=["v"],
        parents=[config_arg_parser, verbose_arg_parser],
    )

    add_parser(
        "dbversion",
        exec_dbversion,
        "Show the current revision for Galaxy's database",
        aliases=["dbv"],
        parents=[config_arg_parser, verbose_arg_parser],
    )

    history_cmd_parser = add_parser(
        "history",
        exec_history,
        "List revision scripts in chronological order",
        parents=[config_arg_parser, verbose_arg_parser],
    )
    history_cmd_parser.add_argument("-i", "--indicate-current", help="Indicate current revision", action="store_true")

    show_cmd_parser = add_parser(
        "show",
        help="Show the revision(s) denoted by the given symbol",
        parents=[config_arg_parser],
        func=exec_show,
    )
    show_cmd_parser.add_argument("revision", help="Revision identifier")

    revision_cmd_parser = add_parser(
        "revision", aliases=["r"], help="Create a new revision file", parents=[config_arg_parser], func=exec_revision
    )
    revision_cmd_parser.add_argument("-m", "--message", help="Message string to use with 'revision'", required=True)
    revision_cmd_parser.add_argument("--rev-id", help="Specify a revision id instead of generating one")

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
