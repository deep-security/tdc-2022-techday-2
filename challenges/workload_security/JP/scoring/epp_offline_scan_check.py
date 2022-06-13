import requests as rq
import json as js
import boto3

print('Loading function')

def get_ssm_params(*keys, region='us-east-1'):
    result = {}
    ssm = boto3.client('ssm', region)
    response = ssm.get_parameters(
        Names=keys,
        WithDecryption=True,
    )
    for p in response['Parameters']:
        result[p['Name']] = p['Value']
    return result

def lambda_handler(event, context):
    parameter = get_ssm_params("/player/C1/c1ApiKey")
    URL_search_policy = "https://workload.trend-us-1.cloudone.trendmicro.com/api/policies"
    key = parameter["/player/C1/c1ApiKey"]
    APIkey = "Apikey " + key
    header = {
    "Content-Type": "application/json",
    "Authorization" : APIkey,
    "api-version": "v1",
    }

    r = rq.get(URL_search_policy, headers=header)
    search_policy = js.loads(r.text)
    for policy in search_policy["policies"]:
        if policy["policySettings"]["antiMalwareSettingOfflineScheduledScanEnabled"]["value"] == "true":
            answer = policy["name"]
            answer == "usethispolicy"
            print(answer)
            return True
        else:
            return False
