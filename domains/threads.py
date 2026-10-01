import os

import requests

from utils import format_fixed_slow_zone, format_new_slow_zone

THREADS_ACCESS_TOKEN = os.environ.get("THREADS_ACCESS_TOKEN")
THREADS_API_URL = "https://graph.threads.net/v1.0/me/threads"


def post_thread(text):
    # auto_publish_text creates and publishes a text post in a single call
    response = requests.post(
        THREADS_API_URL,
        data={
            "media_type": "TEXT",
            "text": text,
            "auto_publish_text": "true",
            "access_token": THREADS_ACCESS_TOKEN,
        },
    )
    response.raise_for_status()
    return response.json()


def send_new_slow_zone_threads(sz):
    for line in sz:
        for z in line:
            output = format_new_slow_zone(z)
            post_thread(output)


def send_fixed_slow_zone_threads(sz):
    for line in sz:
        for z in line:
            output = format_fixed_slow_zone(z)
            post_thread(output)
