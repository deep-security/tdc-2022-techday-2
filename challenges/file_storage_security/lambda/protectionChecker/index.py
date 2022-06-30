import boto3
import filecmp
import zipfile
import urllib.request


bucket = "${ImageUploaderS3Bucket}"
pwned_url = "https://${QSS3BucketName}.s3.${AWS::URLSuffix}/${ToolsPrefix}pwned.zip"
file_key = "connectioncheck"

s3 = boto3.client("s3")


class PayloadNotFoundError(Exception):
    def __init__(self, message="Payload not detected! Try again."):
        self.message = message
        super().__init__(self.message)


class PayloadNotBlockedError(Exception):
    def __init__(self, message="Payload was not blocked by FSS! Try again."):
        self.message = message
        super().__init__(self.message)


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


def payload_check():
    try:
        player_file = "/tmp/player_file"
        control_file = get_payload()
        s3.download_file(bucket, file_key, player_file)
        file_equality = filecmp.cmp(control_file, player_file)
        assert file_equality == True
    except:
        raise PayloadNotFoundError


def protection_check():
    try:
        player_file = "/tmp/player_file"
        control_file = get_payload()
        s3.download_file(bucket, file_key, player_file)
        file_equality = filecmp.cmp(control_file, player_file)
        assert file_equality == True
    except:
        raise PayloadNotFoundError


def handler(event, context):
    try:
        assert payload_check() == True
        assert protection_check() == True
    except PayloadNotFoundError as e:
        print(e)
        raise Exception("Payload not detected! Try again.")
    except PayloadNotBlockedError as e:
        print(e)
        raise Exception("Payload not detected! Try again.")
    except Exception as e:
        print(e)
        raise Exception(f"Exception: {e}")
