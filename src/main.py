import argparse
import asyncio
import logging
import sys
from logging.handlers import WatchedFileHandler
from typing import Union

from pydantic import ValidationError
from yaml import load as load_yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader  # type:ignore

from src.core.settings import LOG_FORMAT
from src.schemas.config import ConfigLogSchema
from src.schemas.config import ConfigSchema
from src.service import MainProcessor
from src.service import ProcessingStatusStorage


def init_logging(logging_data: ConfigLogSchema):
    handlers: list[Union[WatchedFileHandler, logging.StreamHandler]] = []
    formatter = logging.Formatter(LOG_FORMAT)
    if logging_data.filename:
        file_handler = WatchedFileHandler(logging_data.filename)
        file_handler.setLevel(logging_data.level)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    if logging_data.console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging_data.level)
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)
    logging.basicConfig(level=logging_data.level, handlers=handlers)


def main():
    parser = argparse.ArgumentParser(
        prog='File watcher',
        description='Perform file watching and invoke actions on file contents change',
        usage='python ./src/main.py <filename>\n       where filename is YAML configuration file',
    )
    parser.add_argument('filename', help='Configuration file in YAML format')
    config_file = parser.parse_args().filename
    with open(config_file, mode='r') as f:
        config_data: dict = load_yaml(f, Loader=Loader)
    try:
        config = ConfigSchema(**config_data)
    except ValidationError as e:
        print(f'Error on parsing config file {config_file}, details:')
        print(e)
        sys.exit(1)

    init_logging(config.logging)
    logging.info('File watcher: application started')
    processing_status_storage = ProcessingStatusStorage(config.status_file)
    # load status file on startup
    processing_status_storage.load()
    files_processor = MainProcessor(config, processing_status_storage)
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(files_processor.run())
    except asyncio.CancelledError:
        logging.info('CancelledError')
    finally:
        loop.close()
    # update hashes
    processing_status_storage.update_hashes()
    # save status file on exit
    processing_status_storage.save()


if __name__ == "__main__":
    main()
