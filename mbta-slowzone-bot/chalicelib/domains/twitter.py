from utils import chunks, format_fixed_slow_zone, format_new_slow_zone, format_updated_slow_zone
from tweepy import Client
import logging


def send_tweet_threads(tt_map, client: Client):
    for map in tt_map:
        split_map = map.split("\n")
        chunked_map = list(chunks(split_map, 7))
        tweet = client.create_tweet(text="\n".join(list(chunked_map)[0]))
        logging.info(f"tweet: {tweet}")


def send_new_slow_zone_tweets(sz, client: Client):
    for line in sz:
        for z in line:
            output = format_new_slow_zone(z)
            client.create_tweet(text=output)


def send_fixed_slow_zone_tweets(sz, client: Client):
    for line in sz:
        for z in line:
            output = format_fixed_slow_zone(z)
            client.create_tweet(text=output)


def send_updated_slow_zone_tweets(sz, client: Client):
    for line in sz:
        for z in line:
            output = format_updated_slow_zone(z)
            client.create_tweet(text=output)
