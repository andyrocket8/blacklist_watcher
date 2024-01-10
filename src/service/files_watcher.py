import asyncio
import logging
from collections import deque
from pathlib import Path
from typing import AsyncGenerator
from typing import Union

from .file_status import FileStatus


class FilesWatcher:
    """
    Watcher for changing files. Watch on file modification date changes
    """

    def __init__(self, watch_period: int):
        self.watch_period = watch_period
        # storage for storing file on watching
        self.files_to_watch: list[FileStatus] = []
        # queue for storing processing files
        self.processing_files: deque[FileStatus] = deque()

    def add_watcher(self, file_name: Union[str, Path]) -> FileStatus:
        """Add FileStatus object to watcher's list and to "processing_files" queue"""
        file_status_obj = FileStatus(file_name)
        # store file status object to "files_to_watch" storage. Change only on "add_watcher" call
        self.files_to_watch.append(file_status_obj)
        # store file status object to "processing_files" queue. Changed on watch cycle and by "push" call
        self.processing_files.append(file_status_obj)
        return file_status_obj

    async def watch(self) -> AsyncGenerator[FileStatus, None]:
        """
        Generator watching files for changes of modification time.
        1) Yield on file changes.
        2) Sleep on WATCH_PERIOD after checking all files in self.processing_files queue

        :return: AsyncGenerator[FileStatus, None]
        """
        while True:
            logging.debug('Start processing of processing_files queue, queue length: %d', len(self.processing_files))
            not_processed: deque[FileStatus] = deque()
            while len(self.processing_files) > 0:
                file_status_obj = self.processing_files.pop()
                # check change of file date and time modification or file size change. Actuate both metrics on change
                if file_status_obj.changed:
                    # status object processor should push processed object after processing.
                    # we do so to avoid time lasting parallel processing of watched files
                    logging.debug(
                        'Current metrics, size: %s, change datetime: %s',
                        file_status_obj.current_size,
                        file_status_obj.current_date,
                    )
                    yield file_status_obj
                else:
                    not_processed.append(file_status_obj)
            # all files in self.processing_files are processed - fill self.processing_files with not processed files
            while len(not_processed) > 0:
                self.processing_files.append(not_processed.pop())
            logging.debug('Finished processing of processing_files queue, queue length: %d', len(self.processing_files))
            await asyncio.sleep(self.watch_period)

    def push(self, file_status_obj: FileStatus):
        # add status object to processing_files queue (should be called after file processing)
        if file_status_obj not in self.processing_files:
            self.processing_files.append(file_status_obj)
