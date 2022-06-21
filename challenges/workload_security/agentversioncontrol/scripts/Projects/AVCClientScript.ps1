#This script runs on the Client machine AFTER Instance is initialized.
Start-Transcript -path "c:\Projects\AVCClient.log" -append
#Install python 3.10.4 using chocolatey and output progress/errors
choco install python --version=3.10.4 -y | Out-Host
#Install AWS Client tools and output progress/errors
choco install awscli -y | Out-Host
#Reset the Powershell environment to ensure further commands are understood.
$env:ChocolateyInstall = Convert-Path "$((Get-Command choco).Path)\..\.."
Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
refreshenv
#Install the python requests module using pip and output progress/errors
c:\Python310\python.exe -m pip install requests | Out-Host
#Install the python boto3 module using pip and output progress/errors
c:\Python310\python.exe -m pip install boto3 | Out-Host
#Set veriables for further script useage (Players environment C1WS Activation URL, C1WS Tenant ID, C1WS Token ID, C1 Region, and C1 API Key
$activationURLPattern = [Regex]::new('((dsm):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))')
$tenantIDPattern = [Regex]::new('tenantID:\b[0-9A-F]{8}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{12}\b')
$tokenIDPattern = [Regex]::new('token:\b[0-9A-F]{8}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{12}\b')
$C1WSRegion = [IO.File]::ReadAllText("c:\Projects\C1Region.txt")
$C1WSAPIKey = [IO.File]::ReadAllText("c:\Projects\C1WSAPIKey.txt")
#Set the URI to retrieve the Players C1WS Deployment Script
$URI = "https://workload.$C1WSRegion.cloudone.trendmicro.com/api/agentdeploymentscripts"
#Set the Headers to retrieve the Players C1WS Deployment Script
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("api-version", "v1")
$headers.Add("Authorization", "ApiKey $C1WSAPIKey")
$headers.Add("Content-Type", "application/json")
#Set the Payload to retrieve the Players C1WS Deployment Script
$body = "{`n`"platform`": `"windows`",`n`"validateCertificateRequired`": true,`n`"validateDigitalSignatureRequired`": true,`n`"activationRequired`": true`n}"
#Retrieve the C1WS Agent Deployment Script from the Players environment
$response = Invoke-RestMethod -URI $URI -Method 'POST' -Headers $headers -Body $body
#Store **JUST** the deployment script text
$deploymentScript = $response.scriptBody
#Reset the AWS autogenerated instance password to a known one for use with setting up the Scheduled Task (I "COULD" use the autogenerated password and can switch it at a later time)
net user Administrator TrendMicro0! | Out-Host
#Store the C1WS Agent Activation URL as a variable
$activationURL = $activationURLPattern.Matches($deploymentScript).Value[0]
Set-Content -Path 'C:\Projects\C1WSActivationURL.txt' -Value $activationURL -NoNewline
#Store the C1WS Agent Tenant ID as a variable
$tenantID = $tenantIDPattern.Matches($deploymentScript).Value[0].Trim("tenantID:")
Set-Content -Path 'C:\Projects\C1WSTenantID.txt' -Value $tenantID -NoNewline
#Store the C1WS Agent Token as a variable
$tokenID = $tokenIDPattern.Matches($deploymentScript).Value[0].Trim("token:")
Set-Content -Path 'C:\Projects\C1WSTokenID.txt' -Value $tokenID -NoNewline
#Set the scripts that need to run using all the above information
$scriptList = @(
    'C:\Projects\C1WSInstaller.ps1' #Installs the C1WS Agent with an older agent version, tying it into the players environment
    'C:\Projects\CreateSchTask.ps1' #Installs the Windows scheduled task to check the installed C1WS agent version, retrieve the current N-2 C1WS agent and compare. If same, challenge is complete
)
#Continue to run the other scripts necessary for the challenge
foreach ($script in $scriptList) {
    & $script 
}
#Start the Scheduled Task created with the CreateSchTask script
Start-ScheduledTask -TaskName "Version_Checker"
Stop-Transcript