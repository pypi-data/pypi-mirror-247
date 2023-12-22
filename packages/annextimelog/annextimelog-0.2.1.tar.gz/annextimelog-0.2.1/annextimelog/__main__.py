# system modules
import time
import collections
import uuid
import os
import json
import re
import textwrap
import sys
import shlex
import logging
import subprocess
import argparse
import datetime
from datetime import datetime as dt
from pathlib import Path

# internal modules
from annextimelog.event import Event
from annextimelog.log import stdout, stderr
from annextimelog.run import run, get_repo_root
from annextimelog import utils

# external modules
import rich
from rich.logging import RichHandler
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table
from rich.pretty import Pretty
from rich.text import Text
from rich import box

logger = logging.getLogger(__name__)


def git_cmd_handler(args, other_args):
    result = run(subprocess.Popen, ["git", "-C", str(args.repo)] + other_args)
    result.wait()
    sys.exit(result.returncode)


def sync_cmd_handler(args, other_args):
    if logger.getEffectiveLevel() < logging.DEBUG:
        with run(
            subprocess.Popen, ["git", "-C", args.repo, "annex", "assist"]
        ) as process:
            process.wait()
            sys.exit(process.returncode)
    else:
        with stderr.status("Syncing..."):
            result = run(subprocess.run, ["git", "-C", args.repo, "annex", "assist"])
    if result.returncode or result.stderr:
        if result.returncode:
            logger.error(f"Syncing failed according to git annex.")
        if result.stderr:
            logger.warning(
                f"git annex returned some error messages. "
                f"This might be harmless, maybe try again (a couple of times)."
            )
        sys.exit(1)
    else:
        logger.info(f"✅ Syncing finished")
    sys.exit(result.returncode)


def track_cmd_handler(args, other_args):
    event = Event(repo=args.repo)
    for i, arg in enumerate(other_args, start=1):
        if t := Event.parse_date(arg):
            logger.debug(f"Interpreted argument #{i} {arg!r} as {Event.timeformat(t)}")
            if event.start is None:
                event.start = t
            elif event.end is None:
                event.end = t
            else:
                logger.warning(
                    f"Ignoring argument #{i} {arg!r}. "
                    f"Looks like a time but we already have two times {event.start = }, {event.end = }."
                )
            continue
        if m := re.search(r"^@(.*)$", arg.strip()):
            location = m.group(1).strip()
            logger.debug(f"argument #{i} {arg!r} means {location = !r}")
            event.location.add(location)
            continue
        if m := re.search(r"^:(.*)$", arg.strip()):
            note = m.group(1).strip()
            logger.debug(f"argument #{i} {arg!r} is a note {note = !r}")
            if event.note:
                logger.warning(f"Overwriting previous note {note!r}")
            event.note = note
            continue
        if m := re.search(r"^=(.*)$", arg.strip()):
            title = m.group(1).strip()
            logger.debug(f"argument #{i} {arg!r} is a {title = !r}")
            if event.title:
                logger.warning(f"Overwriting previous title {title!r}")
            event.title = title
            continue
        if m := re.search(r"(?P<field>\S+?)(?P<operator>[+]?)=(?P<value>.*)", arg):
            field, operator, value = m.groups()
            if operator.startswith("+"):
                logger.debug(
                    f"argument #{i} {arg!r} adds {value!r} to metadata field {field!r}"
                )
                event.fields[field].add(value)
            else:
                logger.debug(
                    f"argument #{i} {arg!r} sets metadata field {field!r} to (only) {value!r}"
                )
                event.fields[field] = {value}
            continue
        logger.debug(f"argument #{i} {arg!r} is a tag")
        event.tags.add(arg)
    if not (event.start and event.end):
        logger.critical(
            f"Currently, 'annextimelog track' can only record events with exactly two given time bounds. "
            f"This will change in the future."
        )
        sys.exit(1)
    if logger.getEffectiveLevel() < logging.DEBUG:
        logger.debug(f"Event before saving:")
        stderr.print(event.to_rich())
    # make the file
    event.store()
    cmd = ["git", "-C", args.repo, "annex", "metadata", "--key", event.key]
    cmd.extend(["--set", f"start={event.timeformat(event.start)}"])
    cmd.extend(["--set", f"end={event.timeformat(event.end)}"])
    if event.title:
        cmd.extend(["--set", f"title={event.title}"])
    if event.note:
        cmd.extend(["--set", f"note={event.note}"])
    for tag in event.tags:
        cmd.extend(["--tag", tag])
    for location in event.location:
        cmd.extend(["--set", f"location+={location}"])
    for field, values in event.fields.items():
        for value in values:
            cmd.extend(["--set", f"{field}+={value}"])
    if run(subprocess.run, cmd).returncode:
        logger.error(
            f"Something went wrong setting annex metadata on event {event.id} key {event.key!r}"
        )
    if logger.getEffectiveLevel() <= logging.DEBUG and args.output_format not in (
        "rich",
        "console",
    ):
        logger.debug(f"Event after saving:")
        stderr.print(event.to_rich())
    # output event
    stdout.print(getattr(event, f"to_{args.output_format}", event.to_rich)())


def summary_cmd_handler(args, other_args):
    if other_args:
        logger.warning(f"Ignoring other arguments {other_args}")
    with logger.console.status(f"Querying metadata..."):
        result = run(
            subprocess.run, ["git", "-C", args.repo, "annex", "metadata", "--json"]
        )
    infos = dict()
    paths = collections.defaultdict(set)
    for info in utils.from_jsonlines(result.stdout):
        path = Path(info.get("input", [None])[0])
        infos[(info.get("key"), path.stem)] = info.get("fields", dict())
        paths[info.get("key")].add(path)
    for (key, id), fields in infos.items():
        event = Event(
            repo=args.repo,
            id=id,
            key=key,
            fields={
                k: set(v)
                for k, v in fields.items()
                if not (k.endswith("-lastchanged") or k in ["lastchanged"])
            },
        )
        logger.debug(f"{event = }")
        stdout.print(getattr(event, f"to_{args.output_format}", event.to_rich)())
    if not infos:
        logger.info(
            f"😴 There are no tracked events yet. Add some with 'annextimelog track ...'"
        )


parser = argparse.ArgumentParser(
    description="⏱️ Time tracker based on Git Annex",
    prog="annextimelog",
    formatter_class=argparse.RawDescriptionHelpFormatter,
)

datagroup = parser.add_argument_group(title="Data")
datagroup.add_argument(
    "--repo",
    type=Path,
    default=(
        default := Path(
            os.environ.get("ANNEXTIMELOGREPO")
            or Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
            / "annextimelog"
        )
    ),
    help=f"Backend repository to use. "
    f"Defaults to $ANNEXTIMELOG_REPO or $XDG_DATA_HOME/annextimelog ({str(default)})",
)

parser.add_argument(
    "--force",
    action="store_true",
    help="Just do it. Ignore potential data loss.",
)

outputgroup = parser.add_argument_group(
    title="Output", description="Options changing output behaviour"
)
outputgroup.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="verbose output. More -v ⮕ more output",
)
outputgroup.add_argument(
    "-q",
    "--quiet",
    action="count",
    default=0,
    help="less output. More -q ⮕ less output",
)
outputgroup.add_argument(
    "-O",
    "--output-format",
    choices={"rich", "console", "json", "timeclock"},
    default=(default := "console"),
    help="Select output format. Defaults to {default!r}.",
)


subparsers = parser.add_subparsers(title="Subcommands", dest="subcommand")
gitparser = subparsers.add_parser(
    "git", help="Access the underlying git repository", add_help=False
)
gitparser.set_defaults(func=git_cmd_handler)
syncparser = subparsers.add_parser(
    "sync",
    help="sync data",
    description=textwrap.dedent(
        """
    Sync data with configured remotes.
    """
    ).strip(),
    aliases=["sy"],
)
syncparser.set_defaults(func=sync_cmd_handler)
trackparser = subparsers.add_parser(
    "track",
    help="record a time period",
    description=textwrap.dedent(
        """
    Record a time period.

    """
    ).strip(),
    aliases=["tr"],
)
trackparser.set_defaults(func=track_cmd_handler)
summaryparser = subparsers.add_parser(
    "summary",
    help="show a summary of tracked periods",
    description=textwrap.dedent(
        """
    Show a summary of tracked periods

    """
    ).strip(),
    aliases=["su"],
)
summaryparser.set_defaults(func=summary_cmd_handler)


def cli(args=None):
    args, other_args = parser.parse_known_args(args=args)

    logging.basicConfig(
        level=(level := logging.INFO - (args.verbose - args.quiet) * 5),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=stderr,  # log to stderr
                rich_tracebacks=True,
                show_path=level < logging.DEBUG - 10,
            )
        ],
    )
    logger.debug(f"{args = }")
    logger.debug(f"{other_args = }")

    if args.repo.exists() and not args.repo.is_dir():
        logger.critical(f"{args.repo} exists but is not a directory.")
        sys.exit(1)

    if args.repo.exists():
        logger.debug(f"{args.repo} exists")
        if repo_root := get_repo_root(args.repo):
            if repo_root.resolve() != args.repo.resolve():
                logger.critical(
                    f"There's something funny with {args.repo}: git says the repo root is {repo_root}. "
                )
                sys.exit(1)
        else:
            logger.critical(f"{args.repo} exists but is no git repository. 🤔")
            sys.exit(1)
    else:
        if not args.repo.parent.exists():
            logger.info(f"📁 Creating {args.repo.parent}")
            args.repo.parent.mkdir(parent=True, exist_ok=True)
        logger.info(f"Making a git repository at {args.repo}")
        result = run(
            subprocess.run, ["git", "init", str(args.repo)], capture_output=True
        )
        if result.returncode:
            logger.error(f"Couldn't make git repository at {args.repo}")
            sys.exit(1)

    # ✅ at this point, args.repo is a git repository
    annex_uuid = None
    logger.debug(f"Making sure {args.repo} is a git annex repository")
    if not (
        result := run(
            subprocess.run,
            ["git", "-C", args.repo, "config", "annex.uuid"],
            title=f"get git annex uuid for {args.repo}",
            debug_on_error=False,
        )
    ).returncode:
        annex_uuid = result.stdout.strip()
    if not annex_uuid:
        logger.debug(f"{args.repo} is not a git annex repository")
        if not (
            result := run(
                subprocess.run,
                ["git", "-C", args.repo, "annex", "init"],
                title=f"add an annex to {args.repo}",
            )
        ).returncode:
            logger.info(f"Added an annex to {args.repo}")
        else:
            logger.critical(f"Couldn't add an annex to {args.repo}")
            sys.exit(1)

    # ✅ at this point, args.repo is a git annex repository

    result = run(subprocess.run, ["git", "-C", args.repo, "status", "--porcelain"])
    if result.returncode or result.stdout or result.stderr:
        logger.warning(
            f"🐛 The repo {args.repo} is not clean. "
            f"This should not happen. Committing away the following changes:"
        )
        result = run(subprocess.Popen, ["git", "-C", args.repo, "status"])
        with logger.console.status("Committing..."):
            result = run(subprocess.run, ["git", "-C", args.repo, "annex", "add"])
            result = run(subprocess.run, ["git", "-C", args.repo, "add", "-A"])
            result = run(
                subprocess.run,
                ["git", "-C", args.repo, "commit", "-m", "🤷 Leftover changes"],
            )
        result = run(subprocess.run, ["git", "-C", args.repo, "status", "--porcelain"])
        if not (result.returncode or result.stderr):
            logger.info(f"✅ Repo is now clean")
        else:
            logger.warning(f"Commiting leftover changes didn't work.")

    # handle the subcommand
    # (when a subcommand is specified, the 'func' default is set to a callback function)
    if not getattr(args, "func", None):
        # default to 'atl summary'
        args.func = summary_cmd_handler
    try:
        args.func(args, other_args)
    finally:
        result = run(subprocess.run, ["git", "-C", args.repo, "status", "--porcelain"])
        if result.returncode or result.stdout or result.stderr:
            logger.warning(
                f"🐛 This command left the repo {args.repo} in an unclean state. "
                f"This should not happen. Consider investigating. "
                f"The next time you run any 'annextimelog' command, these changes will be committed."
            )
            result = run(subprocess.Popen, ["git", "-C", args.repo, "status"])


if __name__ == "__main__":
    cli()
