from typing import AsyncGenerator
from typing import Optional

from src.schemas.watcher_schema import WatcherRule
from src.utils import parse_regex

from .file_reader import FileReader


class FileParser(FileReader):
    """File reader with capabilities of line parsing"""

    async def parse_lines(self, offset: int, regex: str) -> AsyncGenerator[tuple[int, Optional[tuple]], None]:
        async for offset, line in self.read_lines(offset):
            if line:
                parsed = parse_regex(regex, line)
                if parsed is not None:
                    yield offset, parsed
        yield offset, None


class FileWatcherParser(FileReader):
    async def parse_lines(
        self, offset: int, rules: list[WatcherRule]
    ) -> AsyncGenerator[tuple[int, Optional[WatcherRule], Optional[tuple]], None]:
        async for offset, line in self.read_lines(offset):
            if line:
                for rule in rules:
                    parsed = parse_regex(rule.regex, line)
                    if parsed is not None:
                        yield offset, rule, parsed
                        break
        yield offset, None, None
