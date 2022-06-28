import boto3
import base64
import json
import os
import logging
from botocore.config import Config

# Values passed in from cfn
bucket = "${S3BucketResources.Outputs.ImageUploaderS3BucketName}"
region = "${AWS::Region}"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client(
    "s3",
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    region_name=region,
)

def handler(event, context):

    logger.info("event: {}".format(event))

    try:
        key = event["pathParameters"]["id"]
        logger.info(key)
        
        s3_client.download_file(bucket, key, f'/tmp/{key}')
        
        file = open(f'/tmp/{key}', 'rb')
        image_b64 = base64.b64encode(file.read()).decode('utf-8')
        file.close()
        logger.info(image_b64)

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps(image_b64),
        }
          
    except Exception as e:
        logger.info("Exception: {}".format(e))
        return {"statusCode": 404}
