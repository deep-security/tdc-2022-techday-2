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

#add edge for user
md -Path $env:temp\edgeinstall -erroraction SilentlyContinue | Out-Null
$Download = join-path $env:temp\edgeinstall MicrosoftEdgeEnterpriseX64.msi
(new-object System.Net.WebClient).DownloadFile('https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/a2662b5b-97d0-4312-8946-598355851b3b/MicrosoftEdgeEnterpriseX64.msi',$Download)
Start-Process "$Download" -ArgumentList "/quiet"