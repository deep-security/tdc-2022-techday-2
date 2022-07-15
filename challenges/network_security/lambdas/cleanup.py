import boto3
import os
import re
ssmc = boto3.client("ssm")
ec2c = boto3.client("ec2")
ec2r = boto3.resource("ec2")
cft = boto3.client("cloudformation")
lambdac = boto3.client("lambda")

def handler(event, context):
  igw = os.environ.get("IGWID")
  nat = os.environ.get("NATGW")
  igwrtb = os.environ.get("IGWRTB")
  pubrtb = os.environ.get("PublicRTB")
  privrtb = os.environ.get("PrivateRTB")
  deleteCft = os.environ.get("DELETE_ENDPOINT", "true").lower() == "true"
  clean(igwrtb)
  clean(pubrtb, [{"DestinationCidrBlock": "0.0.0.0/0", "GatewayId": igw}])
  clean(privrtb, [{"DestinationCidrBlock": "0.0.0.0/0", "NatGatewayId": nat}])
  if deleteCft:
    deleteCft()

def clean(rtbarn, desired=[]):
  rtb = ec2r.RouteTable(rtbarn)
  for r in rtb.routes:
    r.delete()
  for r in desired:
    rtb.create_route(r)

def deleteCft():
  cfts = cft.describe_stacks()
  for s in cfts["Stacks"]:
    if s["StackName"].startswith("TM-NS-Endpoint-"):
      cft.delete_stack(StackName=s["StackName"])
