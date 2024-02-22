from dataclasses import dataclass


@dataclass(frozen=True)
class AddressDedupInfo:
    """Immutable address dedup info object - used for deduplication of addresses add/delete records"""

    count: int = 0
    source_agent: str = ''

    def __add__(self, other: 'AddressDedupInfo'):
        # add and set source_agent with new one
        return AddressDedupInfo(source_agent=other.source_agent, count=self.count + other.count)

    def __sub__(self, other: 'AddressDedupInfo'):
        # subtract and set source_agent with new one
        return AddressDedupInfo(source_agent=other.source_agent, count=self.count - other.count)
