[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$SafeModeAdministratorPassword,

    [Parameter(Mandatory=$true)]
    [string]$DomainNetBiosName,

    [Parameter(Mandatory=$true)]
    [string]$TechDayAdminUser
)
Install-WindowsFeature -IncludeManagementTools -Name ADFS-Federation 
 
Import-Module ADFS 
  
$user  = "$DomainNetBiosName\$TechDayAdminUser"
$password = ConvertTo-SecureString -String $SafeModeAdministratorPassword -AsPlainText -Force
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $user, $password

Install-AdfsFarm -CertificateThumbprint $certThumbprint -FederationServiceName $fqdn  -ServiceAccountCredential $credential