from dataclasses import dataclass

from .blacklist_schema import AddressCategory


@dataclass(frozen=True)
class CallDestinationCategory:
    """Class used as key in addresses deduplication routine"""

    address_group: str
    address_category: AddressCategory
