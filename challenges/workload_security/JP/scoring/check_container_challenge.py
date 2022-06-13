import json
import boto3
#Print when loading function
print('Loading function')
def lambda_handler(event, context):
    s3 = boto3.client("s3", region_name='us-east-1')
    correct_answer_container = "1005402 - Identified Suspicious User Agent In HTTP Request"
    print(event)
    keyword = event[0]["Reason"]
    print(keyword)
    if keyword == correct_answer_container:
        response = s3.put_object(
        Bucket='', #need to change env variable
        Key="container_correct",  
         )
    else:
        print("do it again")
