import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class ProcessingStatus(BaseModel):
    """
    Class for storing status of watched files
    Use for save and restore status on program reload
    """

    file_name: Path
    current_offset: int = 0
    file_date_time: Optional[datetime.datetime] = None
    file_size: Optional[int] = None
    file_hash: Optional[str] = None

    def has_no_actual_data(self):
        """Check whether processing status has actual data"""
        return self.file_size is None or self.file_date_time is None
