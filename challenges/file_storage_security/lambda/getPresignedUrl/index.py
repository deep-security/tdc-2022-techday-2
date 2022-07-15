import base64
import boto3
import urllib.request
import json
import os
import logging
from botocore.config import Config

# This is where we grab the profile images.
# Edit between the quotes if you have to change the destination ↓
bucket = "${S3BucketResources.Outputs.ImageUploaderS3BucketName}"




######## DO NOT EDIT BELOW THIS LINE ########
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

        signed_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=500,
        )
        logger.info(signed_url)

        try:
            FILE = "/tmp/asdf"
            res = urllib.request.urlopen(
                urllib.request.Request(url=signed_url, method="GET"), timeout=5
            )
            raw_file = open(FILE, "wb")
            raw_file.write(res.read())
            raw_file.close()

            with open(FILE, "rb") as image_file:
                eicar_bytes = image_file.read(68)
                image_file.seek(69)
                image_bytes = image_file.read()

            if (
                eicar_bytes
                == b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
            ):
                with open(FILE, "wb") as clean_file:
                    clean_file.write(image_bytes)

            with open(FILE, "rb") as final_file:
                data = base64.b64encode(final_file.read())
                code = data.decode("utf-8")

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "body": code,
                "isBase64Encoded": True,
            }
        except Exception as e:
            logger.info("Exception: {}".format(e))
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "isBase64Encoded": True,
                "body": "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",
            }

    except Exception as e:
        logger.info("Exception: {}".format(e))
        return {
            "statusCode": 404,
        }
