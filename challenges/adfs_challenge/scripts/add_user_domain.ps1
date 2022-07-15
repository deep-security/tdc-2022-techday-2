[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$TechDayAdminUser,

    [Parameter(Mandatory=$true)]
    [string]$DomainDNSName,

    [Parameter(Mandatory=$true)]
    [string]$SSMUserName
)

sleep 60

$ServiceName = 'adws'
$arrService = Get-Service -Name $ServiceName

while ($arrService.Status -ne 'Running')
{

    Start-Service $ServiceName
    write-host $arrService.status
    write-host 'Service starting'
    Start-Sleep -seconds 60
    $arrService.Refresh()
    if ($arrService.Status -eq 'Running')
    {
        Write-Host 'Service is now Running'
    }

}

sleep 10

#add player user to domain admins
Add-ADGroupMember -Identity "Domain Admins" -Members $TechDayAdminUser
Add-ADGroupMember -Identity "Enterprise Admins" -Members $TechDayAdminUser

#create ssm-user
$ssmuser = New-LocalUser -AccountNeverExpires:$true -Password ( ConvertTo-SecureString -AsPlainText -Force $SafeModeAdministratorPassword) -Name $SSMUserName -FullName $SSMUserName -Description "ssm-user"
 Add-LocalGroupMember -Group administrators -Member $ssmuser

#add ssm-user to domain admins
Add-ADGroupMember -Identity "Domain Admins" -Members $SSMUserName
Add-ADGroupMember -Identity "Enterprise Admins" -Members $SSMUserName

#set user email address
$email = "$TechDayAdminUser@"
Set-AdUser -Identity $TechDayAdminUser -EmailAddress $email$DomainDNSName