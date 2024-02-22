from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EventCategory(str, Enum):
    # Enum for event description. Map description to parsed values from log file in EventSchema class
    add_address = 'add_address'  # add address in addresses (banned or allowed) hence call .../add handle
    del_address = 'del_address'  # delete address from addresses (banned or allowed) hence call .../delete handle


class EventSchema(BaseModel):
    """
    Example (for fail2ban.log):
        EventSchema(event_string='Ban', event_category='add_address')
        EventSchema(event_string='Unban', event_category='del_address')
    """

    event_string: str  # parsed value from log file
    event_category: EventCategory  # event category for reporting to Blacklist application


class FieldDescription(BaseModel):
    tuple_position: int  # position of field in parsed tuple. Starting from 0


class EventDescription(FieldDescription):
    event_mapping: list[EventSchema]  # mapping of event values bind to EventCategory values
    event_mapping_dict: Optional[dict[str, EventCategory]] = None

    def fill_dictionary(self):
        # fill dictionary for fast event mapping
        self.event_mapping_dict = {value.event_string: value.event_category for value in self.event_mapping}


class AddressDescription(FieldDescription):
    pass


class AddressCategory(str, Enum):
    # Enum for address category. It can be 'banned' and 'allowed'
    banned = 'banned'  # address record would affect black list addresses
    allowed = 'allowed'  # address record would affect white list addresses


class WatcherRule(BaseModel):
    regex: str  # regex for events detection
    agent: str  # agent name for further reporting
    address_description: AddressDescription  # mapping for address description
    event_description: EventDescription  # mapping for event description
    address_group: Optional[
        str
    ] = ''  # address group for HTTP request. If not set - it will be 'default', no need to fill!
    address_category: AddressCategory  # banned / allowed


class WatcherSchema(BaseModel):
    filename: str  # file name
    rules: list[WatcherRule]  # Watcher rules. Can contain [1...n] rules for processing
