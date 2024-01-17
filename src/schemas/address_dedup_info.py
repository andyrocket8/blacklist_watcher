from dataclasses import dataclass


@dataclass
class AddressDedupInfo:
    count: int = 0
    source_agent: str = ''

    def __add__(self, other):
        # add and set source_agent with new one
        self.count += other.count
        self.source_agent = other.source_agent
        return AddressDedupInfo(source_agent=self.source_agent, count=self.count)

    def __sub__(self, other):
        # subtract and set source_agent with new one
        self.count -= other.count
        self.source_agent = other.source_agent
        return AddressDedupInfo(source_agent=self.source_agent, count=self.count)
