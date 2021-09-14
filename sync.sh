#!/bin/bash
# Check if number of arguments equals to 1 or 2
if [ "$#" -ne 1 ] && [ "$#" -ne 2 ]; then
    echo "You must enter 1 or 2 argument(s): BUCKET_NAME [AWS_PROFILE]"
    exit
fi

# Set profile.
if [ "$#" -ne 2 ]; then
  PROFILE="--profile ${2}"
else
  PROFILE="--profile ${AWS_PROFILE}"
fi

# Get Bucket
BUCKET_NAME=$1
Bucket_Location=$(aws s3api get-bucket-location --bucket ${BUCKET_NAME} ${PROFILE} --output text)
if [ $Bucket_Location != '' ] && [ $Bucket_Location != 'None' ]
then
  BUCKET_REGION=${Bucket_Location}
else
  BUCKET_REGION="us-east-1"
fi
echo 'Bucket Region is '${BUCKET_REGION}
echo ""

# Sync local folder with S3
echo 'Syncing to '${BUCKET_NAME}
echo ""
FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
aws s3 sync ${FOLDER} s3://${BUCKET_NAME} --exclude ".git/*" --acl public-read ${PROFILE}
echo 'Files synced!'
echo ''