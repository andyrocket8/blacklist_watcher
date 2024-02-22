import logging
from typing import Optional

from httpx import AsyncClient
from httpx import HTTPStatusError
from httpx import RequestError

from src.core.settings import BLACKLIST_ADD_METHOD_SUFFIX
from src.core.settings import BLACKLIST_ALLOWED_ADDRESS_PREFIX
from src.core.settings import BLACKLIST_BANNED_ADDRESS_PREFIX
from src.core.settings import BLACKLIST_DELETE_METHOD_SUFFIX
from src.schemas.blacklist_schema import BlackListCallSchema
from src.schemas.watcher_schema import AddressCategory
from src.schemas.watcher_schema import EventCategory


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
                'Calling Blacklist host for %s, records count: %d, address category: %s',
                'adding addresses' if event_category == EventCategory.add_address else 'deleting addresses',
                len(data.addresses),
                'banned addresses' if address_category == AddressCategory.banned else 'allowed addresses',
            )
            call_uri = self.compose_call_uri(event_category, address_category)
            # fill headers of request
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
