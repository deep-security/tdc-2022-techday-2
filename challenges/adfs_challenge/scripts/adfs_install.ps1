[CmdletBinding()]
param (
    [Parameter(Mandatory=$true)]
    [string]$SafeModeAdministratorPassword,

    [Parameter(Mandatory=$true)]
    [string]$DomainNetBiosName,

    [Parameter(Mandatory=$true)]
    [string]$TechDayAdminUser
)
#create cert for ADFS
$fqdn = "techday.com"
$password = ConvertTo-SecureString -String $SafeModeAdministratorPassword -Force -AsPlainText 
$filename = "C:\$fqdn.pfx"
 
$selfSignedCert = New-SelfSignedCertificate -certstorelocation cert:\localmachine\my -dnsname  $fqdn
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
  
$user  = "$DomainNetBiosName\$TechDayAdminUser"
$password = ConvertTo-SecureString -String $SafeModeAdministratorPassword -AsPlainText -Force
$credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $user, $password

Install-AdfsFarm -CertificateThumbprint $certThumbprint -FederationServiceName $fqdn  -ServiceAccountCredential $credential