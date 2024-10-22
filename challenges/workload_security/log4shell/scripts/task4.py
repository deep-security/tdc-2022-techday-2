import json, boto3, logging
import os
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("event: {}".format(event))
    result_flag = False
    ips_rule_id = "1008610" # IPS rule that need to be assigned.
    lookup_key = "ruleIDs" # To Ensure that IPS is active and got some IPS rules assigned already.
    ssmc = boto3.client('ssm')
    hostName = os.getenv("HostName")
    # C1 parameter get from SSM Parameter store 
    api_key = ssmc.get_parameter(Name='/player/C1/c1ApiKey')["Parameter"]["Value"]
    region = ssmc.get_parameter(Name='/player/C1/c1Region')["Parameter"]["Value"]
    
    # Customize request parameters
    authorization = "ApiKey " + api_key
    BaseURL = "https://workload." + region + ".cloudone.trendmicro.com/api/computers/"

    # API request to workload security
    headers = {'Content-Type': 'application/json', 'api-version': 'v1', 'Authorization': authorization}
    
    try:
        result = requests.get(BaseURL, headers=headers)
        dict_result = json.loads(result.text)
        
        # Get Computer ID   
        for i in dict_result["computers"]:
            if hostName == i["hostName"] and lookup_key in i["intrusionPrevention"]:
                    ComputerID = i["ID"]
                    try:
                        IPSURL = BaseURL + str(ComputerID) +"/intrusionprevention/rules/"
                        result = requests.get(IPSURL, headers=headers)
                        dict_result = json.loads(result.text)
                        for i in dict_result["intrusionPreventionRules"]:
                            if i["identifier"] == ips_rule_id:
                                if i["detectOnly"] == False:
                                    result_flag = True
                                    break
                        break
                        
                    except requests.exceptions.RequestException as e:
                        raise SystemExit(e)

        # Return task result
        if result_flag == False:
            raise Exception("IPS rule 1008610 isn't assigned yet or still in Detect Mode.")
            return result_flag
        
        return result_flag
        
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)