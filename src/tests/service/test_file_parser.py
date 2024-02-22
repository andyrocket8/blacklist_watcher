from pathlib import Path
from typing import Generator

import pytest

from src.service.file_parser import FileParser
from src.utils.file_utils import compose_file
from src.utils.file_utils import create_temp_dir
from src.utils.file_utils import remove_dir

from .test_file_reader_data import OK_TEST_FILE_DATA


@pytest.fixture()
def file_test_contents() -> Generator[Path, None, None]:
    temp_dir = create_temp_dir()
    try:
        file_name = temp_dir.joinpath('ok_file_data.log')
        compose_file(file_name, OK_TEST_FILE_DATA)
        yield file_name
    finally:
        remove_dir(temp_dir)


async def count_file_statistics(file_name: Path, start_offset: int):
    ban_count, unban_count = 0, 0
    # testing all file reading
    offset = start_offset
    async for offset, data in FileParser(file_name).parse_lines(
        start_offset, r'.*(Ban|Unban).([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*'
    ):
        if data:
            ban_count += 1 if data[0] == 'Ban' else 0
            unban_count += 1 if data[0] == 'Unban' else 0
    return offset, ban_count, unban_count


@pytest.mark.asyncio
async def test_file_reader(file_test_contents):
    # test file from beginning
    offset, ban_count, unban_count = await count_file_statistics(file_test_contents, 0)
    assert ban_count == 4, 'Expecting count of Ban records are not match'
    assert unban_count == 31, 'Expecting count of Unban records are not match'
    assert offset == 6316, 'Expecting offset value is not match'
    # test file with offset
    offset, ban_count, unban_count = await count_file_statistics(file_test_contents, 5458)
    assert ban_count == 2, 'Expecting count of Ban records are not match (with offset)'
    assert unban_count == 1, 'Expecting count of Unban records are not match (with offset)'
    assert offset == 6316, 'Expecting offset value is not match (with offset)'


# @pytest.mark.asyncio
# @pytest.mark.parametrize('file_test_contents', [(OK_TEST_FILE_DATA_SI, 'ok_file_data_si.log')])
# async def test_file_watcher_parser(file_test_contents):
#     pass
