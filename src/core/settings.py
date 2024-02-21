import zoneinfo

# Timezone constants
CUR_TZ = zoneinfo.ZoneInfo('Europe/Moscow')
UTC_TZ = zoneinfo.ZoneInfo('UTC')

# Logging settings
LOG_FORMAT = '%(asctime)s %(levelname)s [%(name)s] %(message)s'

# Watcher settings
WATCH_PERIOD = 2  # interval for watcher checks (in seconds)
SAVE_STATUS_SCHEDULE_PERIOD = 300  # interval for saving status file

# Blacklist handlers URIs
BLACKLIST_BANNED_ADDRESS_PREFIX = '/addresses/banned'
BLACKLIST_ALLOWED_ADDRESS_PREFIX = '/addresses/allowed'
BLACKLIST_ADD_METHOD_SUFFIX = '/add'
BLACKLIST_DELETE_METHOD_SUFFIX = '/delete'
