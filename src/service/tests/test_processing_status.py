import datetime
from pathlib import Path

from src.schemas import ProcessingStatus
from src.service import ProcessingStatusStorage
from src.utils import create_temp_dir
from src.utils import curr_datetime
from src.utils import remove_dir

PROCESSING_STATUS: list[ProcessingStatus] = [
    ProcessingStatus(file_name=Path('/home/test/data/file1.log'), file_date_time=None, file_size=None, file_hash=None),
    ProcessingStatus(
        file_name=Path('/home/test/data/file2.log'),
        current_offset=1024,
        file_date_time=curr_datetime(),
        file_size=2048,
        file_hash='1234567890',
    ),
    ProcessingStatus(
        file_name=Path('/home/test/data/file3.log'),
        current_offset=0,
        file_date_time=curr_datetime() - datetime.timedelta(days=2),
        file_size=10000,
        file_hash='1234567890_00',
    ),
]


def test_processing_status():
    temp_dir = create_temp_dir()
    try:
        test_status_file_path = Path(temp_dir).joinpath('status_file.json')
        file_process_status_obj = ProcessingStatusStorage(test_status_file_path)
        assert not file_process_status_obj.status_file.is_file(), 'Expecting absense of config file'
        file_process_status_obj.add_processing_status(PROCESSING_STATUS[0])
        file_process_status_obj.save()
        file_process_status_obj = ProcessingStatusStorage(test_status_file_path)
        assert file_process_status_obj.status_file.is_file(), 'Expecting presence of config file'
        file_process_status_obj.load()
        assert (
            file_process_status_obj.storage[PROCESSING_STATUS[0].file_name] == PROCESSING_STATUS[0]
        ), 'Expecting saved and restored information about one file'
        assert len(file_process_status_obj.storage.keys()) == 1, 'Expecting length of status file storage == 1'
        file_process_status_obj.add_processing_status(PROCESSING_STATUS[1])
        file_process_status_obj.add_processing_status(PROCESSING_STATUS[2])
        file_process_status_obj.save()
        file_process_status_obj.storage.clear()
        assert len(file_process_status_obj.storage.keys()) == 0, 'Expecting empty status file storage after cleaning'
        file_process_status_obj.load()
        assert len(file_process_status_obj.storage.keys()) == 3, 'Expecting length of status file storage == 3'
        assert (
            file_process_status_obj.storage[PROCESSING_STATUS[2].file_name] == PROCESSING_STATUS[2]
        ), 'Expecting saved and restored information about third file'
    finally:
        remove_dir(temp_dir)
