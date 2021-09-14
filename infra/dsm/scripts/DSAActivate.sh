#!/bin/bash
#Get DSMURL and APIKEY from local files
DSMURL=`cat /opt/DSMURL`
APIKEY=`cat /opt/APIKEY`
#Get public ec2 hostname from ec2 metadata
HOSTNAME=`curl http://169.254.169.254/latest/meta-data/public-hostname`
#POLICYID=`cat /opt/policy | jq .ID`
POLICYNAME="Challenge--Policy"
#Get Policy ID from Policy Name
PolicyID=`curl -k -X POST ${DSMURL}/api/policies/search -H "Content-Type:application/json" -H "api-version:v1" -H "api-secret-key:${APIKEY}" -d "{ \"searchCriteria\": [{\"fieldName\": \"name\",\"stringTest\": \"equal\",\"stringValue\": \"${POLICYNAME}\" }] }" | jq -r .policies[0].ID`
#Get Deployment Script
curl -k -X POST ${DSMURL}/api/agentdeploymentscripts -H "Content-Type:application/json" -H "api-version:v1" -H "api-secret-key:${APIKEY}" -d '{
"platform": "linux",
"validateCertificateRequired": false,
"validateDigitalSignatureRequired": false,
"activationRequired": true,
"policyID": '$PolicyID',
"relayGroupID": 0,
"computerGroupID": 0
}' | jq -r .scriptBody >> /opt/Agent_Deployemnt_Script.sh
#Make Deployment Script Executable
chmod +x /opt/Agent_Deployemnt_Script.sh
#Run Deployment Script 
/opt/Agent_Deployemnt_Script.sh
