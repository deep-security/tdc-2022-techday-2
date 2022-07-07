[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$TechDayAdminUser,

    [Parameter(Mandatory=$true)]
    [string]$SafeModeAdministratorPassword,

    [Parameter(Mandatory=$true)]
    [string]$SSMUserName
)

$user = New-LocalUser -AccountNeverExpires:$true -Password ( ConvertTo-SecureString -AsPlainText -Force $SafeModeAdministratorPassword) -Name $TechDayAdminUser -FullName $TechDayAdminUser -Description "Local Administrator"
 Add-LocalGroupMember -Group administrators -Member $user
 Add-LocalGroupMember -Group "Remote Desktop Users"  -Member $user