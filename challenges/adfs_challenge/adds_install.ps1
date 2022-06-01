$domainName = "trendtechday.com"
$password = "TrendMicro123!"
$securePassword = ConvertTo-SecureString $password -AsPlainText -Force
 
Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
Install-ADDSForest -DomainName $domainName -SafeModeAdministratorPassword $securepassword -Force
