import boto3
import filecmp
import zipfile
import urllib.request
from urllib.error import HTTPError


bucket = "${ImageUploaderS3Bucket}"
pwned_url = "https://${QSS3BucketName}.s3.${AWS::URLSuffix}/${ToolsPrefix}pwned.zip"
endpoint = "${SudoSinglesEndpoint}"
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


def scan_on_get_response():
    try:
        url = f"{endpoint}/{file_key}"
        res = urllib.request.urlopen(
            urllib.request.Request(url=f"{endpoint}/getimg/{file_key}", method="GET"),
            timeout=5,
        )
        data = {"code": res.code, "data": res.read()}
    except HTTPError as e:
        data = {"code": e.code, "reason": e.reason, "headers": e.headers.items()}
    finally:
        return data


def payload_check(control_file_path):
    try:
        player_file_path = "/tmp/player_file_path"
        s3.download_file(bucket, file_key, player_file_path)
        files_are_equal: bool = filecmp.cmp(control_file_path, player_file_path)
        assert files_are_equal
    except:
        raise PayloadNotFoundError
    else:
        return files_are_equal


def protection_check(control_file_path):
    try:
        data = scan_on_get_response()
        contents = data.get("data")
        with open(control_file_path, "rb") as control_file:
            file_is_clean: bool = contents not in control_file.read()
        assert file_is_clean
    except:
        raise PayloadNotBlockedError
    else:
        return file_is_clean


def handler(event, context):
    control_file_path = get_payload()
    return payload_check(control_file_path) and protection_check(control_file_path)
