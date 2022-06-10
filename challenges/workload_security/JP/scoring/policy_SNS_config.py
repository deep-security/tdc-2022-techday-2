import boto3
import requests as rq
import json as js

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
    parameter = get_ssm_params("/player/c1/c1apikey/summer")
    URL_policy = "https://workload.trend-us-1.cloudone.trendmicro.com/api/policies"
    URL_sns = "https://workload.trend-us-1.cloudone.trendmicro.com/api/systemsettings"
    key = parameter["/player/c1/c1apikey/summer"]  //need to reconfigure here
    APIkey = "Apikey " + key     
    policyname = "thisisfromryoma"    //renaming
    #SNS keys
    SNS_access_key = ""   //adding accessing key
    SNS_secret_key = ""   //asdding scr key
    SNS_Topic_ARN = ""    //adding ARN

    header = {
        "Content-Type": "application/json",
        "Authorization" : APIkey,
        "api-version": "v1"
    }    

    json_data_policy = {
    "parentID": 0,
    "name": policyname,   
    "policySettings": { 
    "intrusionPreventionSettingVirtualAndContainerNetworkScanEnabled": {"value": "false"}, 
    "intrusionPreventionSettingInspectTlsTrafficEnabled": {"value": "false"}
    }
    }
    
    json_data_sns = {
    "platformSettingEventForwardingSnsEnabled": {"value": "true"},
    'platformSettingEventForwardingSnsAdvancedConfigEnabled': {'value': 'true'},
    'platformSettingEventForwardingSnsConfigJson': {'value': '{\r\n  "Version": "2014-09-24",\r\n  "Statement": [\r\n    {\r\n      "Topic": "arn:aws:sns:us-east-1:333053306512:ryoma_SNS",\r\n      "Condition": {\r\n        "StringEquals" : {\r\n          "EventType" : ["SystemEvent", "AntiMalwareEvent", "WebReputationEvent", "DeviceControlEvent", "AppControlEvent", "IntegrityEvent", "LogInspectionEvent", "PacketLog", "PayloadLog"]\r\n        }\r\n      }\r\n    }\r\n  ]\r\n}'},
    "platformSettingEventForwardingSnsTopicArn": {"value": SNS_Topic_ARN},
    "platformSettingEventForwardingSnsSecretKey": {"value": SNS_secret_key},
    "platformSettingEventForwardingSnsAccessKey": {"value": SNS_access_key }
    }
    
    response = rq.post(URL_policy,headers=header, data=js.dumps(json_data_policy))
    
    print(response.status_code) 
    status_code = response.status_code
    if status_code == 200:
        print("Policy Configured")
    else:
        print("Policy error")
    
    response = rq.post(URL_sns,headers=header, data=js.dumps(json_data_sns))
    
    print(response.status_code) 
    status_code = response.status_code
    if status_code == 200:
        print("SNS Configured")
    else:
        print("SNS error")
