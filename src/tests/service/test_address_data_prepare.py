# type: ignore
from ipaddress import IPv4Address
from pathlib import Path
from typing import Generator

import pytest

from src.schemas.blacklist_schema import BlackListCallSchema
from src.schemas.watcher_schema import AddressCategory
from src.schemas.watcher_schema import EventCategory
from src.service.address_data_prepare import addresses_data_for_sync
from src.service.file_parser import FileWatcherParser
from src.tests.service.test_file_reader_data import (
    OK_TEST_FILE_DATA_SI,
)  # separate process parser test data (implemented in #9, #12)
from src.tests.service.test_file_reader_data import TEST_RULES
from src.utils.file_utils import compose_file
from src.utils.file_utils import create_temp_dir
from src.utils.file_utils import remove_dir


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
async def test_address_data_prepare(file_test_contents):
    fwp_obj = FileWatcherParser(file_test_contents)
    # Test composite function of parser
    offset, parsed_records = await fwp_obj.parse_file_with_rules(0, TEST_RULES)
    assert offset == 6967, 'Mismatch offset after parsing data'
    # Merge data with sync module routine
    tested_data: list[tuple[EventCategory, AddressCategory, BlackListCallSchema]] = [
        x for x in addresses_data_for_sync(parsed_records)
    ]
    # for i in (x for x in tested_data if x[0] == EventCategory.add_address):
    #    print('\n', i)
    # for i in (x for x in tested_data if x[0] == EventCategory.del_address):
    #    print('\n', i)

    assert len(tested_data) == 6, 'Merge routine gathered wrong data (Expected length)'
    for tested_data_record in tested_data:
        event_category, address_category, request_data = tested_data_record
        match event_category, address_category:
            case (EventCategory.add_address, AddressCategory.banned):
                match request_data.source_agent:
                    case 'sshd-out':
                        assert request_data.address_group == 'banned_sshd'
                        assert len(request_data.addresses) == 1
                        assert IPv4Address('10.100.0.11') in request_data.addresses
                    case 'sshd':
                        assert request_data.address_group == 'banned_sshd'
                        assert len(request_data.addresses) == 2
                        assert IPv4Address('192.168.1.4') in request_data.addresses
                        assert IPv4Address('192.168.1.12') in request_data.addresses
                    case 'www':
                        raise AssertionError('www agent must not be in "banned" address category with add operations')
                    case 'ftp':
                        raise AssertionError('ftp agent must not be in "banned" address category with add operations')
            case (EventCategory.add_address, AddressCategory.allowed):
                match request_data.source_agent:
                    case 'www':
                        assert request_data.address_group == ''
                        assert len(request_data.addresses) == 2
                        assert IPv4Address('10.100.0.11') in request_data.addresses
                        assert IPv4Address('192.168.1.16') in request_data.addresses
                    case 'sshd':
                        raise AssertionError('sshd agent must not be in "allowed" address category with add operations')
                    case 'sshd-out':
                        raise AssertionError(
                            'sshd-out agent must not be in "allowed" address category with add operations'
                        )
                    case 'ftp':
                        raise AssertionError('ftp agent must not be in "allowed" address category with add operations')
            case (EventCategory.del_address, AddressCategory.banned):
                match request_data.source_agent:
                    case 'sshd':
                        assert len(request_data.addresses) == 16
                        assert request_data.address_group == 'banned_sshd'
                        assert IPv4Address('192.168.1.1') in request_data.addresses
                        assert IPv4Address('192.168.1.5') in request_data.addresses
                        assert IPv4Address('192.168.1.6') in request_data.addresses
                        assert IPv4Address('192.168.1.7') in request_data.addresses
                        assert IPv4Address('192.168.1.8') in request_data.addresses
                        assert IPv4Address('192.168.1.10') in request_data.addresses
                        assert IPv4Address('192.168.1.11') in request_data.addresses
                        assert IPv4Address('10.100.0.2') in request_data.addresses
                        assert IPv4Address('10.100.0.3') in request_data.addresses
                        assert IPv4Address('10.100.0.12') in request_data.addresses
                    case 'ftp':
                        assert request_data.address_group == 'banned_ftp'
                        assert len(request_data.addresses) == 5
                        assert IPv4Address('192.168.1.13') in request_data.addresses
                        assert IPv4Address('192.168.1.14') in request_data.addresses
                        assert IPv4Address('192.168.1.15') in request_data.addresses
                        assert IPv4Address('10.100.0.1') in request_data.addresses
                    case 'www':
                        raise AssertionError('www agent must not be in "banned" address category with del operations')
                    case 'sshd-out':
                        raise AssertionError(
                            'sshd-out agent must not be in "banned" address category with del operations'
                        )
            case (EventCategory.del_address, AddressCategory.allowed):
                match request_data.source_agent:
                    case 'www':
                        assert request_data.address_group == ''
                        assert len(request_data.addresses) == 3
                        assert IPv4Address('10.100.0.1') in request_data.addresses
                        assert IPv4Address('10.100.0.2') in request_data.addresses
                        assert IPv4Address('192.168.1.12') in request_data.addresses
                    case 'sshd':
                        raise AssertionError('sshd agent must not be in "allowed" address category with del operations')
                    case 'sshd-out':
                        raise AssertionError(
                            'sshd-out agent must not be in "allowed" address category with del operations'
                        )
                    case 'ftp':
                        raise AssertionError('ftp agent must not be in "allowed" address category with del operations')
