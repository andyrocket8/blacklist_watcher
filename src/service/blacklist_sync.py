import logging
from collections import defaultdict
from ipaddress import IPv4Address
from typing import Optional

from httpx import AsyncClient
from httpx import HTTPStatusError
from httpx import RequestError

from src.core.settings import BLACKLIST_ADD_METHOD_SUFFIX
from src.core.settings import BLACKLIST_ALLOWED_ADDRESS_PREFIX
from src.core.settings import BLACKLIST_BANNED_ADDRESS_PREFIX
from src.core.settings import BLACKLIST_DELETE_METHOD_SUFFIX
from src.schemas.address_dedup_info import AddressDedupInfo
from src.schemas.blacklist_schema import BlackListCallSchema
from src.schemas.blacklist_schema import BlackListSyncSchema
from src.schemas.dedup_destination_category import CallDestinationCategory
from src.schemas.watcher_schema import AddressCategory
from src.schemas.watcher_schema import EventCategory
from src.utils import curr_datetime


def produce_address_dict() -> defaultdict[IPv4Address, AddressDedupInfo]:
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
    dedup_agents_dict: dict[CallDestinationCategory, set[str]] = defaultdict(set)
    for address_info in addresses_info:
        dicts_key = CallDestinationCategory(
            address_group=address_info.address_group, address_category=address_info.address_category
        )
        addresses_dict: defaultdict[IPv4Address, AddressDedupInfo] = call_destination_category_dict[dicts_key]
        # on operation below address information counter is filled with agent info
        addresses_dict[address_info.address] += AddressDedupInfo(
            source_agent=address_info.source_agent,
            count=1 if address_info.event_category == EventCategory.add_address else -1,
        )
        dedup_agents_dict[dicts_key].add(address_info.source_agent)
    return call_destination_category_dict, dedup_agents_dict


def aggregate_by_agent(
    add_address: bool, data: defaultdict[IPv4Address, AddressDedupInfo], agent_name: str
) -> list[IPv4Address]:
    return [
        key
        for key, address_record in data.items()
        if (address_record.count > 0 if add_address else address_record.count < 0)
        and address_record.source_agent == agent_name
    ]


class BlackListSync:
    def __init__(self, call_uri: str, token: Optional[str]):
        self.call_uri = call_uri
        self.token = token

    def compose_call_uri(self, event_category: EventCategory, address_category: AddressCategory) -> str:
        address_prefix = (
            BLACKLIST_BANNED_ADDRESS_PREFIX
            if address_category == AddressCategory.banned
            else BLACKLIST_ALLOWED_ADDRESS_PREFIX
        )
        address_suffix = (
            BLACKLIST_ADD_METHOD_SUFFIX
            if event_category == EventCategory.add_address
            else BLACKLIST_DELETE_METHOD_SUFFIX
        )
        return f'{self.call_uri}{address_prefix}{address_suffix}'

    async def sync_data(
        self, event_category: EventCategory, address_category: AddressCategory, data: BlackListCallSchema
    ):
        async with AsyncClient() as client:
            logging.debug(
                'Calling Blacklist host for %s, records count: %d',
                'adding addresses' if event_category == EventCategory.add_address else 'deleting addresses',
                len(data.addresses),
            )
            call_uri = self.compose_call_uri(event_category, address_category)
            headers = {'Content-type': 'application/json'}
            if self.token:
                headers |= {'Authorization': f'Bearer {self.token}'}
            try:
                r = await client.post(call_uri, json=data.model_dump(mode='json'), headers=headers)
                r.raise_for_status()
                logging.debug('Successful call to %s, response: %s', r.request.url, r.text)
            except RequestError as exc:
                logging.error(f'Error while requesting Blacklist host {exc.request.url!r}, details: {str(exc)}')
            except HTTPStatusError as exc:
                logging.error(
                    f'HTTP Error {exc.response.status_code} while requesting Blacklist host '
                    f'{exc.request.url!r}, details: {str(exc)}'
                )

    async def process_data(self, addresses_info: list[BlackListSyncSchema]):
        # Process parsed data with deduplication
        current_time = curr_datetime()
        addresses_dict, agents_dict = deduplicate_addresses_data(addresses_info)
        # iterate over every DedupDestinationCategory object
        for destination_key, addresses_info_dict in addresses_dict.items():
            # process unblock operations
            for agent_name in agents_dict[destination_key]:
                delete_addresses: list[IPv4Address] = aggregate_by_agent(False, addresses_info_dict, agent_name)
                if delete_addresses:
                    await self.sync_data(
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
                    await self.sync_data(
                        EventCategory.add_address,
                        destination_key.address_category,
                        BlackListCallSchema(
                            source_agent=agent_name,
                            action_time=current_time,
                            addresses=add_addresses,
                            address_group=destination_key.address_group,
                        ),
                    )
