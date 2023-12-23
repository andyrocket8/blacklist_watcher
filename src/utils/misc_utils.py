import datetime
import re
from typing import Optional

from src.core.settings import CUR_TZ


def curr_datetime() -> datetime.datetime:
    """
    Получить текущее время
    returns: datetime.datetime: текущее дата и время с таймзоной
    """
    return datetime.datetime.now(tz=CUR_TZ)


def parse_regex(pattern: str, inspected: str) -> Optional[tuple]:
    match_obj = re.match(pattern, inspected)
    if match_obj is not None:
        return match_obj.groups()
    return None
