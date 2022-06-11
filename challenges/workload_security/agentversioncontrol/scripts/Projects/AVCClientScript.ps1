Start-Transcript -path "c:\Projects\AVCClient.log" -append
choco install python --version=3.10.4 -y
choco install awscli -y
$env:ChocolateyInstall = Convert-Path "$((Get-Command choco).Path)\..\.."   
Import-Module "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
refreshenv
c:\Python310\python.exe -m pip install requests | Out-Host
c:\Python310\python.exe -m pip install boto3 | Out-Host
$activationURLPattern = [Regex]::new('((dsm):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))')
$tenantIDPattern = [Regex]::new('tenantID:\b[0-9A-F]{8}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{12}\b')
$tokenIDPattern = [Regex]::new('token:\b[0-9A-F]{8}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{4}\b-\b[0-9A-F]{12}\b')
$C1WSRegion = [IO.File]::ReadAllText("c:\Projects\C1Region.txt")
$C1WSAPIKey = [IO.File]::ReadAllText("c:\Projects\C1WSAPIKey.txt")
$URI = "https://workload.$C1WSRegion.cloudone.trendmicro.com/api/agentdeploymentscripts"
$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("api-version", "v1")
$headers.Add("Authorization", "ApiKey $C1WSAPIKey")
$headers.Add("Content-Type", "application/json")

$body = "{`n`"platform`": `"windows`",`n`"validateCertificateRequired`": true,`n`"validateDigitalSignatureRequired`": true,`n`"activationRequired`": true`n}"

$response = Invoke-RestMethod -URI $URI -Method 'POST' -Headers $headers -Body $body

$deploymentScript = $response.scriptBody

net user Administrator TrendMicro0! | Out-Host

$activationURL = $activationURLPattern.Matches($deploymentScript).Value[0]
Set-Content -Path 'C:\Projects\C1WSActivationURL.txt' -Value $activationURL -NoNewline
$tenantID = $tenantIDPattern.Matches($deploymentScript).Value[0].Trim("tenantID:")
Set-Content -Path 'C:\Projects\C1WSTenantID.txt' -Value $tenantID -NoNewline
$tokenID = $tokenIDPattern.Matches($deploymentScript).Value[0].Trim("token:")
Set-Content -Path 'C:\Projects\C1WSTokenID.txt' -Value $tokenID -NoNewline
$scriptList = @(
    'C:\Projects\C1WSInstaller.ps1'
    'C:\Projects\CreateSchTask.ps1'
)

foreach ($script in $scriptList) {
    & $script 
}
Start-ScheduledTask -TaskName "Version_Checker"
Stop-Transcript