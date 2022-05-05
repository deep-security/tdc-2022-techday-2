#!/usr/bin/env bash
# exit when any command fails
set -e

# define constants
DEPLOYWORKFLOWNAME="build-dev-environment.yaml" # Change if needed

# Check if JQ is installed.
if ! command -v jq &> /dev/null
then
    echo "JQ could not be found. Install it here: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html"
    exit
fi

# Check if GitHub CLI is installed. And user is logged in.
if ! command -v gh &> /dev/null
then
    echo "Github CLI could not be found. Install it here: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html"
    exit
fi
echo "Checking Github authentication status..."
gh auth status #returns exit code 1 if user not logged in
echo ""

# Set variables
LATESTUPSTREAMHASH=$(git rev-parse '@{u}')
CURRENTBRANCHNAME=$(git rev-parse --abbrev-ref HEAD)

# Get user confirmation and start workflow
read -p "Are you sure? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    gh workflow run "$DEPLOYWORKFLOWNAME" \
        --ref "$CURRENTBRANCHNAME" \
        -f name="$(git rev-parse '@{u}')"
fi

# Define the Vending Machine deploy action
function watch-action {
    gh run watch --exit-status # will exit with error code 1 if run fails

    # Once run is complete, get the job ID
    echo "Getting job ID"
    RUNJSON=$(gh run list --workflow="$DEPLOYWORKFLOWNAME" \
        --branch "$CURRENTBRANCHNAME" \
        --json headSha,databaseId \
        -q ".[] | select(.headSha == \"$LATESTUPSTREAMHASH\")")
    RUNID=$(echo "$RUNJSON" | jq '.databaseId')
    JOBID=$(gh run view "$RUNID" | grep "gh run view" | awk '{print $11}' | tail -c 11)

    # Get the json from the logs of the vending job
    echo "Credentials are:"
    gh run view --log --job "$JOBID" | awk 'BEGIN { first = 7; last = 100 }{ for (i = first; i < last; i++) { printf("%s ", $i) } print $last }' | grep -A11 -B1 "PlayerUserName" | jq
}

# Handle the watch options
while true; do
  case "$1" in
    -w | --watch ) sleep 3 && watch-action; exit ;;
    * ) exit ;;
  esac
done
