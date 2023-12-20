import importlib.metadata
from datetime import datetime, timedelta
from typing import Any, Generator

__version__ = importlib.metadata.version("dateiter")


DEFAULT_DATE_FORMAT = "%Y-%m-%d"


def dateiter(
    start: str | datetime,
    end: str | datetime | None,
    step: int = 1,
    format: str = DEFAULT_DATE_FORMAT,
) -> Generator[datetime, Any, None]:
    start_date = datetime.strptime(start, format) if isinstance(start, str) else start

    if end is None:
        end = (datetime.today() + timedelta(days=1)).strftime(format)

    end_date = datetime.strptime(end, format) if isinstance(end, str) else end

    while start_date < end_date:
        yield start_date
        start_date += timedelta(days=step)
