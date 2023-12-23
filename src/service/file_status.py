import datetime
from pathlib import Path
from typing import Optional
from typing import Union

from src.core.settings import CUR_TZ


class FileStatus:
    """
    Class for storing file status information and detect of file status changes
    """

    def __init__(
        self,
        file_name: Union[str, Path],
        current_date: Optional[datetime.datetime] = None,
        current_size: Optional[int] = None,
    ):
        """
        :param file_name: file to track
        :type: Union[str, Path]
        :param current_date: date and time of file (set in constructor and on [file_date_changed] function call)
        :type: Optional[datetime.datetime]
        :param current_size: last stored file size. Set in constructor and on [get_size_change] function call
        :type: Optional[int]
        """
        self.file_path: Path = Path(file_name)
        # set current file date from constructor parameter if it filled else from file itself
        self._file_date: Optional[datetime.datetime] = self.calc_date() if current_date is None else current_date
        # set current size from constructor parameter if it filled else from file itself
        self._size: Optional[int] = self.calc_size() if current_size is None else current_size

    @property
    def current_date(self) -> Optional[datetime.datetime]:
        # stored current time. Can de update by self.file_date_changed call
        return self._file_date

    @property
    def current_size(self) -> Optional[int]:
        # stored current file size. Can de update by self.file_size_changed call
        return self._size

    def calc_date(self) -> Optional[datetime.datetime]:
        """
        Get file modification date. Return None on file access error
        """
        try:
            return datetime.datetime.fromtimestamp(self.file_path.stat().st_mtime, tz=CUR_TZ)
        except (FileNotFoundError, OSError):
            return None

    def calc_size(self) -> Optional[int]:
        """
        Get current size. Return None if we get error on file access
        """
        try:
            return self.file_path.stat().st_size
        except (FileNotFoundError, OSError):
            return None

    @property
    def file_date_changed(self) -> bool:
        """
        Check change status and save new modification date (if changed). If file is not accessible then store None
        :return: True if file changed or file become unavailable
        :rtype bool
        """
        current_date = self.calc_date()
        try:
            return current_date != self._file_date
        finally:
            self._file_date = current_date

    @property
    def file_size_changed(self) -> bool:
        """
        Get current size of file. If file is nit accessible return None
        Save last size in self.current_size
        :return: whether size changed or not
        :rtype bool
        """
        size = self.calc_size()
        try:
            return self._size != size
        finally:
            self._size = size

    @property
    def changed(self) -> bool:
        # checking modification with binary function ensuring both change calculations have been done
        return self.file_date_changed | self.file_size_changed

    def is_available(self) -> bool:
        # return True if file is available for access. Use this function after using "file_date_changed" function
        return self._file_date is not None
