import json
import os
import boto3
import urllib3
import urllib.parse
import logging
import cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Contains a list of Vision One supported regions.
v1SupportedRegions = ["United States", "Europe", "Singapore", "Japan", "Australia", "India"]

# Contains a dictionary of Vision One supported regions and their region-based API Endpoint Base URLs with Region Names as dictionary keys.
v1ApiEndpointBaseUrls = {
    "Australia": "api.au.xdr.trendmicro.com",
    "Europe": "api.eu.xdr.trendmicro.com",
    "India": "api.in.xdr.trendmicro.com",
    "Japan": "api.xdr.trendmicro.co.jp",
    "Singapore": "api.sg.xdr.trendmicro.com",
    "United States": "api.xdr.trendmicro.com"
}

# Returns the Vision One region-based API Endpoint Base URL.
def v1ApiEndpointBaseUrl(v1TrendRegion):

    return "https://" + v1ApiEndpointBaseUrls[v1TrendRegion] + "/beta/xdr/portal"

# Validates the Vision One Auth token passed to this function by listing roles in the Vision One account, returns True if success, otherwise False.
def v1VerifyAuthToken(ssmClient, http, httpHeaders, v1TrendRegion):

    r = http.request('GET', v1ApiEndpointBaseUrl(v1TrendRegion) + "/accounts/roles", headers=httpHeaders)

    v1ListAccountsResponse = json.loads(r.data)
    
    responseHeadersList = r.getheaders()

    if responseHeadersList:
        
        if "TMV1-Customer-ID" in responseHeadersList.keys():

            # Stores global Trend V1 Customer ID as an SSM Parameter  "v1CustomerId", from HTTP Response headers.
            setV1SsmParameter(ssmClient, "v1CustomerId", responseHeadersList["TMV1-Customer-ID"])
            
    if "code" in v1ListAccountsResponse:

        if v1ListAccountsResponse["code"] == "Success":

            return True
    
    # In case it doesn't return True above.
    raise Exception('Error: Invalid/inactive API Key')

# Invites player to the Vision One account via email, assigns a Vision One Role based on the params passed to this function.
def v1InvitePlayer(http, httpHeaders, v1TrendRegion, emailId, v1Role):

    # HTTP Body for the Player Invitation to the Vision One account.
    httpBody = {
        "type": 0,
        "name": str(emailId),
        "enabled": True,
        "description": "Account created by API for Tech Day.",
        "token": "",
        "authorization": 3,
        "role": str(v1Role)
    }

    v1InvitePlayerResponse = json.loads(http.request('POST', v1ApiEndpointBaseUrl(v1TrendRegion) + "/accounts/" + urllib.parse.quote_plus(str(emailId)) , headers=httpHeaders, body=json.dumps(httpBody)).data)

    if "error" in v1InvitePlayerResponse:

        print("Error Code: " + str(v1InvitePlayerResponse["error"]["code"]), "Message: ",  str(v1InvitePlayerResponse["error"]["message"]), "-", str(emailId))
    
    elif "code" in v1InvitePlayerResponse:

        if "Success" in v1InvitePlayerResponse["code"]:

            print("Invitation sent to " + str(emailId) + " with role as " + str(v1Role) + ".")

            return True

        else:
            raise Exception('Error: Invitation unsuccessful.')

# Verify User Accounts exist in the Vision One account.
def v1VerifyUserAccounts(http, httpHeaders, v1TrendRegion, v1UsersList):

    v1UserAccountsResponse = json.loads(http.request('GET', v1ApiEndpointBaseUrl(v1TrendRegion)  + "/accounts", headers=httpHeaders).data)
    
    v1UserAccountsDict = {}
    
    for userAccount in v1UserAccountsResponse["data"]["items"]:

        v1UserAccountsDict.update({userAccount["email"]: userAccount["enabled"]})

    for user in v1UsersList:

        if user not in v1UserAccountsDict.keys():

            raise Exception('Error: User account "' + str(user) + '" not found in the Vision One Account')

        elif not v1UserAccountsDict[user]:

            raise Exception('Error: User account "' + str(user) + '" is disabled in the Vision One Account')

        else:
            print("Success: User '" + str(user) + "' exists in the Vision One account")            

    return True

# Retrieve SSM Parameter value based on parameter key passed.
def getV1SsmParameter(ssmClient, paramKey):
    
    parameter = ssmClient.get_parameter(Name='/player/V1/' + paramKey, WithDecryption=True)

    return parameter ['Parameter']['Value']

# Store SSM Parameter key and value on the AWS backend for future use.
def setV1SsmParameter(ssmClient, paramKey, paramValue):
    
    parameter = ssmClient.put_parameter(Name='/player/V1/' + paramKey, Value=paramValue, Type='String', Overwrite=True)

    print(str(parameter))

def handler(event, context):

    # Setup
    logger.info("event: {}".format(event))
    status = cfnresponse.SUCCESS
    responseData = {}
    responseData['Data'] = {}

    try:
        if event['RequestType'] == 'Create':
            # Read AWS Lambda Environment variables into the Lambda runtime as variables.
            awsRegion = str(os.environ.get("awsRegion"))
            v1TrendRegion = str(os.environ.get("v1TrendRegion"))    
            v1AuthToken = str(os.environ.get("v1AuthToken"))
            v1UsersList = str(os.environ.get("v1UsersList"))

            if v1UsersList[-1] == ",":
                v1UsersList = v1UsersList[:-1].replace(" ", "").split(",")
            else:
                v1UsersList = v1UsersList.replace(" ", "").split(",")

            http = urllib3.PoolManager()

            # HTTP Headers for Vision One API calls.
            headers = {
                "Content-Type": "application/json;charset=utf-8",
                "Authorization": "Bearer " + v1AuthToken
            }

            # If v1TrendRegion is not in the supported regions list, raise exception, else go ahead and verify V1 Auth Token.
            if v1TrendRegion not in v1SupportedRegions:

                raise Exception('Error: Invalid Vision One Region')

            else:

                # Creating an SSM Client to store values in the AWS SSM Parameter Store.
                ssmClient = boto3.client('ssm', region_name=awsRegion)

                # If v1VerifyAuthToken returns True for Vision One API call, store API Key in AWS SSM Parameter Store for future use.
                if v1VerifyAuthToken(ssmClient, http, headers, v1TrendRegion):

                    print("Trend Region - " + str(v1TrendRegion))

                    print("Vision One APIs are a Go!!!")

                    # Stores global Trend V1 API Base URL as an SSM Parameter  "v1ApiBaseUrl".
                    setV1SsmParameter(ssmClient, "v1ApiBaseUrl", v1ApiEndpointBaseUrl(v1TrendRegion))

                    # Stores global Trend V1 API Key as an SSM Parameter  "v1ApiKey".
                    setV1SsmParameter(ssmClient, "v1ApiKey", v1AuthToken)

                    # Verify if all users exist in the Vision One account, raises exception if any one user fails.
                    if v1VerifyUserAccounts(http, headers, v1TrendRegion, v1UsersList):
                        
                        print("Success: User(s) exist in the Vision One account")

                        # Stores onboarding success as an SSM Parameter "v1Onboarding" for Mission Control verification.
                        setV1SsmParameter(ssmClient, "v1OnboardingStatus", "Success")           
    except Exception as e:
        logger.info("Exception: {}".format(e))
        status = cfnresponse.FAILED
    
    cfnresponse.send(event, context, status, responseData, None)