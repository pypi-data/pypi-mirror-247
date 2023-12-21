# system modules
import os
import sys
import shlex
import logging
import subprocess
import argparse
from pathlib import Path

# external modules
import rich
from rich.logging import RichHandler
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.columns import Columns

console = Console()

logger = logging.getLogger(__name__)


def show_process_result(result):
    columns = []
    if result.stdout:
        columns.append(
            Panel(
                Syntax(result.stdout.rstrip(), "txt", line_numbers=True),
                title="📢 STDOUT",
                padding=0,
            )
        )
    if result.stderr:
        columns.append(
            Panel(
                Syntax(result.stderr.rstrip(), "txt", line_numbers=True),
                title="⚠️  STDERR",
                padding=0,
            )
        )
    if not columns:
        columns.append("*no output*")
    kwargs = dict()
    if logger.getEffectiveLevel() < logging.DEBUG - 10:
        kwargs["title"] = getattr(result, "title", None) or shlex.join(result.args)
    console.print(
        Columns(columns, equal=True, expand=True, **kwargs),
    )


def run(runner, cmdline, return_error=True, title=None, **kwargs):
    """
    Run a given ``cmdline`` with a :mod:`subprocess` runner (e.g
    :any:`subprocess.check_output`) with passed command-line arguments.
    If ``return_error`` is ``True``, a raised
    :any:`subprocess.CalledProcessError` is caught and returned. If it's
    ``None``, just ``None`` is returned. Otherwise the exception is bubbled up.
    """
    cmdline = list(map(str, cmdline))
    if logger.getEffectiveLevel() < logging.DEBUG:
        lines = []
        if title:
            lines.append(f"# {title}")
        lines.append(
            f"""# 🚀 Executing (📋 you could copy-paste this) in 📁 {kwargs.get("cwd") or Path.cwd()}:"""
        )
        lines.append(shlex.join(cmdline))
        console.print(
            Syntax(
                "\n".join(lines),
                "bash",
                line_numbers=False,
                indent_guides=False,
                word_wrap=True,
                padding=0,
            )
        )
    if runner is subprocess.run:
        kwargs.setdefault("capture_output", True)
        kwargs.setdefault("check", False)
    try:
        result = runner(
            cmdline, **{**dict(text=True, encoding="utf-8", errors="ignore"), **kwargs}
        )
    except subprocess.CalledProcessError as e:
        if return_error is True:
            return e
        elif return_error is None:
            return None
        else:
            raise
    result.title = title
    if kwargs.get("capture_output") and logger.getEffectiveLevel() < logging.DEBUG - 5:
        show_process_result(result)
    return result


def get_repo_root(path=Path(".")):
    logger.debug(f"🔎 Finding where the containing git repo root is for path {path}")
    result = run(
        subprocess.run,
        ["git", "-C", Path(path), "rev-parse", "--show-toplevel"],
        title=f"find git repo root for {path}",
    )
    if result.returncode:
        return None
    return Path(result.stdout.rstrip("\n").rstrip("\r"))


parser = argparse.ArgumentParser(description="Time tracker based on Git Annex")

datagroup = parser.add_argument_group(title="Data")
datagroup.add_argument(
    "--repo",
    type=Path,
    default=(
        default := Path(
            os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")
        )
        / "annextimelog"
    ),
    help=f"Backend repository to use. Defaults to $XDG_DATA_HOME/annextimelog ({str(default)})",
)

parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="verbose output. More -v ⮕ more output",
)
parser.add_argument(
    "-q",
    "--quiet",
    action="count",
    default=0,
    help="less output. More -q ⮕ less output",
)
parser.add_argument(
    "--force",
    action="store_true",
    help="Just do it. Ignore potential data loss.",
)


def cli():
    args = parser.parse_args()

    logging.basicConfig(
        level=(level := logging.INFO - (args.verbose - args.quiet) * 5),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                show_path=level < logging.DEBUG - 10,
            )
        ],
    )

    if args.repo.exists() and not args.repo.is_dir():
        logger.critical(f"{args.repo} exists but is not a directory.")
        sys.exit(1)

    if args.repo.exists():
        logger.debug(f"{args.repo} exists")
        if repo_root := get_repo_root(args.repo):
            if repo_root.resolve() != args.repo.resolve():
                logger.critical(
                    f"There's something funny with {str(args.repo)!r}: git says the repo root is {str(repo_root)!r}. "
                )
                sys.exit(1)
        else:
            logger.critical(f"{args.repo} exists but is no git repository. 🤔")
            sys.exit(1)
    else:
        if not args.repo.parent.exists():
            logger.info(f"📁 Creating {str(args.repo.parent)!r}")
            args.repo.parent.mkdir(parent=True, exist_ok=True)
        logger.info(f"Making a git repository at {str(args.repo)!r}")
        result = run(
            subprocess.run, ["git", "init", str(args.repo)], capture_output=True
        )
        if result.returncode:
            logger.error(f"Couldn't make git repository at {str(args.repo)!r}")
            sys.exit(1)

    # ✅ at this point, args.repo is a git repository
    annex_uuid = None
    logger.debug(f"Making sure {args.repo} is a git annex repository")
    if not (
        result := run(
            subprocess.run,
            ["git", "-C", args.repo, "config", "annex.uuid"],
            title=f"get git annex uuid for {args.repo}",
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

    logger.info(f"😪 More is not implemented yet...")


if __name__ == "__main__":
    cli()
