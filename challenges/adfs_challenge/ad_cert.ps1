$fqdn =(Get-WmiObject win32_computersystem).DNSHostName+"."+(Get-WmiObject win32_computersystem).Domain 
$password = ConvertTo-SecureString -String "TrendMicro123!" -Force -AsPlainText 
$filename = "C:\$fqdn.pfx"
 
$selfSignedCert = New-SelfSignedCertificate -certstorelocation cert:\localmachine\my -dnsname  $fqdn
$certThumbprint = $selfSignedCert.Thumbprint
Export-PfxCertificate -cert cert:\localMachine\my\$certThumbprint -Password $password -FilePath $filename
 
#optional - Adding cert to trusted root will help stop browser complaining about self signed cert being not from trusted certificate authority.Just for the record you should never do this setting in non dev environments.  
 
$pfx = new-object System.Security.Cryptography.X509Certificates.X509Certificate2  
$pfx.import($filename,$password,'Exportable,PersistKeySet')  
$store = new-object System.Security.Cryptography.X509Certificates.X509Store([System.Security.Cryptography.X509Certificates.StoreName]::Root,'localmachine') 
$store.open('MaxAllowed')  
$store.add($pfx)  
$store.close() 