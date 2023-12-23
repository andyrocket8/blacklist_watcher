import logging
from collections import defaultdict
from ipaddress import IPv4Address
from typing import Optional

from httpx import AsyncClient
from httpx import HTTPStatusError
from httpx import RequestError

from src.core.settings import BLACKLIST_ADDRESS_HANDLER
from src.core.settings import BLACKLIST_BLOCK_METHOD_URI
from src.core.settings import BLACKLIST_UNBLOCK_METHOD_URI
from src.schemas.blacklist_schema import BlackListCallSchema
from src.schemas.blacklist_schema import BlackListSyncSchema
from src.schemas.watcher_schema import EventCategory
from src.utils import curr_datetime


class BlackListSync:
    def __init__(self, call_uri: str, token: Optional[str]):
        self.call_uri = call_uri
        self.token = token

    async def sync_data(self, category: EventCategory, data: BlackListCallSchema):
        async with AsyncClient() as client:
            logging.debug(
                'Calling Blacklist host for %s, records count: %d',
                'blocking' if category == EventCategory.block else 'unblocking',
                len(data.addresses),
            )
            call_uri = (
                f'{self.call_uri}{BLACKLIST_ADDRESS_HANDLER}'
                f'{BLACKLIST_BLOCK_METHOD_URI if category == EventCategory.block else BLACKLIST_UNBLOCK_METHOD_URI}'
            )
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

    async def process_data(self, agent_name: str, addresses_info: list[BlackListSyncSchema]):
        current_time = curr_datetime()
        addresses_count: defaultdict[IPv4Address, int] = defaultdict(int)
        #
        for address_info in addresses_info:
            addresses_count[address_info.address] += 1 if address_info.category == EventCategory.block else -1
        block_addresses: list[IPv4Address] = [key for key, value in addresses_count.items() if value > 0]
        unblock_addresses: list[IPv4Address] = [key for key, value in addresses_count.items() if value < 0]
        if block_addresses:
            await self.sync_data(
                EventCategory.block,
                BlackListCallSchema(source_agent=agent_name, action_time=current_time, addresses=block_addresses),
            )
        if unblock_addresses:
            await self.sync_data(
                EventCategory.unblock,
                BlackListCallSchema(source_agent=agent_name, action_time=current_time, addresses=unblock_addresses),
            )
