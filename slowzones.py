import tweepy
import mastodon as mastodon
import requests
import logging
import argparse
from datetime import timedelta, date
from domains.mastodon import send_fixed_slow_zone_toots, send_new_slow_zone_toots
from domains.twitter import send_fixed_slow_zone_tweets, send_new_slow_zone_tweets
from utils import (
    generate_grouped_slow_zone_list,
    generate_post_text_map,
    generate_new_slow_zones_list,
)
import sys
import os

ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
MASTODON_CLIENT_KEY = os.environ.get("MASTODON_CLIENT_KEY")
MASTODON_CLIENT_SECRET = os.environ.get("MASTODON_CLIENT_SECRET")
MASTODON_ACCESS_TOKEN = os.environ.get("MASTODON_ACCESS_TOKEN")
DRY_RUN = False

twitter_client = api = tweepy.Client(
    bearer_token=os.environ.get("BEARER_TOKEN"),
    access_token=ACCESS_KEY,
    access_token_secret=ACCESS_SECRET,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
)

mastodon_client = mastodon.Mastodon(
    api_base_url='https://better.boston',
    client_id=MASTODON_CLIENT_KEY,
    client_secret=MASTODON_CLIENT_SECRET,
    access_token=MASTODON_ACCESS_TOKEN
)


def main():

    slow_zones = requests.get(
        "https://dashboard.transitmatters.org/static/slowzones/all_slow.json"
    )

    grouped_sz_today = generate_grouped_slow_zone_list(slow_zones.json(), date.today())

    slowzones_ended_yesterday = generate_grouped_slow_zone_list(
        # Slow zones are 1 day behind so we want to check if zones ended two days ago
        slow_zones.json(),
        date.today() - timedelta(days=1),
    )
    logging.info(f"slowzones_ended_yesterday: {slowzones_ended_yesterday}")

    slowzones_started_yesterday = generate_new_slow_zones_list(
        slow_zones.json(), date.today()
    )
    logging.info(f"slowzones_started_yesterday: {slowzones_started_yesterday}")

    post_text_map = generate_post_text_map(grouped_sz_today)
    logging.info(f"post_text_map: {post_text_map}")

    if not DRY_RUN:
        send_new_slow_zone_tweets(slowzones_started_yesterday, twitter_client)
        send_new_slow_zone_toots(slowzones_started_yesterday, mastodon_client)

        send_fixed_slow_zone_tweets(slowzones_ended_yesterday, twitter_client)
        send_fixed_slow_zone_toots(slowzones_ended_yesterday, mastodon_client)

    # exit if no issues
    sys.exit(0)


if __name__ == '__main__':

    # argument parsing
    parser = argparse.ArgumentParser(description='MBTA Slow Zone Bot')
    parser.add_argument("--dry-run", default=False, action='store_true', help='Runs bot without posting')
    args = parser.parse_args()
    DRY_RUN = args.dry_run

    # set logging config
    logging.basicConfig(level=logging.INFO)

    # begin main program execution
    main()
