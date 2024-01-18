from ipaddress import IPv4Address
from pathlib import Path
from typing import Generator

import pytest

from src.service.blacklist_sync import aggregate_by_agent
from src.service.blacklist_sync import count_addresses_data
from src.service.file_parser import FileWatcherParser
from src.utils.file_utils import compose_file
from src.utils.file_utils import create_temp_dir
from src.utils.file_utils import remove_dir

from .test_file_reader_data import OK_TEST_FILE_DATA_SI  # separate process parser test data (implemented in #9, #12)
from .test_file_reader_data import SSHD_AGENT_NAME
from .test_file_reader_data import TEST_RULES
from .test_file_reader_data import WWW_AGENT_NAME


@pytest.fixture()
def file_test_contents() -> Generator[Path, None, None]:
    temp_dir = create_temp_dir()
    try:
        file_name = temp_dir.joinpath('ok_file_data_si.log')
        compose_file(file_name, OK_TEST_FILE_DATA_SI)
        yield file_name
    finally:
        remove_dir(temp_dir)


@pytest.mark.asyncio
async def test_file_watcher_parser(file_test_contents):
    fwp_obj = FileWatcherParser(file_test_contents)
    # Test composite function of parser
    offset, parsed_records = await fwp_obj.parse_file_with_rules(0, TEST_RULES)
    # Merge data with sync module routine
    addresses_count_data, agents = count_addresses_data(parsed_records)
    # Check parsed agents count
    assert len(agents) == 2, 'Merge routine detected wrong agents count'
    agent_block_aggregated: dict[str, list[IPv4Address]] = {}
    agent_unblock_aggregated: dict[str, list[IPv4Address]] = {}
    for agent in agents:
        agent_block_aggregated[agent] = aggregate_by_agent(True, addresses_count_data, agent)
        agent_unblock_aggregated[agent] = aggregate_by_agent(False, addresses_count_data, agent)
    # Some checks
    assert len(agent_block_aggregated[SSHD_AGENT_NAME]) == 2, f'Aggregated for blocking {SSHD_AGENT_NAME} mismatched'
    assert len(agent_block_aggregated[WWW_AGENT_NAME]) == 1, f'Aggregated for blocking {WWW_AGENT_NAME} mismatched'
    assert (
        IPv4Address('101.34.218.206') not in agent_block_aggregated[SSHD_AGENT_NAME]
    ), f'Address 101.34.218.206 must not be in {SSHD_AGENT_NAME} block list'
    assert (
        IPv4Address('101.34.218.206') not in agent_unblock_aggregated[SSHD_AGENT_NAME]
    ), f'Address 101.34.218.206 must not be in {SSHD_AGENT_NAME} unblock list'
    assert (
        IPv4Address('170.64.210.196') in agent_block_aggregated[SSHD_AGENT_NAME]
    ), f'Address 170.64.210.196 must be in {SSHD_AGENT_NAME} block list'
    assert (
        IPv4Address('185.244.25.14') in agent_block_aggregated[WWW_AGENT_NAME]
    ), f'Address 185.244.25.14 must be in {WWW_AGENT_NAME} block list'
    assert (
        IPv4Address('134.122.12.11') not in agent_block_aggregated[WWW_AGENT_NAME]
    ), f'Address 134.122.12.11 must not be in {WWW_AGENT_NAME} block list'
    assert (
        len(agent_unblock_aggregated[SSHD_AGENT_NAME]) == 27
    ), f'Aggregated for unblocking {SSHD_AGENT_NAME} mismatched'
    assert len(agent_unblock_aggregated[WWW_AGENT_NAME]) == 1, f'Aggregated for unblocking {WWW_AGENT_NAME} mismatched'
    assert offset == len(OK_TEST_FILE_DATA_SI), 'Offset after file parsing should be equal length of test data'
