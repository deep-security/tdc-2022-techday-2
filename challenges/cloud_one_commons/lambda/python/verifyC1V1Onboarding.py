import os
import boto3

ssmParametersList = []
ssmParameterValue = None

# Retrieve SSM Parameter value based on parameter key passed.
def getSsmParameter(ssmClient, paramKey):
    
    parameter = ssmClient.get_parameter(Name=paramKey, WithDecryption=True)

    return parameter ['Parameter']['Value']

def handler(event, context):

    # Read AWS Lambda Environment variables into the Lambda runtime as variables.
    awsRegion = str(os.environ.get("awsRegion"))    
    ssmParametersList = str(os.environ.get("ssmParametersList"))
    ssmParameterValue = str(os.environ.get("ssmParameterValue"))

    if ssmParametersList[-1] == ",":
        ssmParametersList = ssmParametersList[:-1].replace(" ", "").split(",")
    else:
        ssmParametersList = ssmParametersList.replace(" ", "").split(",")

    # Creating an SSM Client to store values in the AWS SSM Parameter Store.
    ssmClient = boto3.client('ssm', region_name=awsRegion)

    # If SSM Parameters List is empty and the expected ssmParameterValue is not defined.
    if not len(ssmParametersList) and not ssmParameterValue:

        raise Exception('Error: Input Invalid with SSM Parameter List and the expected SSM Parameter Value')
    
    else:

        for ssmParameterKey in ssmParametersList:

            if ssmParameterValue not in getSsmParameter(ssmClient, ssmParameterKey):

                raise Exception('Error: Onboarding task incomplete or failed')

        return True

