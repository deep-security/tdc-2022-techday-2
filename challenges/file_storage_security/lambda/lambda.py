import boto3
import requests
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = 'conformity-testjp'
    path_test = '/tmp/'         # temp path in lambda.
    FILE_NAME = 'eicar.txt'
    file_url = "https://secure.eicar.org/eicar.com.txt"
    response=requests.get(file_url, stream=True)
    with open(path_test + FILE_NAME, 'wb') as data:
        for chunk in response.iter_content(chunk_size = 16*1024):
            data.write(chunk)
        print(data)
    s3.upload_file('/tmp/eicar.txt', bucket, 'test.txt')

    return {
            'status': 'True',
       'statusCode': 200,
       'body': 'Payload delivered'
      }