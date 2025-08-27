import os

import requests

from utils import format_fixed_slow_zone, format_new_slow_zone

SLOW_ZONE_BOT_SLACK_WEBHOOK_URL = os.environ.get("SLOW_ZONE_BOT_SLACK_WEBHOOK_URL")


def send_new_slow_zone_slacks(sz):
    for line in sz:
        for z in line:
            output = format_new_slow_zone(z)
            requests.post(
                SLOW_ZONE_BOT_SLACK_WEBHOOK_URL,
                json={"text": output},
            )


def send_fixed_slow_zone_slacks(sz):
    for line in sz:
        for z in line:
            output = format_fixed_slow_zone(z)
            requests.post(
                SLOW_ZONE_BOT_SLACK_WEBHOOK_URL,
                json={"text": output},
            )
