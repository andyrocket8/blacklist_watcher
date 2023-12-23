import asyncio
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from hashlib import sha256
from os import chmod
from os import remove
from os import rmdir
from os import walk
from pathlib import Path
from tempfile import mkdtemp
from typing import Literal
from typing import Optional
from typing import Union
from typing import cast

import aiofiles
from aiofiles import open as async_open


def create_temp_dir(base_path: Optional[Union[str, Path]] = None) -> Path:
    """
    Создать временную папку (Используем стандартный модуль tempfile)
    :param Optional[Union[str, Path]] base_path: базовый путь для создания папки
    :return: Path: путь созданной папки
    """
    tmp_dir_name = mkdtemp(suffix=None, prefix=None, dir=base_path)
    return Path(tmp_dir_name)


def remove_dir(dir_path: Path):
    """
    Удалить папку с удалением всех файлов
    :param Path dir_path: Путь до удаляемой папки
    :return: None
    """
    for root, dirs, files in walk(dir_path, topdown=False):
        for name in files:
            current_path = Path(root).joinpath(name)
            try:
                chmod(current_path, 0o777)
            except PermissionError:
                pass
            remove(current_path)
        for name in dirs:
            rmdir(Path(root).joinpath(name))
    rmdir(dir_path)


def calc_hash(content: bytes) -> str:
    m = sha256()
    m.update(content)
    return m.hexdigest()


async def calc_starting_hash_async(file_path: Path) -> Optional[str]:
    """Async reading up to 256 first bytes of file and calculate hash based on loaded content"""
    if file_path.is_file():  # file exists
        try:
            async with async_open(file_path, mode='rb') as f:
                first_up_to_256_bytes = await f.read(256)
        except OSError as e:
            # if any error with file occurs - log it and set content to empty buffer
            logging.error('Error while accessing file %s on hash calculation, details %s', file_path, str(e))
            first_up_to_256_bytes = b''
        if len(first_up_to_256_bytes):  # file is not empty
            loop = asyncio.get_running_loop()
            with ThreadPoolExecutor() as pool:
                task = loop.run_in_executor(pool, partial(calc_hash, first_up_to_256_bytes))
            return await task
    return None


def calc_starting_hash(file_path: Path) -> Optional[str]:
    if file_path.is_file():  # file exists
        try:
            with open(file_path, mode='rb') as f:
                first_up_to_256_bytes = f.read(256)
        except OSError as e:
            # if any error with file occurs - log it and set content to empty buffer
            logging.error('Error while accessing file %s on hash calculation, details %s', file_path, str(e))
            first_up_to_256_bytes = b''
        if len(first_up_to_256_bytes):  # file is not empty
            return calc_hash(first_up_to_256_bytes)
    return None


def compose_file(file_path: Path, file_contents: Union[bytes, str]):
    """Write file contents (string or bytes)"""
    with open(file_path, mode='wb' if (type(file_contents) is bytes) else 'w') as f:
        f.write(file_contents)


async def compose_file_async(file_path: Path, file_contents: Union[bytes, str]):
    """Write file contents (string or bytes) with aiofiles approach"""
    mode: Literal['w', 'wb'] = cast(Literal['w', 'wb'], 'wb' if (type(file_contents) is bytes) else 'w')
    async with aiofiles.open(file_path, mode=mode) as f:
        await f.write(file_contents)  # type: ignore[arg-type]
