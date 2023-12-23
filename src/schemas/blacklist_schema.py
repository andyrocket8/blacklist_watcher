import datetime
from ipaddress import IPv4Address

from pydantic import BaseModel

from .watcher_schema import EventCategory


class BlackListSyncSchema(BaseModel):
    category: EventCategory
    address: IPv4Address


class BlackListCallSchema(BaseModel):
    source_agent: str
    action_time: datetime.datetime
    addresses: list[IPv4Address]
