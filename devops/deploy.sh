#!/bin/bash -x

REQUIRED_VARS=(
    DD_API_KEY
    ACCESS_KEY ACCESS_SECRET CONSUMER_KEY CONSUMER_SECRET BEARER_TOKEN
    MASTODON_CLIENT_KEY MASTODON_CLIENT_SECRET MASTODON_ACCESS_TOKEN
    ATP_AUTH_HANDLE ATP_AUTH_PASSWORD
    SLOW_ZONE_BOT_SLACK_WEBHOOK_URL
)
for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!var}" ]]; then
        echo "Must provide $var in environment" 1>&2
        exit 1
    fi
done

STACK_NAME=mbta-slow-zone-bot
BUCKET=mbta-slow-zone-bot-lambda-deployments

# Identify the version and commit of the current deploy
GIT_VERSION=`git describe --tags --always`
GIT_SHA=`git rev-parse HEAD`
echo "Deploying version $GIT_VERSION | $GIT_SHA"

# Adding some datadog tags to get better data
DD_TAGS="git.commit.sha:$GIT_SHA,git.repository_url:github.com/transitmatters/mbta-slow-zone-bot,version:$GIT_VERSION"

uv export --no-hashes --no-dev > slowzonebot/requirements.txt

pushd slowzonebot/

uv run chalice package --stage prod --merge-template .chalice/resources.json cfn/

# Don't echo the secrets passed as parameter overrides
set +x
aws cloudformation package --template-file cfn/sam.json --s3-bucket $BUCKET --output-template-file cfn/packaged.yaml
aws cloudformation deploy --template-file cfn/packaged.yaml --stack-name $STACK_NAME --s3-bucket $BUCKET \
    --capabilities CAPABILITY_NAMED_IAM --no-fail-on-empty-changeset \
    --tags service=$STACK_NAME env=prod \
    --parameter-overrides \
        DDApiKey="$DD_API_KEY" GitVersion="$GIT_VERSION" DDTags="$DD_TAGS" \
        TwitterAccessKey="$ACCESS_KEY" TwitterAccessSecret="$ACCESS_SECRET" \
        TwitterConsumerKey="$CONSUMER_KEY" TwitterConsumerSecret="$CONSUMER_SECRET" \
        TwitterBearerToken="$BEARER_TOKEN" \
        MastodonClientKey="$MASTODON_CLIENT_KEY" MastodonClientSecret="$MASTODON_CLIENT_SECRET" \
        MastodonAccessToken="$MASTODON_ACCESS_TOKEN" \
        AtpAuthHandle="$ATP_AUTH_HANDLE" AtpAuthPassword="$ATP_AUTH_PASSWORD" \
        SlackWebhookUrl="$SLOW_ZONE_BOT_SLACK_WEBHOOK_URL"
