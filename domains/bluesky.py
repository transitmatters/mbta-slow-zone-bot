from atproto import Client
from utils import format_fixed_slow_zone, format_new_slow_zone, format_updated_slow_zone
import re


def parse_urls(text: str) -> list[dict]:
    """
    credit: https://raw.githubusercontent.com/bluesky-social/cookbook/refs/heads/main/python-bsky-post/create_bsky_post.py
    """
    spans = []
    # partial/naive URL regex based on: https://stackoverflow.com/a/3809435
    # tweaked to disallow some training punctuation
    url_regex = rb"[$|\W](https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*[-a-zA-Z0-9@%_\+~#//=])?)"
    text_bytes = text.encode("UTF-8")
    for m in re.finditer(url_regex, text_bytes):
        spans.append(
            {
                "start": m.start(1),
                "end": m.end(1),
                "url": m.group(1).decode("UTF-8"),
            }
        )
    return spans


def parse_facets(text: str) -> list[dict]:
    """
    parses post text and returns a list of app.bsky.richtext.facet objects for any mentions (@handle.example.com) or URLs (https://example.com)

    indexing must work with UTF-8 encoded bytestring offsets, not regular unicode string offsets, to match Bluesky API expectations

    modified from: https://raw.githubusercontent.com/bluesky-social/cookbook/refs/heads/main/python-bsky-post/create_bsky_post.py
    """
    facets = []

    for u in parse_urls(text):
        facets.append(
            {
                "index": {
                    "byteStart": u["start"],
                    "byteEnd": u["end"],
                },
                "features": [
                    {
                        "$type": "app.bsky.richtext.facet#link",
                        # NOTE: URI ("I") not URL ("L")
                        "uri": u["url"],
                    }
                ],
            }
        )
    return facets


def send_new_slow_zone_bsky(sz, client: Client):
    for line in sz:
        for z in line:
            output = format_new_slow_zone(z)
            client.send_post(text=output, facets=parse_facets(output))


def send_fixed_slow_zone_bsky(sz, client: Client):
    for line in sz:
        for z in line:
            output = format_fixed_slow_zone(z)
            client.send_post(text=output, facets=parse_facets(output))


def send_updated_slow_zone_bsky(sz, client: Client):
    for line in sz:
        for z in line:
            output = format_updated_slow_zone(z)
            client.send_post(text=output, facets=parse_facets(output))
