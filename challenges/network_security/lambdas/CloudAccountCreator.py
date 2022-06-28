import boto3
import json
import traceback
import urllib3
import cfnresponse
import time

iamc = boto3.client('iam')
PNAME = "NetworkSecurityPolicy"


def handler(event, context):
  print("executed")
  print(str(event))
  print(str(context))
  print("")
  try:
    data = run(event.get("ResourceProperties", {}), event, context)
    print(data)
    cfnresponse.send(event, context, cfnresponse.SUCCESS, data, str(data.get("id", "-1")))
  except Exception as e:
    print("type error: " + str(e))
    print(traceback.format_exc())
    cfnresponse.send(event, context, cfnresponse.FAILED, {})
  return


def run(p, event, context):
  url = "network.{}.cloudone.trendmicro.com".format(p["env"])
  requests = urllib3.HTTPSConnectionPool(url, port=443)
  ApiHeaders = {
      'Authorization': 'ApiKey {}'.format(p['apiKey']),
      'api-version': 'v1',
  }
  e = getExistingConnector(p, url, requests, ApiHeaders)
  if e:
    if event["RequestType"] == "Delete" and str(e["id"]) == event.get("PhysicalResourceId", ""):
      r = requests.request('DELETE', '/api/awsconnectors/{}'.format(e["id"], headers=ApiHeaders))
    return e
  time.sleep(2)
  r = requests.request('POST', '/api/awsconnectors', headers={**ApiHeaders, **{'Content-Type': 'application/json'}}, body=json.dumps({"accountName": "TDC-{}".format(p["accountId"]), "crossAccountRole": p["roleArn"]}))
  if not r.status == 200:
    print(r.data)
    msg = "Failed to call createAccountUsingPOST from Cloud One Network Security ({} error)".format(r.status)
    print(msg)
    # This endpoint seems to be giving 400 error despite successfully creating?
    time.sleep(2)
    e = getExistingConnector(p, url, requests, ApiHeaders)
    if e:
      return e
    else:
      raise Exception(msg)
  return json.loads(r.data)


def getExistingConnector(p, url, requests, ApiHeaders):
  r = requests.request('GET', '/api/awsconnectors', headers=ApiHeaders)
  if not r.status == 200:
    raise Exception("Failed to call AWS-Connectors-API from Cloud One Network Security ({} error)".format(r.status))
  for role in json.loads(r.data).get("crossAccountRoles", []):
    if str(role.get("accountId")) == p["accountId"]:
      return role
  return None