import logging
from typing import Optional

from src.schemas.processing_status import ProcessingStatus
from src.schemas.watcher_schema import WatcherSchema
from src.utils.file_utils import calc_starting_hash_async

from .address_data_prepare import addresses_data_for_sync
from .blacklist_sync import BlackListSync
from .file_parser import FileWatcherParser
from .file_status import FileStatus


class FileProcessor:
    """Processing of changed file based on change status. Actuate process status"""

    def __init__(
        self,
        file_status_obj: FileStatus,
        watcher_schema_obj: WatcherSchema,
        processing_status_obj: ProcessingStatus,
        blacklist_uri: str,
        token: str,
    ):
        self.file_status_obj = file_status_obj
        self.processing_status_obj = processing_status_obj
        self.watcher_schema_obj = watcher_schema_obj
        self.blacklist_uri = blacklist_uri
        self.token = token

    async def calc_hash(self) -> Optional[str]:
        return await calc_starting_hash_async(self.file_status_obj.file_path)

    async def rotated(self) -> tuple[bool, str]:
        """Detect whether file was rotated. Calculate hash if we need it"""
        file_hash = await self.calc_hash()
        ps_size = self.processing_status_obj.file_size if self.processing_status_obj.file_size else 0
        st_size = self.file_status_obj.current_size if self.file_status_obj.current_size else 0
        file_size_decreased = ps_size > st_size
        if file_size_decreased:
            return True, 'file size decreased'
        try:
            hash_mismatch = self.processing_status_obj.file_hash != file_hash
            # save calculated hash in processing status. Will be None if file is absent or file empty
            if hash_mismatch:
                if self.processing_status_obj.file_hash is not None:  # we have information about previous file hash
                    # for files with size from 256 bytes hash could not change
                    return (
                        ps_size >= 256 and st_size >= 256,
                        'file hash changed',
                    )
            return False, 'rotation not detected'
        finally:
            # set calculated file hash to processing status
            self.processing_status_obj.file_hash = file_hash

    def actuate_process_status(self):
        """Actuate process status based on change status"""
        self.processing_status_obj.file_size = self.file_status_obj.current_size
        self.processing_status_obj.file_date_time = self.file_status_obj.current_date

    async def process_file_contents(self):
        file_parser_obj = FileWatcherParser(self.processing_status_obj.file_name)
        offset: int = self.processing_status_obj.current_offset
        # parse all rules in one file
        offset, parsed_records = await file_parser_obj.parse_file_with_rules(offset, self.watcher_schema_obj.rules)
        if len(parsed_records):
            sync_obj = BlackListSync(self.blacklist_uri, self.token)
            # Prepare data and pass it to Blacklist service
            for event_category, address_category, request_data in addresses_data_for_sync(parsed_records):
                await sync_obj.sync_data(event_category, address_category, request_data)
        # actuate current file offset
        self.processing_status_obj.current_offset = offset
        logging.debug('File %s, current offset: %s', self.file_status_obj.file_path, offset)

    async def process(self) -> ProcessingStatus:
        """Process file
        Cases:
        1) no process status information - process file from beginning and save file process info
        No status information sign: file hash is empty (Can be empty on short file or absent file)
        But we can't get here if file is absent!

        2) has process information - compare saved process info with status, detect rotation and after
        that process file depends on rotation info.
        After processing we need to update file process info with fresh one.

        Rotation detection is based on two things
        1) file size has been decreased comparing to previous saved info
        2) we do first process after program startup, and this can occur after undetected file rotation. So we need to
        check file hash (if possible).
        """
        rotated, rotation_msg = await self.rotated()
        logging.debug('Rotation status: %s, %s', 'rotated' if rotated else 'not rotated', rotation_msg)
        if rotated:
            self.processing_status_obj.current_offset = 0
        if not self.file_status_obj.is_available():
            logging.warning('File %s is not accessible', self.file_status_obj.file_path)
        else:
            await self.process_file_contents()
        # actuate file processing status
        self.actuate_process_status()
        # return actuated file processing status
        return self.processing_status_obj
