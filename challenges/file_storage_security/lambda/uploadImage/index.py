import boto3
import json
import os
import logging
from botocore.config import Config

# Values passed in from cfn
bucket = "${ImageUploaderS3Bucket}"
region = "${AWS::Region}"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):

    logger.info("event: {}".format(event))

    try:
        key = event["pathParameters"]["name"]
        logger.info(key)
        ttl = 120

        s3_client = boto3.client(
            "s3",
            config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
            region_name=region,
        )

        signed_url = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=ttl,
        )

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps(signed_url),
        }
          
    except Exception as e:
        logger.info("Exception: {}".format(e))
        return {"statusCode": 404}
