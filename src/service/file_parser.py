import logging
from ipaddress import IPv4Address
from typing import AsyncGenerator
from typing import Optional

from src.schemas.blacklist_schema import BlackListSyncSchema
from src.schemas.watcher_schema import EventCategory
from src.schemas.watcher_schema import WatcherRule
from src.utils import parse_regex

from .file_reader import FileReader


class FileParser(FileReader):
    """File reader with capabilities of line parsing"""

    async def parse_lines(self, offset: int, regex: str) -> AsyncGenerator[tuple[int, Optional[tuple]], None]:
        async for offset, line in self.read_lines(offset):
            if line:
                parsed = parse_regex(regex, line)
                if parsed is not None:
                    yield offset, parsed
        yield offset, None


class FileWatcherParser(FileReader):
    async def parse_lines(
        self, offset: int, rules: list[WatcherRule]
    ) -> AsyncGenerator[tuple[int, Optional[WatcherRule], Optional[tuple]], None]:
        async for offset, line in self.read_lines(offset):
            if line:
                for rule in rules:
                    parsed = parse_regex(rule.regex, line)
                    if parsed is not None:
                        yield offset, rule, parsed
                        break
        yield offset, None, None

    async def parse_file_with_rules(
        self, offset: int, rules: list[WatcherRule]
    ) -> tuple[int, list[BlackListSyncSchema]]:
        # Parse file with rules and collect data with BlackListSyncSchema records
        parsed_records: list[BlackListSyncSchema] = []
        try:
            async for offset, rule, parsed_data in self.parse_lines(offset, rules):
                if rule is not None:
                    # process detected string with rule definition
                    assert parsed_data is not None, 'Check of parsed tuple value failed!'
                    address: str = parsed_data[rule.address_description.tuple_position]
                    event_desc: str = parsed_data[rule.event_description.tuple_position]
                    assert (
                        rule.event_description.event_mapping_dict is not None
                    ), 'event_description on this stage must be defined'
                    event_category: EventCategory = rule.event_description.event_mapping_dict[event_desc]
                    source_agent = rule.agent
                    logging.debug(
                        'Extracted log event: %s, address: %s, agent: %s', event_category, address, source_agent
                    )
                    parsed_records.append(
                        BlackListSyncSchema(
                            category=event_category, address=IPv4Address(address), source_agent=source_agent
                        )
                    )
        except OSError as e:
            logging.error('Error while processing file, details: %s', str(e))
        return offset, parsed_records
