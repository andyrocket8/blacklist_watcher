import datetime
from ipaddress import IPv4Address

from pydantic import BaseModel

from .watcher_schema import EventCategory


class BlackListSyncSchema(BaseModel):
    # Schema for registering watched files events
    source_agent: str
    category: EventCategory
    address: IPv4Address


class BlackListCallSchema(BaseModel):
    # Schema for calling Blacklist methods (add/delete)
    source_agent: str
    action_time: datetime.datetime
    addresses: list[IPv4Address]
