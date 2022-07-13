import boto3
import cfnresponse
import json
from urllib3 import PoolManager


# Retrieve SSM Parameter value based on parameter key passed.
def getC1SsmParameter(ssmClient, paramKey):
    parameter = ssmClient.get_parameter(
        Name="/player/C1/" + paramKey, WithDecryption=True
    )
    return parameter["Parameter"]["Value"]


# Store SSM Parameter key and value on the AWS backend for future use.
def setFSSSsmParameter(ssmClient, paramKey, paramValue):
    parameter = ssmClient.put_parameter(
        Name="/player/FSS/" + paramKey, Value=paramValue, Type="String", Overwrite=True
    )
    print(str(parameter))


ssm_client = boto3.client("ssm", region_name="${AWS::Region}")


def handler(event, context):
    region = getC1SsmParameter(ssm_client, "c1Region")
    api_key = getC1SsmParameter(ssm_client, "c1ApiKey")

    url = f"https://filestorage.{region}.cloudone.trendmicro.com/api/external-id"

    # Init ...
    the_event = event["RequestType"]
    print("The event is: ", str(the_event))
    response_data = {}

    try:
        if the_event in ("Create", "Update"):
            print("Preparing API request env...")
            http = PoolManager()
            headers = {
                "Content-Type": "application/json;charset=utf-8",
                "Authorization": f"ApiKey {api_key}",
                "Api-Version": "v1",
            }

            print("Getting FSS external ID...")
            get_external_id_response = json.loads(
                http.request(
                    "GET",
                    url=url,
                    headers=headers,
                ).data
            )
            external_id: str = get_external_id_response.get("externalID")

            print("Adding external ID to SSM...")
            setFSSSsmParameter(ssm_client, "ExternalID", external_id)

        # Everything OK... send the signal back
        print("Operation successful!")
        cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
    except Exception as e:
        print("Operation failed...")
        print(str(e))
        response_data["Data"] = str(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, response_data)
