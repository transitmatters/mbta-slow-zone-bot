# mbta-slow-zone-bot
![lint](https://github.com/transitmatters/mbta-slow-zone-bot/workflows/lint/badge.svg?branch=main)
![run](https://github.com/transitmatters/mbta-slow-zone-bot/workflows/run/badge.svg?branch=main)

A Twitter & Mastodon & Slack & Bluesky & Threads bot to track MBTA slow zones

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

## Threads Setup
Posting to Threads uses the [Threads API](https://developers.facebook.com/docs/threads).

1. Create a Meta app with the Threads API use case and the `threads_basic` and `threads_content_publish` permissions, and add the bot's Threads account as a tester
2. Generate a long-lived access token for the bot account and store it as the `THREADS_ACCESS_TOKEN` repo secret
3. Create a fine-grained personal access token for this repo with **Secrets: read & write** and store it as the `THREADS_SECRET_WRITER_PAT` repo secret

Long-lived Threads tokens expire after 60 days, so the `refresh_threads_token` workflow refreshes the token weekly and writes the new one back to `THREADS_ACCESS_TOKEN`.

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
