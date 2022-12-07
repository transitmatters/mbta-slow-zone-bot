import tweepy
import requests
from datetime import timedelta, date
from utils import (
    generate_grouped_slow_zone_list,
    generate_tweet_text_map,
    generate_new_slow_zones_list,
    send_new_slow_zone_tweets,
    send_fixed_slow_zone_tweets,
)
import os


ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
print(os.environ)

client = api = tweepy.Client(
    bearer_token=os.environ.get("BEARER_TOKEN"),
    access_token=ACCESS_KEY,
    access_token_secret=ACCESS_SECRET,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
)

slow_zones = requests.get(
    "https://dashboard.transitmatters.org/static/slowzones/all_slow.json"
)

grouped_sz_today = generate_grouped_slow_zone_list(slow_zones.json(), date.today())

slowzones_ended_yesterday = generate_grouped_slow_zone_list(
    # Slow zones are 1 day behind so we want to check if zones ended two days ago
    slow_zones.json(),
    date.today() - timedelta(days=1),
)

slowzones_started_yesterday = generate_new_slow_zones_list(
    slow_zones.json(), date.today()
)

tweet_text_map = generate_tweet_text_map(grouped_sz_today)

send_new_slow_zone_tweets(slowzones_started_yesterday, client)

send_fixed_slow_zone_tweets(slowzones_ended_yesterday, client)
