import requests
import logging
from zipfile import ZipFile
import subprocess
import shlex
from pathlib import Path
import json
from time import sleep

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
message = ''
code = ''
retries = 10

SUCCESS = "SUCCESS"
FAILED = "FAILED"


def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=''):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = reason if reason else 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    print("Response body:\n" + json_responseBody)

    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }

    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))


def run_command(command):
    code = 0
    try:
        logger.debug("executing command: %s" % command)
        output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT).decode("utf-8")
        logging.debug(output)
    except subprocess.CalledProcessError as exc:
        code = exc.returncode
        output = exc.output.decode("utf-8")
        logger.error("Command failed [exit %s]: %s" % (exc.returncode, exc.output.decode("utf-8")))
    return code, output


with ZipFile("./awscli-exe-linux-x86_64.zip") as zip:
    zip.extractall('/tmp/cli-install/')
run_command('chmod +x /tmp/cli-install/aws/dist/aws')
run_command('chmod +x /tmp/cli-install/aws/install')
c, r = run_command('/tmp/cli-install/aws/install -b /tmp/bin -i /tmp/aws-cli')
if c != 0:
    raise Exception(f"Failed to install cli. Code: {c} Message: {r}")


def execute_cli(properties):
    code, response = run_command(f"/tmp/bin/aws {properties['AwsCliCommand']} --output json")
    if code != 0 and ('NotFound' in response or 'does not exist' in response):
        return None
    if code != 0:
        raise Exception(response)
    return json.loads(response)


def handler(event, context):
    logger.debug(event)
    status = SUCCESS
    pid = 'None'
    resp = {}
    reason = ''
    try:
        if event['RequestType'] != 'Delete':
            while not Path("/tmp/bin/aws").is_file():
                print("waiting for cli install to complete")
                sleep(10)
            resp = execute_cli(event['ResourceProperties'])
            if 'IdField' in event['ResourceProperties'] and isinstance(resp, dict):
                pid = resp[event['ResourceProperties']['IdField']]
            else:
                pid = str(resp)
    except Exception:
        logging.error('Unhandled exception', exc_info=True)
        reason = (str(e))
        status = FAILED
    finally:
        send(event, context, status, resp, pid, reason=reason)
