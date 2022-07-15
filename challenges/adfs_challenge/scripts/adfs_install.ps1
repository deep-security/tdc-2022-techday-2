[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$SafeModeAdministratorPassword,

    [Parameter(Mandatory=$true)]
    [string]$DomainNetBiosName,

    [Parameter(Mandatory=$true)]
    [string]$TechDayAdminUser,

    [Parameter(Mandatory=$true)]
    [string]$DomainDNSName,

    [Parameter(Mandatory=$true)]
    [string]$SSMUserName

)
#create cert for ADFS
$password = ConvertTo-SecureString -String $SafeModeAdministratorPassword -Force -AsPlainText 
$filename = "C:\$DomainDNSName.pfx"
 
$selfSignedCert = New-SelfSignedCertificate -certstorelocation cert:\localmachine\my -dnsname  $DomainDNSName
$certThumbprint = $selfSignedCert.Thumbprint
Export-PfxCertificate -cert cert:\localMachine\my\$certThumbprint -Password $password -FilePath $filename
 

$pfx = new-object System.Security.Cryptography.X509Certificates.X509Certificate2  
$pfx.import($filename,$password,'Exportable,PersistKeySet')  
$store = new-object System.Security.Cryptography.X509Certificates.X509Store([System.Security.Cryptography.X509Certificates.StoreName]::Root,'localmachine') 
$store.open('MaxAllowed')  
$store.add($pfx)  
$store.close()
#install adfs with cert
Install-WindowsFeature -IncludeManagementTools -Name ADFS-Federation 
 
Import-Module ADFS 
$adminConfig=(C:\s3-downloads\scripts\adfs_dkm.ps1 -ServiceAccount $DomainNetBiosName\adsvctd -AdfsAdministratorAccount $DomainNetBiosName\localadmin) 
$user  = "$DomainNetBiosName\$TechDayAdminUser"
$password = ConvertTo-SecureString -String $SafeModeAdministratorPassword -AsPlainText -Force
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $user, $password

Install-AdfsFarm -CertificateThumbprint $certThumbprint -FederationServiceName $DomainDNSName  -ServiceAccountCredential $credential -AdminConfiguration $adminConfig

#enable idp signon page
Set-AdfsProperties -EnableIdpInitiatedSignonPage $true

#add edge for user
md -Path $env:temp\edgeinstall -erroraction SilentlyContinue | Out-Null
$Download = join-path $env:temp\edgeinstall MicrosoftEdgeEnterpriseX64.msi
(new-object System.Net.WebClient).DownloadFile('https://msedge.sf.dl.delivery.mp.microsoft.com/filestreamingservice/files/a2662b5b-97d0-4312-8946-598355851b3b/MicrosoftEdgeEnterpriseX64.msi',$Download)
Start-Process "$Download" -ArgumentList "/quiet"

#Run add_user_domain before reboot
C:\s3-downloads\scripts\add_user_domain.ps1 -TechDayAdminUser $TechDayAdminUser -DomainDNSName $DomainDNSName -SSMUserName $SSMUserName

#reboot after ADFS install
Start-Sleep -Seconds 10
Restart-Computer -Force