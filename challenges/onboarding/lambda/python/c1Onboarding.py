import json
import os
from datetime import datetime
import boto3
import urllib3
import logging
import cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

c1TrendRegion = None
c1AccountId = None

# Returns Cloud One Accounts API Global Endpoint URL.
def c1AccountsApiEndpointBaseUrl():
    
    return "https://accounts.cloudone.trendmicro.com/api"

# Returns Cloud One region-based Services API Endpoint URL.
def c1ServicesApiEndpointBaseUrl(c1TrendRegion):
    
    return "https://services." + str(c1TrendRegion) + ".cloudone.trendmicro.com/api"

# Retrieve API Key ID from the raw API Key passed to this function.
def parseApiKeyForKeyId(rawApiKey):

    return rawApiKey.split(':')[0]

# Validates the Cloud One API Key passed to this function by checking enabled status in DescribeApiKey response, returns Cloud One Trend Region and Cloud One Account ID.
def c1DescribeApiKey(http, httpHeaders, apiKeyId):

    c1DescribeApiKeyResponse = json.loads(http.request('GET', c1AccountsApiEndpointBaseUrl() + "/apikeys/" + apiKeyId, headers=httpHeaders).data)

    if "enabled" in c1DescribeApiKeyResponse:

        if c1DescribeApiKeyResponse["enabled"] and "urn" in c1DescribeApiKeyResponse:

            return c1DescribeApiKeyResponse["urn"].split(":")[3], c1DescribeApiKeyResponse["urn"].split(":")[4]

        else:
            raise Exception('Error: Invalid/inactive API Key')
    else:
        raise Exception('Error: Invalid response')

# Returns True if Cloud One licenses are valid for the duration of the event.
def c1CheckServicesStatus(http, httpHeaders, c1TrendRegion, c1LicenseValidationDayCount):

    c1CheckServicesStatusResponse = json.loads(http.request('GET', c1ServicesApiEndpointBaseUrl(c1TrendRegion) + "/services", headers=httpHeaders).data)

    for service in c1CheckServicesStatusResponse["services"]:

        # Check if licenses are expired.
        if "expired" in service:
            
            if service["expired"]:

                raise Exception('Expired license for ' + service["name"] + ". Unable to proceed with this license.")

            else:
                print("License for", service["name"], "- Valid")

        # Check if the licenses are expiring during the duration of the TDC.
        elif "expires" in service:
        
            if (datetime.strptime(service["expires"], '%Y-%m-%dT%H:%M:%SZ') - datetime.now()).days <= c1LicenseValidationDayCount:

                raise Exception('License expiry imminent for ' + service["name"] + ". Unable to proceed with this license status.")

            else:
                print("License for", service["name"], "- Valid")
        
        else:
            print("License for", service["name"], "- Valid")

    return True

# Invites player to the Cloud One account via email, assigns a Cloud One Role based on the params passed to this function.
def c1InvitePlayer(http, httpHeaders, emailId, c1Role):

    httpBody = {
        "email": str(emailId),
        "roleID": str(c1Role)
    }

    c1InvitePlayerResponse = json.loads(http.request('POST', c1AccountsApiEndpointBaseUrl() + "/invitations", headers=httpHeaders, body=json.dumps(httpBody)).data)

    if "message" in c1InvitePlayerResponse:        

        for field in c1InvitePlayerResponse["fields"]:

            print(str(c1InvitePlayerResponse["message"]), str(c1InvitePlayerResponse["fields"][field]).capitalize(), "-", str(emailId))
    
    elif "state" in c1InvitePlayerResponse:

        if "invited" in c1InvitePlayerResponse["state"]:

            print("Invitation sent to " + str(emailId) + " with \"" + str(c1Role) + "\" role. Invitation ID - " + str(c1InvitePlayerResponse["id"]) + ".")

            return True

        else:
            raise Exception('Error: Invitation unsuccessful.')

# Verify Users exist in the Cloud One account
def c1VerifyUsers(http, httpHeaders, c1UsersList):

    c1UsersResponse = json.loads(http.request('GET', c1AccountsApiEndpointBaseUrl() + "/users", headers=httpHeaders).data)

    c1UsersDict = {}
    
    for user in c1UsersResponse["users"]:

        c1UsersDict.update({user["email"]: user["state"]})

    for user in c1UsersList:

        if user not in c1UsersDict.keys():

            raise Exception('Error: User "' + str(user) + '" not found in the Cloud One Account')

        elif "enabled" not in c1UsersDict[user]:

            raise Exception('Error: User "' + str(user) + '" is disabled in the Cloud One Account')

    return True

# Retrieve SSM Parameter value based on parameter key passed.
def getC1SsmParameter(ssmClient, paramKey):
    
    parameter = ssmClient.get_parameter(Name='/player/C1/' + paramKey, WithDecryption=True)

    return parameter ['Parameter']['Value']

# Store SSM Parameter key and value on the AWS backend for future use.
def setC1SsmParameter(ssmClient, paramKey, paramValue):
    
    parameter = ssmClient.put_parameter(Name='/player/C1/' + paramKey, Value=paramValue, Type='String', Overwrite=True)

    print(str(parameter))

def main(event, context):

    # Setup
    logger.info("event: {}".format(event))
    status = cfnresponse.SUCCESS
    responseData = {}
    responseData['Data'] = {}
    try:
        if event['RequestType'] == 'Create':

            # Read AWS Lambda Environment variables into the Lambda runtime as variables.
            awsRegion = str(os.environ.get("awsRegion"))
            c1ApiKey = str(os.environ.get("c1ApiKey"))
            c1UsersList = str(os.environ.get("c1UsersList"))
            c1LicenseValidationDayCount = int(os.environ.get("c1LicenseValidationDayCount"))

            if c1UsersList[-1] == ",":
                c1UsersList = c1UsersList[:-1].replace(" ", "").split(",")
            else:
                c1UsersList = c1UsersList.replace(" ", "").split(",")

            http = urllib3.PoolManager()

            # HTTP Headers for Cloud One API calls.
            headers = {
                "Content-Type": "application/json;charset=utf-8",
                "Authorization": "ApiKey " + c1ApiKey,
                "Api-Version": "v1"
            }

            # Retrieve Cloud One Region information and Account ID based on the API Key ID passed to this function.
            c1TrendRegion, c1AccountId = c1DescribeApiKey(http, headers, parseApiKeyForKeyId(c1ApiKey))

            # Creating an SSM Client to store values in the AWS SSM Parameter Store.
            ssmClient = boto3.client('ssm', region_name=awsRegion)

            # If Account ID and Trend region are none, raise exception, else go ahead.
            if not c1AccountId and not c1TrendRegion:

                raise Exception('Error: Invalid Cloud One Account ID or Region. Please contact organizer.')

            # If valid Account Id and Trend region, store those values in AWS SSM Parameter Store for future use.
            else:

                print("Cloud One Account Id - " + str(c1AccountId))

                # Stores global Trend C1 Account ID as an SSM Parameter  "c1AccountId".
                setC1SsmParameter(ssmClient, "c1AccountId", c1AccountId)

                # Stores global Trend C1 API Key as an SSM Parameter  "c1ApiKey".
                setC1SsmParameter(ssmClient, "c1ApiKey", c1ApiKey)

                print("Trend Region - " + str(c1TrendRegion))

                # Stores Trend hosted Cloud One Region Identifier.
                setC1SsmParameter(ssmClient, "c1Region", c1TrendRegion)

                # Stores global Trend C1 Accounts API Base URL as an SSM Parameter  "c1AccountsApiBaseUrl".
                setC1SsmParameter(ssmClient, "c1AccountsApiBaseUrl", c1AccountsApiEndpointBaseUrl())

                # Stores region specific Trend C1 Services API Base URL as an SSM Parameter  "c1ServicesApiBaseUrl".
                setC1SsmParameter(ssmClient, "c1ServicesApiBaseUrl", c1ServicesApiEndpointBaseUrl(c1TrendRegion))

                # Check if all Cloud One services are licensed for the duration of the TDC.
                if c1CheckServicesStatus(http, headers, c1TrendRegion, c1LicenseValidationDayCount):

                    print("All Services are Go!!!")

                    # Verify if all users exist in the Cloud One account, raises exception if any one user fails.
                    if c1VerifyUsers(http, headers, c1UsersList):
                        
                        print("Success: User(s) exist in the Cloud One account")

                        # Stores onboarding success as an SSM Parameter "c1Onboarding" for Mission Control verification.
                        setC1SsmParameter(ssmClient, "c1OnboardingStatus", "Success")
    except Exception as e:
        logger.info("Exception: {}".format(e))
        status = cfnresponse.FAILED
    
    cfnresponse.send(event, context, status, responseData, None)