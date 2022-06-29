#!/bin/bash

# exit when any command fails
set -e

# Check if number of arguments equals 3 or 4
if [ "$#" -ne 3 ]; then
    echo "You must enter 3 or 4 command line arguments: BUCKET_NAME STACK_NAME AWS_PROFILE"
    exit
fi

# Check if AWS CLI is installed.
if ! command -v aws &> /dev/null
then
    echo "AWS CLI could not be found. Install it here: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html"
    exit
fi

# Check if JQ is installed.
if ! command -v jq &> /dev/null
then
    echo "JQ could not be found."
    exit
fi

# Get Bucket
BUCKET_NAME=$1
AWS_PROFILE=$3
Bucket_Location=$(aws s3api get-bucket-location --bucket ${BUCKET_NAME} --profile ${AWS_PROFILE} --output text)
if [ $Bucket_Location != '' ] && [ $Bucket_Location != 'None' ]
then
  BUCKET_REGION=${Bucket_Location}
else
  BUCKET_REGION="us-east-1"
fi
echo 'Bucket Region is '${BUCKET_REGION}
echo ""

# Sync local folder with S3
FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo 'Syncing local files to S3 bucket...'
aws s3 sync ${FOLDER} s3://${BUCKET_NAME} --exclude ".git/*" --acl public-read --profile ${AWS_PROFILE} --delete
echo 'Files synced!'
echo ''

# Create CloudFormation Stack
STACK_NAME=$2
BUCKET_URL="https://"${BUCKET_NAME}".s3."${BUCKET_REGION}".amazonaws.com"
TEMPLATE_URL=""${BUCKET_URL}"/templates/main.template.yaml"
PARAMETER1="value1"
PARAMETER2="value2"
echo 'Deploying Stack...'
# You should add more parameters as needed under the --parameters flag, like:
# ParameterKey=PARAMETER1,ParameterValue=${PARAMETER1} \
# ParameterKey=PARAMETER2,ParameterValue=${PARAMETER2} \
# ParameterKey=BuildEks,ParameterValue="false" \
aws cloudformation create-stack --stack-name ${STACK_NAME} \
    --template-url ${TEMPLATE_URL} \
    --parameters ParameterKey=QSS3BucketName,ParameterValue=${BUCKET_NAME} \
                 ParameterKey=QSS3KeyPrefix,ParameterValue="" \
    --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND \
    --profile ${AWS_PROFILE}

echo 'Stack deployed!'