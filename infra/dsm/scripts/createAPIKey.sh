#!/bin/bash
#Set DSM URL from File on server
DSMURL=`cat /opt/DSMURL`
DSMPassword=`cat /opt/DSMPassword`
until curl -vk ${DSMURL}:443/rest/status/manager/current/ping; do echo \"manager not started yet\" >> /tmp/4-check-service;  sleep 30; done

##Get Session Cookie and RequestID via user/pass
curl -k -X POST ${DSMURL}/api/sessions -H 'Cache-Control: no-cache' -H 'Content-Type: application/json' -H 'api-version: v1' -c cookie.txt -d '{
"userName": "SuperUser",
"password": "'${DSMPassword}'"
}' | jq -r .RID > /opt/RID
###Set RID as variable
RID=`cat /opt/RID`
###Create API key with Cookie and RID
curl -k -X POST \
  ${DSMURL}/api/apikeys \
  -H 'Content-Type: application/json' \
  -H 'api-version: v1' \
  -H "rID: ${RID}" \
  -b cookie.txt \
  -d '{
  "keyName": "Challenge Key '${RANDOM}'",
  "description": "Created using a request ID",
  "roleID": 1
}' | jq -r .secretKey > /opt/APIKEY