# Class for storing file process status.
# Can load and save status (on program reload)
import json
import logging
from pathlib import Path
from typing import Optional
from typing import Union

import aiofiles

from src.schemas.processing_status import ProcessingStatus
from src.utils import calc_starting_hash


class ProcessingStatusStorage:
    def __init__(self, status_file: Union[Path, str]):
        self.status_file: Path = Path(status_file)
        self.storage: dict[Path, ProcessingStatus] = dict()

    def add_processing_status(self, status_obj: ProcessingStatus):
        """Add status info to storage"""
        self.storage[status_obj.file_name] = status_obj

    def load(self):
        self.storage = dict()
        """Simple load implementation (with no exception handling)"""
        logging.debug('Loading status information from %s', self.status_file)
        if self.status_file.is_file():
            with open(self.status_file, mode='r') as f:
                contents = json.load(f)
            for record in contents:
                status_obj = ProcessingStatus(**record)
                self.add_processing_status(status_obj)
            logging.debug('Status information loaded, records count: %d', len(self.storage.keys()))
        else:
            logging.warning('Status information file %s is absent, suppose first start', self.status_file)

    def prepare_data(self) -> list:
        result = []
        for key in self.storage:
            result.append(self.storage[key].model_dump(mode='json'))
        return result

    def save(self):
        """Simple save implementation (with no exception handling)"""
        logging.debug('Saving status information to %s', self.status_file)
        result = self.prepare_data()
        with open(self.status_file, mode='w') as f:
            json.dump(result, f)
        logging.debug('Status information saved, records count: %d', len(result))

    async def save_async(self):
        logging.debug('Saving status information to %s', self.status_file)
        result = self.prepare_data()
        async with aiofiles.open(self.status_file, mode='w') as f:
            await f.write(json.dumps(result))
        logging.debug('Status information saved, records count: %d', len(result))

    def update_hashes(self):
        logging.debug('Update hash data to %s', self.status_file)
        for key in self.storage:
            item = self.storage[key]
            item.file_hash = calc_starting_hash(item.file_name)
        logging.debug('Hash information saved, records count: %d', len(self.storage.keys()))

    def get(self, file_name: Path) -> Optional[ProcessingStatus]:
        return self.storage.get(file_name, None)
