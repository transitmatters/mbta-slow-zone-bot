# mbta-slow-zone-bot
![lint](https://github.com/transitmatters/mbta-slow-zone-bot/workflows/lint/badge.svg?branch=main)
![run](https://github.com/transitmatters/mbta-slow-zone-bot/workflows/run/badge.svg?branch=main)

A Twitter & Mastodon & Slack & Bluesky bot to track MBTA slow zones

https://twitter.com/mbtaslowzonebot

https://better.boston/@mbtaslowzonebot

## How to Run
Make sure you set the proper environmental variables then you can use the following commands to run the bot

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
$ poetry install
$ poetry run python3 slowzones.py
```

Note you can use the `--dry-run` flag to run the both without posting to Twitter/Mastodon, and the `--debug` flag for additional logging

## Linting
You can run the linter against any code changes with the following commands

```bash
$ curl -sSL https://install.python-poetry.org | python3 -
$ poetry install
$ poetry run flake8
$ poetry run black .
```

## Support TransitMatters
If you've found this app helpful or interesting, please consider [donating](https://transitmatters.org/donate) to TransitMatters to help support our mission to provide data-driven advocacy for a more reliable, sustainable, and equitable transit system in Metropolitan Boston.
