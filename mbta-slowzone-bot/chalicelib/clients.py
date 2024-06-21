import tweepy
import mastodon as mastodon
import os
from chalicelib.constants import (
    ACCESS_KEY,
    ACCESS_SECRET,
    CONSUMER_KEY,
    CONSUMER_SECRET,
    MASTODON_CLIENT_KEY,
    MASTODON_CLIENT_SECRET,
    MASTODON_ACCESS_TOKEN,
)

twitter_client = api = tweepy.Client(
    bearer_token=os.environ.get("BEARER_TOKEN"),
    access_token=ACCESS_KEY,
    access_token_secret=ACCESS_SECRET,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
)

mastodon_client = mastodon.Mastodon(
    api_base_url="https://better.boston",
    client_id=MASTODON_CLIENT_KEY,
    client_secret=MASTODON_CLIENT_SECRET,
    access_token=MASTODON_ACCESS_TOKEN,
)
