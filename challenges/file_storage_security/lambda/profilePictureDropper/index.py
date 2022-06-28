import zipfile
import boto3
import json
import os
import logging
import cfnresponse
from botocore.config import Config


bucket = os.environ["BUCKET"]

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        raise
    return True


def handler(event, context):
    response_data = {}
    path = "/tmp/pics"

    try:
        if event["RequestType"] == "Create":
            with zipfile.ZipFile("./malicious-peeps.zip", "r") as zip_ref:
                zip_ref.extractall(path=path, pwd=b"novirus")

            files = [
                f"{path}/malicious-peeps/{f}"
                for f in os.listdir(f"{path}/malicious-peeps")
            ]
            response_data = {"files": files}

            # Upload the image
            for file in files:
                upload_file(file, bucket)
        status = cfnresponse.SUCCESS
    except Exception as e:
        logging.error(e)
        status = cfnresponse.FAILED
    finally:
        cfnresponse.send(event, context, status, response_data)
