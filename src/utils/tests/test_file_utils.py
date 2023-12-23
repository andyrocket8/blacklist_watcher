from dataclasses import dataclass
from typing import Optional

import pytest

from src.utils import calc_starting_hash
from src.utils import calc_starting_hash_async
from src.utils import compose_file
from src.utils import compose_file_async
from src.utils import create_temp_dir
from src.utils import remove_dir


@pytest.mark.asyncio
async def test_create_temp_dir():
    # test of managing test directories
    temp_dir = create_temp_dir()
    try:
        assert temp_dir.is_dir(), 'Expecting of temp directory creation'
        inside_temp_dir = create_temp_dir(temp_dir)
        assert inside_temp_dir.is_dir(), 'Expecting of inbound temp directory creation'
        assert inside_temp_dir.parent == temp_dir, 'Child dir must be created temporary directory'
        inside_file_txt = inside_temp_dir.joinpath('inside_file.txt')
        await compose_file_async(inside_file_txt, 'Some text contents')
        inside_file_bin = inside_temp_dir.joinpath('inside_file.bin')
        await compose_file_async(inside_file_bin, b'Some binary contents')
        assert inside_file_txt.is_file(), 'Expecting of inbound text file creation'
        assert inside_file_bin.is_file(), 'Expecting of inbound binary file creation'
        # some blocking operations
        inside_blocking_file_txt = inside_temp_dir.joinpath('inside_blk_file.txt')
        compose_file(inside_blocking_file_txt, 'Some text contents with blocking write')
        inside_blocking_file_bin = inside_temp_dir.joinpath('inside_blk_file.bin')
        compose_file(inside_blocking_file_bin, 'Some binary contents with blocking write')
        assert inside_blocking_file_txt.is_file(), 'Expecting of inbound text file creation (via blocking)'
        assert inside_blocking_file_bin.is_file(), 'Expecting of inbound binary file creation (via blocking)'

    finally:
        remove_dir(temp_dir)
        assert not temp_dir.is_dir(), 'Expecting of temp directory deletion'


@dataclass(frozen=True)
class HashTestRecord:
    file_contents: Optional[str]
    hash_value: Optional[str]
    file_name: str
    test_description: str


HASH_TEST_SET: set[HashTestRecord] = {
    HashTestRecord(
        file_contents=None, hash_value=None, file_name='non_exist.txt', test_description='No file calc hash test'
    ),
    HashTestRecord(
        file_contents='', hash_value=None, file_name='empty.txt', test_description='Empty file calc hash test'
    ),
    HashTestRecord(
        file_contents='1234567890',
        hash_value='c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646',
        file_name='short.txt',
        test_description='Short file calc hash test',
    ),
    HashTestRecord(
        file_contents=(
            '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
            '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
            '123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
            '1234567890'
        ),
        hash_value='0f1829840ec086a069609d54ae9695fc92b280a4f32b6a0270d50956ecd6196f',
        file_name='long.txt',
        test_description='Long file calc hash test',
    ),
}


@pytest.mark.asyncio
async def test_hash_routines():
    # test hash routine
    temp_dir = create_temp_dir()
    try:
        for step, record in enumerate(HASH_TEST_SET):
            file_name = temp_dir.joinpath(record.file_name)
            if record.file_contents is not None:
                # create file and calc hash
                await compose_file_async(file_name, record.file_contents)
            hash_value_async = await calc_starting_hash_async(file_name)
            hash_value = calc_starting_hash(file_name)
            assert (
                hash_value == record.hash_value
            ), f'Mismatch hash value on {step + 1} {record.test_description} - sync version'
            assert (
                hash_value_async == record.hash_value
            ), f'Mismatch hash value on {step + 1} {record.test_description} - async version'
    finally:
        remove_dir(temp_dir)
        assert not temp_dir.is_dir(), 'Expecting of temp directory deletion'
