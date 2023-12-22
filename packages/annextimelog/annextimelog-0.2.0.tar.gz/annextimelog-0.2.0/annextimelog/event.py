# system modules
import re
import subprocess
import locale
import logging
import textwrap
import collections
import string
import random
import datetime
from datetime import datetime as dt
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, Set, Dict

# internal modules
from annextimelog.run import run
from annextimelog import utils

# external modules
from rich.table import Table
from rich.text import Text
from rich.highlighter import ReprHighlighter, ISO8601Highlighter
from rich import box

logger = logging.getLogger(__name__)


@dataclass
class Event:
    repo: Path
    id: Optional[Path] = None
    paths: Optional[Set[Path]] = None
    key: Optional[str] = None
    fields: Optional[Dict[str, Set[str]]] = None

    SUFFIX = ".ev"

    def __post_init__(self):
        if self.id is None:
            self.id = self.random_id()
        if self.paths is None:
            self.paths = set()
        if self.fields is None:
            self.fields = collections.defaultdict(set)

    @property
    def location(self):
        if "location" not in self.fields:
            self.fields["location"] = set()
        return self.fields["location"]

    @property
    def start(self):
        if not "start" in self.fields:
            self.fields["start"] = set()
        if not (start := self.fields["start"]):
            return None
        elif len(start) > 1:
            try:
                earliest = min(filter(bool, map(self.parse_date, start)))
            except Exception as e:
                logger.error(
                    f"There are len({start}) start times for event {self!r}, but I can't determine the earliest."
                )
                self.fields["start"].clear()
                return None
            self.fields["start"].clear()
            self.fields["start"].add(earliest)
        return self.parse_date(next(iter(self.fields["start"]), None))

    @start.setter
    def start(self, value):
        if value is None:
            self.fields["start"].clear()
            return
        if d := self.parse_date(value):
            self.fields["start"].clear()
            self.fields["start"].add(d)
        else:
            logger.error(f"Couldn't interpret {value!r} as time.")
            self.fields["start"].clear()

    @property
    def end(self):
        if not "end" in self.fields:
            self.fields["end"] = set()
        if not (end := self.fields["end"]):
            return None
        elif len(end) > 1:
            try:
                latest = max(filter(bool, map(self.parse_date, end)))
            except Exception as e:
                logger.error(
                    f"There are len({end}) end times for event {self!r}, but I can't determine the earliest."
                )
                self.fields["end"].clear()
                return None
            self.fields["end"].clear()
            self.fields["end"].add(latest)
        return self.parse_date(next(iter(self.fields["end"]), None))

    @end.setter
    def end(self, value):
        if value is None:
            self.fields["end"].clear()
            return
        if d := self.parse_date(value):
            self.fields["end"].clear()
            self.fields["end"].add(d)
        else:
            logger.error(f"Couldn't interpret {value!r} as time.")
            self.fields["end"].clear()

    @property
    def note(self):
        if len(note := self.fields.get("note", set())) > 1:
            note = "\n".join(self.fields["note"])
            self.fields["note"].clear()
            self.fields["note"].add(note)
        return "\n".join(self.fields.get("note", set()))

    @note.setter
    def note(self, value):
        self.fields["note"].clear()
        self.fields["note"].add(value)

    @property
    def title(self):
        if len(title := self.fields.get("title", set())) > 1 or any(
            re.search(r"[\r\n]", t) for t in title
        ):
            title = " ".join(re.sub(r"[\r\n]+", " ", t) for t in self.fields["title"])
            self.fields["title"].clear()
            self.fields["title"].add(title)
        return "\n".join(self.fields.get("title", set()))

    @title.setter
    def title(self, value):
        value = re.sub(r"[\r\n]+", " ", str(value))
        self.fields["title"].clear()
        self.fields["title"].add(value)

    @property
    def tags(self):
        if "tag" not in self.fields:
            self.fields["tag"] = set()
        return self.fields["tag"]

    @classmethod
    def from_fields(cls, fields):
        event = cls()

    @staticmethod
    def random_id():
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))

    @staticmethod
    def parse_date(string):
        if isinstance((d := string), datetime.datetime):
            if not d.tzinfo:
                d = d.replace(tzinfo=datetime.timezone.utc)
            return d
        offset = datetime.timedelta(days=0)
        if m := re.search(r"^(?P<prefix>[yt]+)(?P<rest>.*)$", string):
            offset = datetime.timedelta(
                days=sum(dict(y=-1, t=1).get(c) for c in m.group("prefix"))
            )
            logger.debug(
                f"{string!r} starts with {m.group('prefix')!r}, so thats as an {offset = }"
            )
            string = m.group("rest")
        result = None
        for f in (
            dt.fromisoformat,
            lambda s: dt.fromisoformat(f"{dt.utcnow().strftime('%Y-%m-%d')} {s}"),
            lambda s: dt.strptime(
                f"{dt.utcnow().strftime('%Y-%m-%d')} {s}", "%Y-%m-%d %H%M"
            ),
            lambda s: dt.strptime(
                f"{dt.utcnow().strftime('%Y-%m-%d')} {s}", "%Y-%m-%d %H"
            ),
            lambda s: dt.strptime(
                f"{dt.utcnow().strftime('%Y-%m-%d')} {s}", "%Y-%m-%d %-H"
            ),
        ):
            try:
                result = f(string).replace(tzinfo=datetime.timezone.utc)
                break
            except Exception:
                pass
        if result:
            result += offset
        return result

    @staticmethod
    def timeformat(t):
        return t.strftime("%Y-%m-%dT%H:%M:%S%z")

    def store(self):
        self.start = self.start or datetime.date.utcnow()
        self.end = self.end or datetime.date.utcnow()
        if self.end < self.start:
            logger.info(
                f"↔️  event {self.id!r}: Swapping start and end (they're backwards)"
            )
            self.start, self.end = self.end, self.start

        def folders():
            start, end = self.start, self.end
            start = datetime.date(start.year, start.month, start.day)
            end = datetime.date(end.year, end.month, end.day)
            day = start
            lastweekpath = None
            while day <= end:
                path = Path()
                for p in "%Y %m %d".split():
                    path /= day.strftime(p)
                yield path
                weekpath = Path()
                for p in "%Y W %W".split():
                    weekpath /= day.strftime(p)
                if weekpath != lastweekpath:
                    yield weekpath
                lastweekpath = weekpath
                day += datetime.timedelta(days=1)

        paths = set()
        for folder in folders():
            if not (folder_ := self.repo / folder).exists():
                logger.debug(f"📁 Creating new folder {folder}")
                folder_.mkdir(parents=True)
            file = (folder_ / self.id).with_suffix(self.SUFFIX)
            if (file.exists() or file.is_symlink()) and not (self.paths or self.key):
                logger.warning(
                    f"🐛 {file} exists although this event {event.id} is new (it has no paths or key attached). "
                    f"This is either a bug 🐛 or you just witnessed a collision. 💥"
                    f"🗑️ Removing {file}."
                )
                file.unlink()
            if file.is_symlink() and not os.access(str(file), os.W_OK):
                logger.debug(f"🗑️ Removing existing read-only symlink {file}")
                file.unlink()
            file_existed = file.exists()
            with file.open("w") as fh:
                logger.debug(
                    f"🧾 {'Overwriting' if file_existed else 'Creating'} {file} with content {self.id!r}"
                )
                fh.write(self.id)
            try:
                paths.add(file.relative_to(self.repo))
            except ValueError:
                paths.add(file)
        self.paths = paths
        with logger.console.status(f"Adding {len(self.paths)} paths..."):
            result = run(
                subprocess.run,
                ["git", "-C", self.repo, "annex", "add", "--json"] + sorted(self.paths),
                output_lexer="json",
                title=f"Adding {len(self.paths)} paths for event {self.id!r}",
            )
            keys = set()
            for info in utils.from_jsonlines(result.stdout):
                if key := info.get("key"):
                    keys.add(key)
            if len(keys) != 1:
                logger.warning(
                    f"🐛 Adding {len(self.paths)} paths for event {self.id!r} resulted in {len(keys)} keys {keys}. "
                    f"That should be exactly 1. This is probably a bug."
                )
            if keys:
                self.key = next(iter(keys), None)
                logger.debug(f"🔑 key for event {self.id!r} is {self.key!r}")
        with logger.console.status(f"Force-dropping {keys = }..."):
            result = run(
                subprocess.run,
                ["git", "-C", self.repo, "annex", "drop", "--force", "--key"]
                + list(keys),
                title=f"Force-dropping {keys = } for event {self.id!r}",
            )
        with logger.console.status(f"Committing addition of event {self.id!r}..."):
            result = run(
                subprocess.run,
                [
                    "git",
                    "-C",
                    self.repo,
                    "commit",
                    "-m",
                    f"➕ Add {self.id!r} ({self.title or 'untitled'})",
                ],
                title=f"Committing addition of event {self.id!r}",
            )
            if not result.returncode:
                logger.info(f"✅ Committed addition of event {self.id!r}")

    def to_rich(self):
        table = Table(title=self.title, padding=0, box=box.ROUNDED, show_header=False)
        table.add_column("", justify="left")
        table.add_column("Field", justify="right", style="cyan")
        table.add_column("Value", justify="left")
        if self.id:
            table.add_row("💳", "id", f"[b]{self.id}[/b]")
        if self.paths and logger.getEffectiveLevel() < logging.DEBUG:
            table.add_row(
                "🧾",
                "paths",
                ReprHighlighter()(Text("\n".join(str(p) for p in self.paths))),
            )
        if self.paths and logger.getEffectiveLevel() < logging.DEBUG:
            table.add_row("🔑", "key", self.key)
        timehighlighter = ISO8601Highlighter()
        if start := self.start:
            table.add_row("🚀", "start", start.strftime("%c%Z"))
        if end := self.end:
            table.add_row("⏱️", "end", end.strftime("%c%Z"))
        if self.location:
            table.add_row(
                "📍", "location", ", ".join([f"📍 {t}" for t in sorted(self.location)])
            )
        if self.tags:
            table.add_row(
                "🏷️", "tags", " ".join([f"🏷️ {t}" for t in sorted(self.tags)])
            )
        for field, values in self.fields.items():
            if field in "start end tag location title note".split():
                continue
            table.add_row("", field, " ".join(f"📝 {value}" for value in values))
        if self.note:
            table.add_row("📝", "note", self.note)
        return table

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        def default(x):
            if hasattr(x, "strftime"):
                return self.timeformat(x)
            if not isinstance(x, str):
                try:
                    iter(x)
                    return tuple(x)
                except TypeError:
                    pass
            return str(x)

        return json.dumps(self.to_dict(), default=default)

    def to_timeclock(self):
        def sanitize(s):
            s = re.sub(r"[,:;]", r"⁏", s)  # replace separation chars
            s = re.sub(r"[\r\n]+", r" ", s)  # no newlines
            return s

        hledger_tags = {
            "tags": " ⁏ ".join(map(sanitize, sorted(self.tags))),
            "location": " ⁏ ".join(map(sanitize, sorted(self.location))),
        }
        for tag in sorted(self.tags):
            hledger_tags[tag] = ""
        hledger_tags = [f"{t}: {v}" for t, v in hledger_tags.items()]
        hledger_comment = f";  {', '.join(hledger_tags)}" if hledger_tags else ""
        info = [
            ":".join(self.fields.get("account", self.tags)),
            self.title,
            hledger_comment,
        ]
        return textwrap.dedent(
            f""" 
        i {self.start.strftime('%Y-%m-%d %H:%M:%S%z')} {'  '.join(filter(bool,info))}
        o {self.end.strftime('%Y-%m-%d %H:%M:%S%z')}
        """
        ).strip()
