# Application config schemas
from pathlib import Path

from pydantic import BaseModel
from pydantic import field_validator

from .watcher_schema import WatcherSchema


class ConfigLogSchema(BaseModel):
    # TODO cover config with tests
    level: str = 'INFO'
    filename: str = ''
    console: bool = True

    @field_validator('level')
    @classmethod
    def upper(cls, log_level: str) -> str:
        assert type(log_level) is str, 'level value should be defined as string'
        log_level_upper = log_level.upper()
        assert log_level_upper in (
            'DEBUG',
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL',
        ), f'Wrong log level specified: {log_level_upper}'
        return log_level_upper


class ConfigSchema(BaseModel):
    watchers: list[WatcherSchema]
    status_file: Path
    blacklist_uri: str
    blacklist_token: str = ''
    logging: ConfigLogSchema = ConfigLogSchema()
