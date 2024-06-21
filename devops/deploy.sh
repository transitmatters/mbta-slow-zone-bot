#!/bin/bash -x

if [[ -z "$DD_API_KEY" ]]; then
    echo "Must provide DD_API_KEY in environment" 1>&2
    exit 1
fi

if [[ -z "$ACCESS_KEY" || -z "$ACCESS_SECRET" || -z "$CONSUMER_KEY" || -z "$CONSUMER_SECRET" ]]; then
    echo "Must provide ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY and CONSUMER_SECRET in environment" 1>&2
    exit 1
fi

if [[ -z "$MASTODON_CLIENT_KEY" || -z "$MASTODON_CLIENT_SECRET" || -z "$MASTODON_ACCESS_TOKEN" ]]; then
    echo "Must provide MASTODON_CLIENT_KEY, MASTODON_CLIENT_SECRET and MASTODON_ACCESS_TOKEN in environment" 1>&2
    exit 1
fi

STACK_NAME=mbta-slowzone-bot
BUCKET=mbta-slowzone-bot

# Identify the version and commit of the current deploy
GIT_VERSION=`git describe --tags --always`
GIT_SHA=`git rev-parse HEAD`
echo "Deploying version $GIT_VERSION | $GIT_SHA"

# Adding some datadog tags to get better data
DD_TAGS="git.commit.sha:$GIT_SHA,git.repository_url:github.com/transitmatters/mbta-slow-zone-bot"
DD_GIT_REPOSITORY_URL="github.com/transitmatters/mbta-slow-zone-bot"
DD_GIT_COMMIT_SHA="$GIT_SHA"

poetry export -f requirements.txt --output mbta-slowzone-bot/requirements.txt --without-hashes

pushd mbta-slowzone-bot/

poetry run chalice package --stage prod --merge-template .chalice/resources.json cfn/

# Shrink the deployment package for the lambda layer https://stackoverflow.com/a/69355796
echo "Shrinking the deployment package for the lambda layer"

source ../devops/helpers.sh
shrink

# Check package size before deploying
maximumsize=79100000
actualsize=$(wc -c <"cfn/layer-deployment.zip")
if [ $actualsize -ge $maximumsize ]; then
    echo ""
    echo "layer-deployment.zip is over $maximumsize bytes. Shrink the package further to be able to deploy"
    exit 1
fi

aws s3 cp stations.json s3://$BUCKET
aws cloudformation package --template-file cfn/sam.json --s3-bucket $BUCKET --output-template-file cfn/packaged.yaml
aws cloudformation deploy --template-file cfn/packaged.yaml --stack-name $STACK_NAME \
    --capabilities CAPABILITY_NAMED_IAM --no-fail-on-empty-changeset \
    --parameter-overrides DDApiKey=$DD_API_KEY GitVersion=$GIT_VERSION DDTags=$DD_TAGS \
        TwitterAccessKey=$ACCESS_KEY TwitterAccessSecret=$ACCESS_SECRET \
        TwitterConsumerKey=$CONSUMER_KEY TwitterConsumerSecret=$CONSUMER_SECRET \
        MastodonClientKey=$MASTODON_CLIENT_KEY \
        MastodonClientSecret=$MASTODON_CLIENT_SECRET \
        MastodonAccessToken=$MASTODON_ACCESS_TOKEN \ 
        SlackWebhookUrl=$SLOW_ZONE_BOT_SLACK_WEBHOOK_URL
