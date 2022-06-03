import boto3
import json
import os
import logging
from botocore.config import Config

# Get bucket name
bucket = "BUCKET_NAME"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info("event: {}".format(event))

    try:
            region = os.environ["AWS_REGION"]
            key = event['pathParameters']['id']
            logger.info(key)
            ttl = 5 * 24 * 60 * 60 # days * hours per day * minutes per hour * seconds per hour

            s3_client = boto3.client(
                's3',
                config = Config(
                    signature_version='s3v4',
                    s3 = {'addressing_style': 'path'}
                ),
                region_name = region
            )

            signed_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket,
                    'Key': key
                },
                ExpiresIn=ttl,
            )

            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(signed_url),
            }


    except Exception as e:
        logger.info("Exception: {}".format(e))
        return {
            'statusCode': 404
        }
