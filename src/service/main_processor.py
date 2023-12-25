import asyncio
import functools
import logging
import signal
from pathlib import Path
from typing import Iterable
from typing import Optional
from typing import Set

from src.schemas.config import WatcherSchema
from src.schemas.processing_status import ProcessingStatus

from .file_processor import FileProcessor
from .file_status import FileStatus
from .files_watcher import FilesWatcher
from .processing_status_storage import ProcessingStatusStorage


class MainProcessor:
    def __init__(
        self,
        files_to_process: Iterable[WatcherSchema],
        ps_storage: ProcessingStatusStorage,
        blacklist_uri: str,
        token: str,
        watch_period: int,
    ):
        self.watcher_obj = FilesWatcher(watch_period)
        self.ps_storage = ps_storage
        self.files_to_process_dict: dict[Path, WatcherSchema] = dict()
        for file_watcher_info in files_to_process:
            # Add watcher to internal watcher object
            status_obj: FileStatus = self.watcher_obj.add_watcher(file_watcher_info.filename)
            logging.debug('Added watcher for file %s', file_watcher_info.filename)
            if not status_obj.file_path.is_file():
                logging.warning('Watched file %s does not exists', file_watcher_info.filename)
            # fill event_description dictionary for WatcherSchema instance (for faster event category detection)
            file_watcher_info.event_description.fill_dictionary()
            # store element in internal dictionary
            self.files_to_process_dict[Path(file_watcher_info.filename)] = file_watcher_info
        self.watcher_task: Optional[asyncio.Task] = None
        self.blacklist_uri = blacklist_uri
        self.token = token

    async def save_configuration(self):
        await self.ps_storage.save_async()

    async def process_file(self, status_file_obj: FileStatus):
        # process file
        logging.debug('Starting File %s processing', status_file_obj.file_path)
        processing_status_obj = self.ps_storage.get(status_file_obj.file_path)
        if processing_status_obj is None:
            processing_status_obj = ProcessingStatus(file_name=status_file_obj.file_path)
            self.ps_storage.add_processing_status(processing_status_obj)
        watcher_obj = self.files_to_process_dict[status_file_obj.file_path]
        file_processor_obj = FileProcessor(
            status_file_obj, watcher_obj, processing_status_obj, self.blacklist_uri, self.token
        )
        await file_processor_obj.process()
        # add processed file to processing queue
        self.watcher_obj.push(status_file_obj)
        logging.debug('File %s processing completed', status_file_obj.file_path)

    async def run(self):
        loop = asyncio.get_running_loop()
        # set signal catcher
        for signal_name in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signal_name), functools.partial(self.sig_stop_catcher, signal_name, loop)
            )
        logging.debug('Process bootstrap sync')
        for status_file_obj in self.watcher_obj.files_to_watch:
            if status_file_obj.current_date is not None:
                await self.process_file(status_file_obj)
            else:
                logging.warning('Process bootstrap: watched file %s is not exist', status_file_obj.file_path)
        logging.debug('Bootstrap sync completed')
        try:
            async for status_file_obj in self.watcher_obj.watch():
                logging.debug('File %s changed. Starting file processing', status_file_obj.file_path)
                loop.create_task(self.process_file(status_file_obj))
        except asyncio.CancelledError:
            logging.debug('Loop execution cancelled. Prepare for exit now')

    def sig_stop_catcher(self, signal_name, _loop):
        logging.info('Got signal %s: exit now', signal_name)
        tasks: Set[asyncio.Task] = asyncio.all_tasks()
        logging.debug(f'Stopping {len(tasks)} tasks ... ')
        [task.cancel() for task in tasks]
        logging.debug('All tasks stopped')
