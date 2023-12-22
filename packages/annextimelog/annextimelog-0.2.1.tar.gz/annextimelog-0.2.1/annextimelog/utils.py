# system modules
import json
import logging


logger = logging.getLogger(__name__)


def from_jsonlines(string):
    if hasattr(string, "decode"):
        string = string.decode(errors="ignore")
    string = str(string or "")
    for i, line in enumerate(string.splitlines(), start=1):
        try:
            yield json.loads(line)
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            logger.warning(f"line #{i} ({line!r}) is invalid JSON: {e!r}")
            continue
