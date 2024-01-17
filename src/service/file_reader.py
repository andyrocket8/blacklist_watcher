from pathlib import Path
from typing import AsyncGenerator

import aiofiles


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
