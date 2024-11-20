from atproto import Client
from utils import format_fixed_slow_zone, format_new_slow_zone, format_updated_slow_zone


def send_new_slow_zone_bsky(sz, client: Client):
    for line in sz:
        for z in line:
            output = format_new_slow_zone(z)
            client.send_post(text=output)


def send_fixed_slow_zone_bsky(sz, client: Client):
    for line in sz:
        for z in line:
            output = format_fixed_slow_zone(z)
            client.send_post(text=output)


def send_updated_slow_zone_bsky(sz, client: Client):
    for line in sz:
        for z in line:
            output = format_updated_slow_zone(z)
            client.send_post(text=output)
