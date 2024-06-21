import requests

from chalicelib.output import format_fixed_slow_zone, format_new_slow_zone, format_updated_slow_zone
from chalicelib.constants import SLOW_ZONE_BOT_SLACK_WEBHOOK_URL


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


def send_updated_slow_zone_slacks(sz):
    for line in sz:
        for z in line:
            output = format_updated_slow_zone(z)
            requests.post(
                SLOW_ZONE_BOT_SLACK_WEBHOOK_URL,
                json={"text": output},
            )
