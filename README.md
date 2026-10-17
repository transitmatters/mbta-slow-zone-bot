# mbta-slow-zone-bot
![lint](https://github.com/transitmatters/mbta-slow-zone-bot/workflows/lint/badge.svg?branch=main)
![deploy](https://github.com/transitmatters/mbta-slow-zone-bot/workflows/deploy/badge.svg?branch=main)

A Twitter & Mastodon & Slack & Bluesky bot to track MBTA slow zones

https://twitter.com/mbtaslowzonebot

https://better.boston/@mbtaslowzonebot

## Setup

### Requirements

- Python 3.14 (pinned in `.python-version`). We recommend [mise](https://mise.jdx.dev): `mise trust && mise install`
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Installation

```bash
uv sync --group dev
uv run pre-commit install
```

## How to Run

The bot runs on AWS Lambda via [Chalice](https://github.com/aws/chalice), once a day at 13:05 UTC (9:05 AM EDT / 8:05 AM EST). The schedule is defined in [`slowzonebot/app.py`](slowzonebot/app.py).

To run it locally, set the proper environment variables (see `slowzonebot/chalicelib/slowzones.py`), then:

```bash
uv run python -m slowzonebot.chalicelib.slowzones
```

Use the `--dry-run` flag to run the bot without posting (no credentials needed), and the `--debug` flag for additional logging.

## Linting

```bash
uv run ruff check slowzonebot
uv run ruff format slowzonebot
```

## Deploying

Merging to `main` deploys automatically through the `deploy` GitHub Actions workflow, which runs [`devops/deploy.sh`](devops/deploy.sh). That script packages the Chalice app and deploys the `mbta-slow-zone-bot` CloudFormation stack. Bot credentials are stored as GitHub secrets and passed to the Lambda as CloudFormation parameters.

## Support TransitMatters
If you've found this app helpful or interesting, please consider [donating](https://transitmatters.org/donate) to TransitMatters to help support our mission to provide data-driven advocacy for a more reliable, sustainable, and equitable transit system in Metropolitan Boston.
