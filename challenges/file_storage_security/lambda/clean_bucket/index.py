import logging
import time
from typing import Literal, TypedDict

import boto3
import cfnresponse
from mypy_boto3_s3.service_resource import Bucket, BucketVersioning, S3ServiceResource


class CfnEvent(TypedDict):
    RequestType: str
    ResourceProperties: dict[str, str]


status = cfnresponse.SUCCESS
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handler(event: CfnEvent, context: None):
    logger.debug(event)
    if event["RequestType"] == "Delete":
        BUCKETNAME: str = event["ResourceProperties"]["BucketName"]
        s3: S3ServiceResource = boto3.resource("s3")  # pyright: ignore
        time.sleep(90)
        bucket: Bucket = s3.Bucket(BUCKETNAME)
        bucket_versioning: BucketVersioning = s3.BucketVersioning(BUCKETNAME)
        if bucket_versioning.status == "Enabled":
            bucket.object_versions.delete()
        else:
            bucket.objects.all().delete()
        cfnresponse.send(event, context, status, {}, None)  # pyright: ignore
    else:
        cfnresponse.send(event, context, status, {}, None)  # pyright: ignore
