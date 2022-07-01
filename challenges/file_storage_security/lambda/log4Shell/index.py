import boto3
import urllib.request

bucket = "${ImageUploaderS3Bucket}"
file_url = "https://secure.eicar.org/eicar.com.txt"
FILE_NAME = 'eicar.txt'

def handler(event, context):
    s3 = boto3.client('s3')
    path = '/tmp/'         # temp path in lambda.
    with open(path + FILE_NAME, "wb") as data:
        res = urllib.request.urlopen(
            urllib.request.Request(url=file_url, method="GET"), timeout=5
        )
        data.write(res.read())
    s3.upload_file('/tmp/eicar.txt', bucket, 'log4shell.txt')

    return {
            'status': 'True',
       'statusCode': 200,
       'body': 'Payload delivered'
      }

