from mastodon import Mastodon
from chalicelib.output import chunks, format_fixed_slow_zone, format_new_slow_zone, format_updated_slow_zone
import logging


def send_toot_threads(tt_map, client: Mastodon):
    for map in tt_map:
        split_map = map.split("\n")
        chunked_map = list(chunks(split_map, 7))
        output = "\n".join(list(chunked_map)[0])
        toot = client.status_post(status=output)
        logging.info(f"toot: {toot}")


def send_new_slow_zone_toots(sz, client: Mastodon):
    for line in sz:
        for z in line:
            output = format_new_slow_zone(z)
            client.status_post(status=output)


def send_fixed_slow_zone_toots(sz, client: Mastodon):
    for line in sz:
        for z in line:
            output = format_fixed_slow_zone(z)
            client.status_post(status=output)


def send_updated_slow_zone_toots(sz, client: Mastodon):
    for line in sz:
        for z in line:
            output = format_updated_slow_zone(z)
            client.status_post(status=output)
