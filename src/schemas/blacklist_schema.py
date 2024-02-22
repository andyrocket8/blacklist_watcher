import datetime
from ipaddress import IPv4Address

from pydantic import BaseModel

from .watcher_schema import AddressCategory
from .watcher_schema import EventCategory


class BlackListSyncSchema(BaseModel):
    # Schema for registering watched files events
    source_agent: str
    event_category: EventCategory
    address: IPv4Address
    address_group: str = ''
    address_category: AddressCategory


class BlackListCallSchema(BaseModel):
    # Schema for calling Blacklist methods (add/delete)
    source_agent: str
    action_time: datetime.datetime
    addresses: list[IPv4Address]
    address_group: str = ''
