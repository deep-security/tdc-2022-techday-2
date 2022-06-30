import subprocess
import os
import boto3
import time
import re

ssmc = boto3.client("ssm")
ec2c = boto3.client("ec2")
ec2r = boto3.resource("ec2")
lambdac = boto3.client("lambda")

def sendReq(server, timeout=2):
    return curl("curl --connect-timeout {} {}".format(timeout, server).split(' '))

def sendAttack(server, timeout=2):
    return curl("curl --connect-timeout {} -H 'User-Agent: sdvntyer' {}/api/v88".format(timeout, server).split(' '))
    # return curl("curl --connect-timeout {} {}".format(timeout, server).split(' '))  
def curl(cmd):
    # Returns True if was able to connect to server
    # AWS Lambda Functions block all ICMP packets, need to use curl instead.
    try:
        output = subprocess.run(cmd, stderr=subprocess.PIPE, check=False).stderr.decode().strip()
        errcode = re.search(".*curl: \((\d+)\).*", output)
        print("server: {} / errcode: {}".format(server, errcode.group(1) if errcode else errcode))
        if errcode is None:  # No error code means we were able to connect
            return True
        else:
            return errcode.group(1) != "28"  # errcode 28 means connection timeout, which means Network Security blocked it, or lambda has no internet access
    except Exception as e:
        print(e)
        return None

def handler(event, context):
    msg = ""
    victim = os.environ.get("VICTIM")
    # req = sendReq(victim)
    req = sendReq('http://www.google.com')
    attack = sendAttack(victim)
    if req is True and attack is False:
        msg = "You've successfully blocked the vulnerability!"
        return True
    else:
        msg = "Unfortunately attacks are still occurring against your servers! Make sure you check your configuration and perhaps re-read the instructions, and try again."
        print(req)
        print(attack)
        raise Exception("Incomplete")
    return msg