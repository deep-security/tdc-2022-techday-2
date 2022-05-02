# Fromhttps://raw.githubusercontent.com/trendmicro/cloudone-filestorage-plugins/master/post-scan-actions/aws-python-conformity-custom-check/handler.py
# Tweaks made for static type checking
import json
import logging
import os
import re
import urllib.parse
from typing import List, TypedDict

import boto3
import urllib3


# import datetime

logger: logging.Logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

http = urllib3.PoolManager()

region = os.environ.get("CC_REGION", "us-west-2")
ccsecretsarn = os.environ["CC_API_SECRETS_ARN"]
customcheckid = os.environ.get("CC_CUSTOMCHECKID", "CUSTOM-001").upper()
customchecksev = os.environ.get("CC_CHECKSEV", "VERY_HIGH").upper()

secrets = boto3.client("secretsmanager").get_secret_value(  # pyright: ignore
    SecretId=ccsecretsarn
)
secrets_data = json.loads(secrets["SecretString"])
apikey = secrets_data["ccapikey"]

headers = {
    "Content-Type": "application/vnd.api+json",
    "Authorization": "ApiKey " + apikey,
}


def get_cc_accountid(awsaccountid: str):
    accountsapi = f"https://{region}-api.cloudconformity.com/v1/accounts"
    r = http.request(method="GET", url=accountsapi, headers=headers)  # pyright: ignore
    accounts = json.loads(r.data.decode("utf-8"))["data"]  # pyright: ignore
    for account in accounts:
        try:
            if account["attributes"]["awsaccount-id"] == awsaccountid:
                return account["id"]
        except:
            pass


class Record(TypedDict):
    Sns: dict[str, str]
    EventSubscriptionArn: str


class Event(TypedDict):
    Records: List[Record]


def lambda_handler(event: Event, context: None):

    for record in event["Records"]:

        # Message details from SNS event
        message = json.loads(record["Sns"]["Message"])
        logger.debug(message)
        findings = message["scanning_result"].get("Findings")

        if findings:
            # Get AWS Account Info
            arn = json.dumps(record["EventSubscriptionArn"])
            aws_region = arn.split(":")[3].strip()
            account_id = arn.split(":")[4].strip()
            # Get Conformity Account ID for AWS Account
            ccaccountid = get_cc_accountid(account_id)

            # Get the bucket & object details
            s3_domain_pattern = "s3(\\..+)?\\.amazonaws.com"
            url = urllib.parse.urlparse(message["file_url"])
            # check pre-signed URL type, path or virtual
            if re.fullmatch(s3_domain_pattern, url.netloc):
                bucketname = url.path.split("/")[1]
                s3_object = "/".join(url.path.split("/")[2:])
            else:
                bucketname = url.netloc.split(".")[0]
                s3_object = url.path[1:]
            object_key = urllib.parse.unquote_plus(s3_object)
            object_keyshort = object_key.split("/")[-1]
            s3uri = f"s3://{bucketname}/{object_key}"
            s3arn = f"arn:aws:s3:::{bucketname}/{object_key}"
            s3consoleurl = f"https://s3.console.aws.amazon.com/s3/buckets/{bucketname}?region={aws_region}&prefix={object_key}"

            # Generate TTL to expire message (not currently supported by conformity custom checks api - coming soon?)
            # timenow = datetime.datetime.now()
            # ttl = timenow + datetime.timedelta(days=1)
            # ttlepoch = round(datetime.datetime.timestamp(ttl))

            malwares: list[str] = []
            types: list[str] = []
            for finding in message["scanning_result"]["Findings"]:
                malwares.append(finding.get("malware"))
                types.append(finding.get("type"))

                checksdata = {
                    "data": [
                        {
                            "type": "checks",
                            "attributes": {
                                "rule-title": "C1 File Storage Security - Malware Detected",
                                "message": f"Object {object_keyshort} in bucket {bucketname} contains malware",
                                "not-scored": False,
                                "region": aws_region,
                                "resource": s3uri.replace("/", ":"),
                                "risk-level": customchecksev,
                                "status": "FAILURE",
                                "service": "S3",
                                "categories": ["security"],
                                "link": s3consoleurl,
                                # "ttl": ttlepoch,
                                "extradata": [
                                    {
                                        "label": "Malware Name",
                                        "name": "Malware Name",
                                        "type": "Meta",
                                        "value": ", ".join(malwares),
                                    },
                                    {
                                        "label": "Malware Type",
                                        "name": "Malware Type",
                                        "type": "Meta",
                                        "value": ", ".join(types),
                                    },
                                    {
                                        "label": "S3 URI",
                                        "name": "S3 URI",
                                        "type": "Meta",
                                        "value": s3uri,
                                    },
                                    {
                                        "label": "S3 ARN",
                                        "name": "S3 ARN",
                                        "type": "Meta",
                                        "value": s3arn,
                                    },
                                    {
                                        "label": "S3 Console URL",
                                        "name": "S3 Console URL",
                                        "type": "Meta",
                                        "value": s3consoleurl,
                                    },
                                ],
                            },
                            "relationships": {
                                "account": {
                                    "data": {"id": ccaccountid, "type": "accounts"}
                                },
                                "rule": {
                                    "data": {"id": customcheckid, "type": "rules"}
                                },
                            },
                        }
                    ]
                }

                bodyencoded = json.dumps(checksdata).encode("utf-8")
                checksapi = f"https://{region}-api.cloudconformity.com/v1/checks"

                r = http.request(  # pyright: ignore
                    "POST", checksapi, body=bodyencoded, headers=headers
                )
                print(r.data.decode("utf-8"))  # pyright: ignore
