import boto3

bucket = "${S3BucketResources.Outputs.ImageUploaderS3BucketName}"
file_key = "connectioncheck"
s3_client = boto3.client("s3")


def handler(event, context):
    result = s3_client.list_objects_v2(Bucket=bucket, Prefix=file_key)
    print(result)
    if "Contents" in result:
        print("You've hacked the service!")
        return True
    else:
        raise Exception("Payload not detected! Try again.")
