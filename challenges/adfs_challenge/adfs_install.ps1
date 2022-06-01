Install-WindowsFeature -IncludeManagementTools -Name ADFS-Federation 
 
Import-Module ADFS 
  
$user  = "$env:USERDOMAIN\$env:USERNAME"
$password = ConvertTo-SecureString -String "TrendMicro123!" -AsPlainText -Force
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $user, $password
echo $credential
Install-AdfsFarm -CertificateThumbprint $certThumbprint -FederationServiceName $fqdn  -ServiceAccountCredential $credential