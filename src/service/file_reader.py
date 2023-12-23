from pathlib import Path
from typing import AsyncGenerator
from typing import Optional

import aiofiles

from src.utils import parse_regex


class FileReader:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    async def read_lines(self, offset: int) -> AsyncGenerator[tuple[int, str], None]:
        async with aiofiles.open(self.file_path, mode='r') as f:
            await f.seek(offset)
            while True:
                line = await f.readline()
                offset = await f.tell()
                yield offset, line
                if len(line) == 0:
                    break


class FileParser(FileReader):
    """File reader with capabilities of line parsing"""

    async def parse_lines(self, offset: int, regex: str) -> AsyncGenerator[tuple[int, Optional[tuple]], None]:
        async for offset, line in self.read_lines(offset):
            if line:
                parsed = parse_regex(regex, line)
                if parsed is not None:
                    yield offset, parsed
        yield offset, None
