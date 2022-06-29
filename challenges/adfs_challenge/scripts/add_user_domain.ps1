[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$TechDayAdminUser
)

#add user to domain admins
Add-ADGroupMember -Identity "Domain Admins" -Members $TechDayAdminUser
Add-ADGroupMember -Identity "Enterprise Admins" -Members $TechDayAdminUser

#add edge for user
md -Path $env:temp\edgeinstall -erroraction SilentlyContinue | Out-Null
$Download = join-path $env:temp\edgeinstall MicrosoftEdgeEnterpriseX64.msi
(new-object System.Net.WebClient).DownloadFile('https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/a2662b5b-97d0-4312-8946-598355851b3b/MicrosoftEdgeEnterpriseX64.msi',$Download)
Start-Process "$Download" -ArgumentList "/quiet"

#enable idp signon page
Set-AdfsProperties -EnableIdpInitiatedSignonPage $true