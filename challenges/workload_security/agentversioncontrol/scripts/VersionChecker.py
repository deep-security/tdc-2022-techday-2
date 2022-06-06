import requests
import json
import subprocess
import re
import boto3

#Pull in players C1WS Region and APIKey
C1WSRegion = open("c:\Projects\C1Region.txt")
Region = C1WSRegion.read()
C1WSRegion.close()
C1WSAPIKey = open("c:\Projects\C1WSAPIKey.txt")
AuthKey = C1WSAPIKey.read()
C1WSAPIKey.close()

#Declare the path to the dsa_query executable, Agent Version Control information, and headers required for HTTP GET
#Agent Version Control Profile = 0 as we only support the Default Profile currently
#Agent Version Controls = 11 as this get the Windows 2016 64bit information. I hope to make this more "universal" later (check OS and OS version)
path = '"C:/Program Files/Trend Micro/Deep Security Agent/dsa_query.cmd"'
url = 'https://workload.%s.cloudone.trendmicro.com/api/agentversioncontrolprofiles/0/agentversioncontrols/11'%Region
headers = {"Authorization": f"ApiKey {AuthKey}", "api-version": "v1"}

#Request the Agent Version Control information from Cloud One
try:
    response_API = requests.get(url, headers=headers)
    response_API.raise_for_status()
except requests.exceptions.RequestException as e: # Reports any error other than HTTP error
    raise SystemExit(e)
except requests.exceptions.HTTPError as err: # Reports any HTTP connection errors
    raise SystemExit(err)

#Use the API to GET the Agent Version Controls for (Win 10/64-bit) from the Default Agent Version Control Profile information in C1WS
data = json.loads(response_API.text)

#Load the Available Versions section of the Default Agent Version Control Profile / Agent Version Controls (Win 10/64-bit) into a table
availableVersions = data['availableVersions']

#Put just the version information into a list
versions = list()
for item in availableVersions:
    versions.append(item['version'])

#Pull the N-2 Version number for comparison
n_minus_2_version = (versions[2])

#Get the Agent information from the local computer DSA through a command shell
output = subprocess.check_output(path +" -c GetPluginVersion", shell=True)

#Convert the output from bytes to a string
str_convert = output.decode('ascii')

#Load the results into a table to pull out just the DSA Agent Version number
result = {}
for row in str_convert.split('\n'):
    if ': ' in row:
        key, value = row.split(': ')
        result[key.strip(' .')] = value.strip()

#Replace dash with dot in version information
AgentVersion = re.sub("-", ".", result['PluginVersion.core'])

#Reset the UpgradeTask file to False, just in case... (***REMOVE AFTER DONE TESTING***)
cleanup = open("c:/Projects/UpgradeTask.txt", "w")
cleanup.write("False")
cleanup.close()

#RegEx to check installed version vs N-2 Version in C1WS and update the UpgradeTask.txt file if Correct
if re.match(n_minus_2_version, AgentVersion):
    with open("c:/Projects/UpgradeTask.txt", "w") as completed:
        completed.write("True")
        completed.close()
        #Read the S3 bucket information from the original Service Catalog installation script and upload the UpgradeTask.txt file
        # (***POSSIBLE SOME OF THIS ISN'T NEED, I DON'T PRETEND TO KNOW WHAT MAGIC THE CFT BUILDERS DO*** -- This was done for my testing)
        awsbucket = open("c:\Projects\Bucket.txt")
        s3bucket = awsbucket.read()
        awsobj = boto3.resource('s3')
        copy_source = "c:/Projects/UpgradeTask.txt"
        upload = awsobj.meta.client.upload_file(copy_source, s3bucket, "UpgradeTask.txt")
        awsbucket.close()