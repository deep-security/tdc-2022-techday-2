[CmdletBinding()]
param (

    [Parameter(Mandatory=$true)]
    [string]$SafeModeAdministratorPassword
)

$fqdn =(Get-WmiObject win32_computersystem).DNSHostName+"."+(Get-WmiObject win32_computersystem).Domain 
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