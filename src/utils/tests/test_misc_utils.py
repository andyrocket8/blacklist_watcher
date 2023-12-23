from typing import Any

from src.utils.misc_utils import parse_regex

TEST_PARSE_REGEX_DATA: list[dict[str, Any]] = [
    {
        'pattern': r'.*(Ban|Unban).([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*',
        'inspected': '2023-12-17 00:21:03,731 fail2ban.actions        [3621555]: NOTICE  [sshd] Ban 134.122.12.11',
        'expected': (
            'Ban',
            '134.122.12.11',
        ),
    },
    {
        'pattern': r'.*(Ban|Unban).([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*',
        'inspected': '2023-12-17 00:21:03,731 fail2ban.actions        [3621555]: NOTICE  [sshd] Banned 134.122.12.11',
        'expected': None,
    },
]


def test_parse_regex():
    for step, record in enumerate(TEST_PARSE_REGEX_DATA):
        assert record['expected'] == parse_regex(
            record['pattern'], record['inspected']
        ), f'test_parse_regex failed on step {step+1}'
