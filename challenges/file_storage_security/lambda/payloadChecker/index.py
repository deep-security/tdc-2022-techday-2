import boto3
import time
import filecmp
import zipfile
import urllib.request


bucket = "${ImageUploaderS3Bucket}"
pwned_url = "https://${QSS3BucketName}.s3.${AWS::URLSuffix}/${ToolsPrefix}pwned.zip"
file_key = "connectioncheck"

s3 = boto3.client("s3")
ssm = boto3.client("ssm")


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


def check_container_filesystem():
    tries = 0
    while tries < 10:
        time.sleep(0.5)
        tries = tries + 1
        print(f"try number {tries}")
        response = ssm.send_command(
            Targets=[{"Key": "tag:Name", "Values": ["EKSBastion"]}],
            DocumentName="AWS-RunShellScript",
            Parameters={
                # the below returns an error exit code if file doesnt exist
                "commands": [
                    "sudo /usr/local/bin/kubectl exec -n fss-log4shell-attacker-env deployment/log4shell-deployment -- md5sum /srv/connectioncheck"
                ]
            },
        )
        print(f"response:{response}")
        command_id = response["Command"]["CommandId"]
        print(command_id)
        try:
            time.sleep(3)  # some delay always required...
            invocations_list = ssm.list_command_invocations(
                CommandId=command_id,
            )["CommandInvocations"]
            print(invocations_list)
            if invocations_list == []:
                continue
            instance_id = sorted(
                invocations_list, key=lambda d: d["RequestedDateTime"], reverse=True
            )[0]["InstanceId"]
            print(instance_id)
            result = ssm.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id,
            )
            print(result)
            if result["Status"] == "InProgress":
                continue
            else:
                if result["Status"] != "Success":
                    return False
                else:
                    output = result["StandardOutputContent"]
                    print(output)
                    return True
        except ssm.exceptions.InvocationDoesNotExist:
            continue


def handler(event, context):
    player_file = "/tmp/player_file"
    control_file = get_payload()
    try:
        executed_in_container = check_container_filesystem()
        print(executed_in_container)
        s3.download_file(bucket, file_key, player_file)
        file_equality = filecmp.cmp(control_file, player_file)
        print(file_equality)
        assert executed_in_container == True
        assert file_equality == True
    except Exception as e:
        print(e)
        raise Exception("Payload not detected! Try again.")
