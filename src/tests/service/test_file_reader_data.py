from src.schemas.watcher_schema import WatcherRule

OK_TEST_FILE_DATA = (
    """2023-12-17 00:00:26,822 fail2ban.filter         [3621555]: INFO    [sshd] Found """
    + """139.19.117.195 - 2023-12-17 00:00:26
2023-12-17 00:01:43,082 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 43.156.33.183
2023-12-17 00:02:11,166 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 43.130.57.4
2023-12-17 00:02:34,442 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 2.83.61.37
2023-12-17 00:02:35,076 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 170.106.101.133
2023-12-17 00:02:42,319 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 186.31.95.163
2023-12-17 00:03:03,584 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 43.156.240.183
2023-12-17 00:03:50,291 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 110.42.234.146
2023-12-17 00:04:01,546 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 124.221.163.28
2023-12-17 00:04:19,639 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 193.112.136.96
2023-12-17 00:04:38,300 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 24.144.85.171
2023-12-17 00:04:42,348 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 101.35.56.189
2023-12-17 00:05:38,462 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 124.223.100.217
2023-12-17 00:06:22,559 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 134.122.12.11
2023-12-17 00:07:01,246 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 121.204.251.131
2023-12-17 00:07:09,328 fail2ban.filter         [3621555]: INFO    [sshd] Found 24.144.85.171 - 2023-12-17 00:07:09
2023-12-17 00:07:11,331 fail2ban.filter         [3621555]: INFO    [sshd] Found 24.144.85.171 - 2023-12-17 00:07:11
2023-12-17 00:07:39,047 fail2ban.filter         [3621555]: INFO    [sshd] Found 170.64.210.196 - 2023-12-17 00:07:38
2023-12-17 00:07:39,339 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 170.64.210.196
2023-12-17 00:08:34,568 fail2ban.filter         [3621555]: INFO    [sshd] Found 134.122.12.11 - 2023-12-17 00:08:34
2023-12-17 00:08:36,424 fail2ban.filter         [3621555]: INFO    [sshd] Found 134.122.12.11 - 2023-12-17 00:08:36
2023-12-17 00:10:40,232 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 101.34.218.206
2023-12-17 00:11:48,362 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 170.64.188.209
2023-12-17 00:12:32,451 fail2ban.filter         [3621555]: INFO    [sshd] Found 85.209.11.226 - 2023-12-17 00:12:32
2023-12-17 00:12:34,203 fail2ban.filter         [3621555]: INFO    [sshd] Found 85.209.11.226 - 2023-12-17 00:12:34
2023-12-17 00:13:14,577 fail2ban.filter         [3621555]: INFO    [sshd] Found 170.64.188.209 - 2023-12-17 00:13:14
2023-12-17 00:13:16,738 fail2ban.filter         [3621555]: INFO    [sshd] Found 170.64.188.209 - 2023-12-17 00:13:16
2023-12-17 00:14:02,588 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 82.154.230.131
2023-12-17 00:14:13,258 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 43.134.82.51
2023-12-17 00:14:14,500 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 134.209.214.171
2023-12-17 00:14:29,156 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 51.89.163.215
2023-12-17 00:14:35,202 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 170.187.155.47
2023-12-17 00:14:47,256 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 68.178.168.70
2023-12-17 00:14:47,291 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 152.70.217.117
2023-12-17 00:14:47,638 fail2ban.filter         [3621555]: INFO    [sshd] Found 134.122.12.11 - 2023-12-17 00:14:47
2023-12-17 00:14:48,523 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 43.130.244.94
2023-12-17 00:14:49,634 fail2ban.filter         [3621555]: INFO    [sshd] Found 134.122.12.11 - 2023-12-17 00:14:49
2023-12-17 00:14:51,161 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 142.93.63.89
2023-12-17 00:14:53,195 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 43.134.109.110
2023-12-17 00:14:56,382 fail2ban.filter         [3621555]: INFO    [sshd] Found 24.144.85.171 - 2023-12-17 00:14:56
2023-12-17 00:14:59,285 fail2ban.filter         [3621555]: INFO    [sshd] Found 24.144.85.171 - 2023-12-17 00:14:58
2023-12-17 00:15:22,468 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 43.130.37.230
2023-12-17 00:16:18,587 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 124.126.75.104
2023-12-17 00:19:01,995 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:01
2023-12-17 00:19:05,829 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:05
2023-12-17 00:19:09,186 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:09
2023-12-17 00:19:13,425 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:13
2023-12-17 00:19:16,892 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:16
2023-12-17 00:19:17,072 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 185.244.25.14
2023-12-17 00:20:38,427 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 81.70.86.88
2023-12-17 00:20:54,704 fail2ban.filter         [3621555]: INFO    [sshd] Found 170.64.188.209 - 2023-12-17 00:20:54
2023-12-17 00:20:56,992 fail2ban.filter         [3621555]: INFO    [sshd] Found 170.64.188.209 - 2023-12-17 00:20:56
2023-12-17 00:21:00,491 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 141.148.143.73
2023-12-17 00:21:03,222 fail2ban.filter         [3621555]: INFO    [sshd] Found 134.122.12.11 - 2023-12-17 00:21:03
2023-12-17 00:21:03,731 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 134.122.12.11
2023-12-17 00:21:05,984 fail2ban.filter         [3621555]: INFO    [sshd] Found 134.122.12.11 - 2023-12-17 00:21:05
2023-12-17 00:22:31,087 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 117.72.34.95
2023-12-17 00:22:45,518 fail2ban.filter         [3621555]: INFO    [sshd] Found 24.144.85.171 - 2023-12-17 00:22:45
2023-12-17 00:22:45,750 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 24.144.85.171
2023-12-17 00:22:48,228 fail2ban.filter         [3621555]: INFO    [sshd] Found 24.144.85.171 - 2023-12-17 00:22:48
2023-12-17 00:28:36,111 fail2ban.filter         [3621555]: INFO    [sshd] Found 170.64.188.209 - 2023-12-17 00:28:36
"""
)


OK_TEST_FILE_DATA_SI = (
    """2023-12-17 00:00:26,822 fail2ban.filter         [3621555]: INFO    [sshd] Found """
    + """139.19.117.195 - 2023-12-17 00:00:26
2023-12-17 00:01:43,082 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.1
2023-12-17 00:02:11,166 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.2
2023-12-17 00:02:34,442 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.3
2023-12-17 00:02:35,076 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.4
2023-12-17 00:02:42,319 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.5
2023-12-17 00:03:03,584 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.6
2023-12-17 00:03:50,291 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.7
2023-12-17 00:04:01,546 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.8
2023-12-17 00:04:19,639 fail2ban.actions        [3621555]: NOTICE  [www] Unban 10.100.0.1
2023-12-17 00:04:38,300 fail2ban.actions        [3621555]: NOTICE  [www] Unban 10.100.0.2
2023-12-17 00:07:09,328 fail2ban.filter         [3621555]: INFO    [sshd] Found 10.100.1.3 - 2023-12-17 00:07:09
2023-12-17 00:04:42,348 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 10.100.0.1
2023-12-17 00:05:38,462 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 10.100.0.2
2023-12-17 00:06:22,559 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 10.100.0.3
2023-12-17 00:07:01,246 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 10.100.0.4
2023-12-17 00:07:09,328 fail2ban.filter         [3621555]: INFO    [sshd] Found 10.100.0.1 - 2023-12-17 00:07:09
2023-12-17 00:07:11,331 fail2ban.filter         [3621555]: INFO    [sshd] Found 10.100.0.1 - 2023-12-17 00:07:11
2023-12-17 00:07:39,047 fail2ban.filter         [3621555]: INFO    [sshd] Found 10.100.0.1 - 2023-12-17 00:07:38
2023-12-17 00:07:39,339 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 10.100.0.1
2023-12-17 00:08:34,568 fail2ban.filter         [3621555]: INFO    [sshd] Found 192.168.1.9 - 2023-12-17 00:08:34
2023-12-17 00:08:36,424 fail2ban.filter         [3621555]: INFO    [sshd] Found 192.168.1.9 - 2023-12-17 00:08:36
2023-12-17 00:10:40,232 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 10.100.0.10
2023-12-17 00:11:48,362 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.10
2023-12-17 00:12:32,451 fail2ban.filter         [3621555]: INFO    [sshd] Found 192.168.1.9 - 2023-12-17 00:12:32
2023-12-17 00:12:34,203 fail2ban.filter         [3621555]: INFO    [sshd] Found 192.168.1.9 - 2023-12-17 00:12:34
2023-12-17 00:13:14,577 fail2ban.filter         [3621555]: INFO    [sshd] Found 192.168.1.10 - 2023-12-17 00:13:14
2023-12-17 00:13:16,738 fail2ban.filter         [3621555]: INFO    [sshd] Found 192.168.1.10 - 2023-12-17 00:13:16
2023-12-17 00:14:02,588 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.11
2023-12-17 00:14:13,258 fail2ban.actions        [3621555]: NOTICE  [www] Unban 192.168.1.12
2023-12-17 00:14:14,500 fail2ban.actions        [3621555]: NOTICE  [ftp] Unban 192.168.1.13
2023-12-17 00:14:29,156 fail2ban.actions        [3621555]: NOTICE  [ftp] Unban 192.168.1.14
2023-12-17 00:14:35,202 fail2ban.actions        [3621555]: NOTICE  [ftp] Unban 192.168.1.15
2023-12-17 00:14:47,256 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 192.168.1.11 - Some duplication
2023-12-17 00:14:47,291 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 10.100.0.12
2023-12-17 00:14:47,638 fail2ban.filter         [3621555]: INFO    [www] Found 10.100.0.12 - 2023-12-17 00:14:47
2023-12-17 00:14:48,523 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 10.100.0.13
2023-12-17 00:14:49,634 fail2ban.filter         [3621555]: INFO    [sshd] Found 192.168.1.1 - 2023-12-17 00:14:49
2023-12-17 00:14:50,638 fail2ban.filter         [3621555]: INFO    [www] Found 10.100.0.12 - 2023-12-17 00:14:47
2023-12-17 00:14:51,161 fail2ban.actions        [3621555]: NOTICE  [ftp] Unban 10.100.0.1
2023-12-17 00:14:53,195 fail2ban.actions        [3621555]: NOTICE  [ftp] Unban 43.134.109.110
2023-12-17 00:14:56,382 fail2ban.filter         [3621555]: INFO    [sshd] Found 192.168.1.1 - 2023-12-17 00:14:56
2023-12-17 00:14:59,285 fail2ban.filter         [3621555]: INFO    [sshd] Found 192.168.1.1 - 2023-12-17 00:14:58
2023-12-17 00:15:22,468 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 43.130.37.230
2023-12-17 00:16:18,587 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 124.126.75.104
2023-12-17 00:19:01,995 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:01
2023-12-17 00:19:05,829 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:05
2023-12-17 00:19:09,186 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:09
2023-12-17 00:19:13,425 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:13
2023-12-17 00:19:16,892 fail2ban.filter         [3621555]: INFO    [sshd] Found 185.244.25.14 - 2023-12-17 00:19:16
2023-12-17 00:19:17,072 fail2ban.actions        [3621555]: NOTICE  [www] Ban 10.100.0.11
2023-12-17 00:20:38,427 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 81.70.86.88
2023-12-17 00:20:54,704 fail2ban.filter         [3621555]: INFO    [sshd] Found 170.64.188.209 - 2023-12-17 00:20:54
2023-12-17 00:20:56,992 fail2ban.filter         [3621555]: INFO    [sshd] Found 170.64.188.209 - 2023-12-17 00:20:56
2023-12-17 00:21:00,491 fail2ban.actions        [3621555]: NOTICE  [sshd] Unban 141.148.143.73
2023-12-17 00:21:03,222 fail2ban.filter         [3621555]: INFO    [sshd] Found 134.122.12.11 - 2023-12-17 00:21:03
2023-12-17 00:21:03,731 fail2ban.actions        [3621555]: NOTICE  [www] Ban 192.168.1.16
2023-12-17 00:21:05,984 fail2ban.filter         [3621555]: INFO    [sshd] Found 134.122.12.11 - 2023-12-17 00:21:05
2023-12-17 00:22:31,087 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 192.168.1.12
2023-12-17 00:22:45,518 fail2ban.filter         [3621555]: INFO    [sshd] Found 24.144.85.171 - 2023-12-17 00:22:45
2023-12-17 00:22:45,750 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 10.100.0.13
2023-12-17 00:22:48,228 fail2ban.filter         [3621555]: INFO    [sshd] Found 24.144.85.171 - 2023-12-17 00:22:48
2023-12-17 00:28:36,111 fail2ban.filter         [3621555]: INFO    [sshd] Found 170.64.188.209 - 2023-12-17 00:28:36
2023-12-17 00:22:45,750 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 192.168.1.2
2023-12-17 00:22:48,010 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 192.168.1.3
2023-12-17 00:22:49,010 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 192.168.1.4
2023-12-17 00:22:50,010 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 192.168.1.4 - some duplication
2023-12-17 00:22:51,010 fail2ban.actions        [3621555]: NOTICE  [sshd-out] Ban 10.100.0.11 -- should be in banned sshd-out # noqa E501

"""
)


def get_regex_str(agent_name: str) -> str:
    return r'.*\[' + agent_name + r'\]\s(Ban|Unban)\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*'


TRAILER_DICT = {
    'address_description': {'tuple_position': 1},
    'event_description': {
        'tuple_position': 0,
        'event_mapping': [
            {'event_string': 'Ban', 'event_category': 'add_address'},
            {'event_string': 'Unban', 'event_category': 'del_address'},
        ],
    },
}

SSHD_AGENT_NAME = 'sshd'
SI_RULE_SSHD = WatcherRule(
    **{'regex': get_regex_str(SSHD_AGENT_NAME), 'agent': SSHD_AGENT_NAME, 'address_category': 'banned'}
    | TRAILER_DICT
    | {'address_group': 'banned_sshd'}
)

SSHD_OUT_AGENT_NAME = 'sshd-out'
SI_RULE_SSHD_OUT = WatcherRule(
    **{'regex': get_regex_str(SSHD_OUT_AGENT_NAME), 'agent': SSHD_OUT_AGENT_NAME, 'address_category': 'banned'}
    | TRAILER_DICT
    | {'address_group': 'banned_sshd'}
)

FTP_AGENT_NAME = 'ftp'
SI_RULE_SSHD_SEP_GROUP = WatcherRule(
    **{'regex': get_regex_str(FTP_AGENT_NAME), 'agent': FTP_AGENT_NAME, 'address_category': 'banned'}
    | TRAILER_DICT
    | {'address_group': 'banned_ftp'}
)

WWW_AGENT_NAME = 'www'
SI_RULE_WWW = WatcherRule(
    **{'regex': get_regex_str(WWW_AGENT_NAME), 'agent': WWW_AGENT_NAME, 'address_category': 'allowed'} | TRAILER_DICT
)

SI_RULE_SSHD.event_description.fill_dictionary()
SI_RULE_WWW.event_description.fill_dictionary()
SI_RULE_SSHD_SEP_GROUP.event_description.fill_dictionary()
SI_RULE_SSHD_OUT.event_description.fill_dictionary()

TEST_RULES: list[WatcherRule] = [SI_RULE_SSHD, SI_RULE_WWW, SI_RULE_SSHD_SEP_GROUP, SI_RULE_SSHD_OUT]
