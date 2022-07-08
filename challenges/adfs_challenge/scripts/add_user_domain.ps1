[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$TechDayAdminUser,

    [Parameter(Mandatory=$true)]
    [string]$DomainDNSName
)

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

sleep 30

#add user to domain admins
Add-ADGroupMember -Identity "Domain Admins" -Members $TechDayAdminUser
Add-ADGroupMember -Identity "Enterprise Admins" -Members $TechDayAdminUser

#set user email address
$email = "$TechDayAdminUser@"
Set-AdUser -Identity $TechDayAdminUser -EmailAddress $email$DomainDNSName

#add edge for user
md -Path $env:temp\edgeinstall -erroraction SilentlyContinue | Out-Null
$Download = join-path $env:temp\edgeinstall MicrosoftEdgeEnterpriseX64.msi
(new-object System.Net.WebClient).DownloadFile('https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/a2662b5b-97d0-4312-8946-598355851b3b/MicrosoftEdgeEnterpriseX64.msi',$Download)
Start-Process "$Download" -ArgumentList "/quiet"