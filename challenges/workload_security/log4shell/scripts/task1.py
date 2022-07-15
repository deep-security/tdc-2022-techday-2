import json, boto3, logging
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("event: {}".format(event))
    result_flag = False
    ssmc = boto3.client('ssm')
    hostName = os.getenv("HostName")
    # C1 parameter get from SSM Parameter store 
    api_key = ssmc.get_parameter(Name='/player/C1/c1ApiKey')["Parameter"]["Value"]
    region = ssmc.get_parameter(Name='/player/C1/c1Region')["Parameter"]["Value"]
    
    # Customize request parameters
    authorization = "ApiKey " + api_key
    BaseURL = "https://workload." + region + ".cloudone.trendmicro.com/api/computers"

    # API request to workload security
    headers = {'Content-Type': 'application/json', 'api-version': 'v1', 'Authorization': authorization}
    
    try:
        result = requests.get(BaseURL, headers=headers)
        dict_result = json.loads(result.text)
        
        # Check agent   
        for i in dict_result["computers"]:
            if hostName == i["hostName"]:
                if i["computerStatus"]["agentStatus"] == "active" and i["computerStatus"]['agentStatusMessages'][0] in ("Managed (Online)", "管理対象 (オンライン)"):
                    result_flag = True
                    break
        
        # Return task result
        if result_flag == False:
            raise Exception("Agent isn't installed or activated yet.")
            return result_flag
        
        return result_flag

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)