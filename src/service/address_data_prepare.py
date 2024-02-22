from collections import defaultdict
from ipaddress import IPv4Address
from typing import Generator

from src.schemas.address_dedup_info import AddressDedupInfo
from src.schemas.blacklist_schema import BlackListCallSchema
from src.schemas.blacklist_schema import BlackListSyncSchema
from src.schemas.dedup_destination_category import CallDestinationCategory
from src.schemas.watcher_schema import AddressCategory
from src.schemas.watcher_schema import EventCategory
from src.utils import curr_datetime


def produce_address_dict() -> defaultdict[IPv4Address, AddressDedupInfo]:
    """Default value producer for defaultdict"""
    return defaultdict(AddressDedupInfo)


def deduplicate_addresses_data(
    addresses_info: list[BlackListSyncSchema],
) -> tuple[
    dict[CallDestinationCategory, defaultdict[IPv4Address, AddressDedupInfo]], dict[CallDestinationCategory, set[str]]
]:
    """
    :param addresses_info: list[BlackListSyncSchema]
    :return:
        - dictionary with keys with knowledge about handle calling destination (address category, address group)
          values are also dict
          - keys are IP addresses (deduplicated)
          - values are information about agent information (last used one) and counter about event category.
            We increment counter if we parse 'add_address' operation and decrease it if we parse 'delete_address'
        - one more dictionary with the same keys, containing sets of agent_names.
    :rtype: tuple
    """
    # Prepare variables for further deduplication
    call_destination_category_dict: dict[
        CallDestinationCategory, defaultdict[IPv4Address, AddressDedupInfo]
    ] = defaultdict(produce_address_dict)
    call_destination_agents_dict: dict[CallDestinationCategory, set[str]] = defaultdict(set)
    for address_info in addresses_info:
        dicts_key = CallDestinationCategory(
            address_group=address_info.address_group, address_category=address_info.address_category
        )
        addresses_dict: defaultdict[IPv4Address, AddressDedupInfo] = call_destination_category_dict[dicts_key]
        # on operation below address information counter is filled with agent info.
        # We store only last logged agent_name to avoid unexpected additions and deletions of addresses
        addresses_dict[address_info.address] += AddressDedupInfo(
            source_agent=address_info.source_agent,
            count=1 if address_info.event_category == EventCategory.add_address else -1,
        )
        # all met agents will be added to distinct destination agents sets.
        call_destination_agents_dict[dicts_key].add(address_info.source_agent)
    return call_destination_category_dict, call_destination_agents_dict


def aggregate_by_agent(
    add_address: bool, data: defaultdict[IPv4Address, AddressDedupInfo], agent_name: str
) -> list[IPv4Address]:
    return [
        key
        for key, address_record in data.items()
        if (address_record.count > 0 if add_address else address_record.count < 0)
        and address_record.source_agent == agent_name
    ]


def addresses_data_for_sync(
    addresses_info: list[BlackListSyncSchema],
) -> Generator[tuple[EventCategory, AddressCategory, BlackListCallSchema], None, None]:
    # Process parsed data with deduplication
    current_time = curr_datetime()
    addresses_dict, agents_dict = deduplicate_addresses_data(addresses_info)
    # iterate over every DedupDestinationCategory object
    for destination_key, addresses_info_dict in addresses_dict.items():
        # process unblock operations, iterate over all stored agents
        # for every agent connected with processed destination
        for agent_name in agents_dict[destination_key]:
            delete_addresses: list[IPv4Address] = aggregate_by_agent(False, addresses_info_dict, agent_name)
            if delete_addresses:
                yield (
                    EventCategory.del_address,
                    destination_key.address_category,
                    BlackListCallSchema(
                        source_agent=agent_name,
                        action_time=current_time,
                        addresses=delete_addresses,
                        address_group=destination_key.address_group,
                    ),
                )
        # process block operations
        for agent_name in agents_dict[destination_key]:
            add_addresses: list[IPv4Address] = aggregate_by_agent(True, addresses_info_dict, agent_name)
            if add_addresses:
                yield (
                    EventCategory.add_address,
                    destination_key.address_category,
                    BlackListCallSchema(
                        source_agent=agent_name,
                        action_time=current_time,
                        addresses=add_addresses,
                        address_group=destination_key.address_group,
                    ),
                )
