import zoneinfo

# Timezone constants
CUR_TZ = zoneinfo.ZoneInfo('Europe/Moscow')
UTC_TZ = zoneinfo.ZoneInfo('UTC')

# Logging settings
LOG_FORMAT = '%(asctime)s %(levelname)s [%(name)s] %(message)s'

# Watcher settings
WATCH_PERIOD = 2  # interval for watcher checks (in seconds)

# Blacklist handlers URIs
BLACKLIST_ADDRESS_HANDLER = '/addresses/banned'
BLACKLIST_BLOCK_METHOD_URI = '/add'
BLACKLIST_UNBLOCK_METHOD_URI = '/delete'
