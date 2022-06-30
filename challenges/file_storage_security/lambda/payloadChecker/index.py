import boto3
import filecmp
import zipfile
import urllib.request


bucket = "${ImageUploaderS3Bucket}"
pwned_url = "https://${QSS3BucketName}.s3.${AWS::URLSuffix}/${ToolsPrefix}pwned.zip"
file_key = "connectioncheck"

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
    player_file = "/tmp/player_file"
    control_file = get_payload()
    try:
        s3.download_file(bucket, file_key, player_file)
        file_equality = filecmp.cmp(control_file, player_file)
        print(file_equality)
        assert file_equality == True
    except Exception as e:
        print(e)
        raise Exception("Payload not detected! Try again.")
