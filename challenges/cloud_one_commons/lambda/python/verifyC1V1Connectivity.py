import json
import os
import boto3
import urllib3

serviceConnectionStatusDict = {
    "0": "RED",
    "1": "GREEN"
}

# Retrieve SSM Parameter value based on parameter key passed.
def getV1SsmParameter(ssmClient, paramKey):
    
    parameter = ssmClient.get_parameter(Name=paramKey, WithDecryption=True)

    return parameter ['Parameter']['Value']

# Enable Trend Remote Support status on the Vision One.
def enableTrendRemoteSupport(http, v1ApiBaseUrl, httpHeaders):

    body = {
        'enabled': True
    }

    r = http.request('PUT', v1ApiBaseUrl + "/remoteSupport", headers=httpHeaders, body=json.dumps(body))

    return json.loads(r.data)

# Retrieve Trend Remote Support status from Vision One.
def getTrendRemoteSupportStatus(http, v1ApiBaseUrl, httpHeaders):

    r = http.request('GET', v1ApiBaseUrl + "/remoteSupport", headers=httpHeaders)

    getTrendRemoteSupportStatusResponse = json.loads(r.data)

    if "data" in getTrendRemoteSupportStatusResponse:
        
        if getTrendRemoteSupportStatusResponse["code"] == "Success":
            
            return True

    return False

def listSupportedProducts(http, v1ApiBaseUrl, httpHeaders):

    r = http.request('GET', v1ApiBaseUrl + "/connectors", headers=httpHeaders)

    return json.loads(r.data)

def checkServiceConnectionStatus(http, v1ApiBaseUrl, httpHeaders, v1ConnectedProductList):
    
    serviceConnectionStatusResponse = listSupportedProducts(http, v1ApiBaseUrl, httpHeaders)
        
    if "data" in serviceConnectionStatusResponse:
    
        if serviceConnectionStatusResponse["code"] == "Success":

            for service in serviceConnectionStatusResponse["data"]:

                if service["productId"] in v1ConnectedProductList:

                    if not service["isConnected"]:

                        raise Exception('Error: Product "' + str(service["productId"]) + '" is not connected to the Vision One account')

                    else:
                        print("Service", str(service["productId"]), "is Connected and the status is", serviceConnectionStatusDict[str(service["status"])])

            return True

        else:
            raise Exception('Error: Vision One API endpoint errored out or is unavailable.')

    else:
        raise Exception('Error:', str(serviceConnectionStatusResponse["error"]["code"]))

def handler(event, context):
    
    # Read AWS Lambda Environment variables into the Lambda runtime as variables.
    awsRegion = str(os.environ.get("awsRegion"))
    v1AuthToken = str(os.environ.get("v1AuthToken"))
    v1ConnectedProductList = str(os.environ.get("v1ConnectedProductList"))
    v1ApiBaseUrlSSMKey = os.environ.get("v1ApiBaseUrlSSMKey")

    if v1ConnectedProductList[-1] == ",":
        v1ConnectedProductList = v1ConnectedProductList[:-1].replace(" ", "").split(",")
    else:
        v1ConnectedProductList = v1ConnectedProductList.replace(" ", "").split(",")

    # Creating an SSM Client to store values in the AWS SSM Parameter Store.
    ssmClient = boto3.client('ssm', region_name=awsRegion)

    # Get Vision One API Base URL from the AWS SSM Parameter Store.
    v1ApiBaseUrl = getV1SsmParameter(ssmClient, v1ApiBaseUrlSSMKey)

    http = urllib3.PoolManager()

    headers = {
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": "Bearer " + v1AuthToken
    }

    # Enable Trend Remote Support on the Vision One Console.
    print("enableTrendRemoteSupport - " + str(enableTrendRemoteSupport(http, v1ApiBaseUrl, headers)))

    # Verify Trend Remote Support status is enabled.
    print("getTrendRemoteSupportStatus - " + str(getTrendRemoteSupportStatus(http, v1ApiBaseUrl, headers)))

    # Run service connection status on the Vision One console to ensure services in the v1ConnectedProductList list is connected and the status is GREEN.
    checkServiceConnectionStatus(http, v1ApiBaseUrl, headers, v1ConnectedProductList)

    return True