import http.client
import json
import re

#Pull in players C1WS Region and APIKey
C1WSRegion = open("c:\Projects\C1Region.txt")
Region = C1WSRegion.read()
C1WSRegion.close()
C1WSAPIKey = open("c:\Projects\C1WSAPIKey.txt")
AuthKey = C1WSAPIKey.read()
C1WSAPIKey.close()

#Connection parameters to connect to the players C1 Instance
conn = http.client.HTTPSConnection("workload.%s.cloudone.trendmicro.com")%Region
payload = json.dumps({
  "platform": "windows",
  "validateCertificateRequired": True,
  "validateDigitalSignatureRequired": True,
  "activationRequired": True
})
headers = {
  'api-version': 'v1',
  'Authorization': 'ApiKey {AuthKey}',
  'Content-Type': 'application/json',
}

#Connect to players C1 Instance
try:
  conn.request("POST", "/api/agentdeploymentscripts", payload, headers)
  res = conn.getresponse()
  data = res.read()
  deploymentscript = data.decode("utf-8")
except conn.exceptions.RequestException as e: # Reports any error other than HTTP error in the POST process
    raise SystemExit(e)
except res.exceptions.RequestException as e: # Reports any error other than HTTP error in the response process
    raise SystemExit(e)
except conn.exceptions.HTTPError as err: # Reports any HTTP connection errors in the POST process
    raise SystemExit(err)
except res.exceptions.HTTPError as err: # Reports any HTTP connection errors in the response process
    raise SystemExit(err)

#Parse the output to find the required ACTIVATIONURL, TENANTID, and TOKENID from the players environment deployment script
activation = re.findall(r"((dsm):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))", deploymentscript)[:1]
cnvtTupletoList1 = list(activation)
for i in cnvtTupletoList1:
  activationURL = i[0]
tenant = re.findall(r"tenantID:\b[0-9A-F]{8}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{12}\b", deploymentscript)[:1]
cnvtTupletoList2 = list(tenant)
for i in cnvtTupletoList2:
  tenantID = i[9:]
token = re.findall(r"token:\b[0-9A-F]{8}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{12}\b", deploymentscript)[:1]
cnvtTupletoList3 = list(token)
for i in cnvtTupletoList3:
  tokenID = i[6:]

#Write the outputs to local files for use in scripts.
C1WSActivationURLFile = open("c:\Projects\C1WSActivationURL.txt", "w")
C1WSActivationURLFile.write(activationURL)
C1WSActivationURLFile.close
C1WSTenantIDFile = open ("c:\Projects\C1WSTenantID.txt", "w")
C1WSTenantIDFile.write(tenantID)
C1WSTenantIDFile.close
C1WSTokenIDFile = open ("c:\Projects\C1WSTokenID.txt", "w")
C1WSTokenIDFile.write(tokenID)
C1WSTokenIDFile.close