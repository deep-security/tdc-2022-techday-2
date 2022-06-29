import boto3
import json
import os
import urllib
import logging
from botocore.config import Config

# Values passed in from cfn
bucket = "${QSS3BucketName}"
image_bucket = "${S3BucketResources.Outputs.ImageUploaderS3BucketName}"
true_prefix = "${LambdaPrefix}payloadLoader/true.js"
false_prefix = "${LambdaPrefix}payloadLoader/false.js"
region = "${AWS::Region}"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")


def handler(event, context):
    true_file = "/tmp/true.js"
    s3.download_file(bucket, true_prefix, true_file)
    with open(true_file, "rb") as true_file:
        data: str = true_file.read().decode("utf-8")
        data = "const exploit = '/profile/getimg/connectioncheck'\n" + data
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "content-type": "application/javascript",
        },
        "body": data,
    }
