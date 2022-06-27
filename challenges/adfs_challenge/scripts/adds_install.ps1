[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$SafeModeAdministratorPassword,

    [Parameter(Mandatory=$true)]
    [string]$DomainDNSName
)

$securePassword = ConvertTo-SecureString $SafeModeAdministratorPassword -AsPlainText -Force
 
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
Install-ADDSForest -DomainName $DomainDNSName -SafeModeAdministratorPassword $securepassword -Force
