import logging
import os

from chalice import Chalice, ConvertToMiddleware, Cron
from chalicelib import slowzones
from datadog_lambda.wrapper import datadog_lambda_wrapper

# Configure logging level from environment variable (default: INFO)
# Set LOG_LEVEL=DEBUG in environment to enable debug logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))

app = Chalice(app_name="mbta-slow-zone-bot")

app.register_middleware(ConvertToMiddleware(datadog_lambda_wrapper))


# Runs once a day at 13:05 UTC (9:05 AM EDT / 8:05 AM EST)
@app.schedule(Cron("5", "13", "*", "*", "?", "*"))
def post_slow_zones(event):
    """Post yesterday's new and fixed slow zones to Twitter, Slack, Mastodon, and Bluesky."""
    slowzones.run()
