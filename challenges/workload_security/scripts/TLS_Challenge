import json
import boto3
#Print when loading function
print('Loading function')
def lambda_handler(event, context):
    s3 = boto3.client("s3")
    tls_answer =  //TLS’s answer
    print(event)
    keyword = event[0]["Reason"]
    print(keyword)
    if keyword == tls_answer:
        response = s3.put_object(
        Bucket='', #need to change env variable
        Key="tls_correct",  
         )
    else:
        print("do it again")
