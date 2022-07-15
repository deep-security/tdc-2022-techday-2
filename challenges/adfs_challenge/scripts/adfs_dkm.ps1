[CmdletBinding(SupportsShouldProcess=$true)]
param (
   [Parameter(Mandatory=$True)]
   [string]$ServiceAccount,
   [Parameter(Mandatory=$True)]
   [string]$AdfsAdministratorAccount
)

$ServiceAccountSplit = $ServiceAccount.Split("\");
if ($ServiceAccountSplit.Length -ne 2)
{
	Write-error "Specify the ServiceAccount identifier in 'domain\username' format"
	exit 1
}

$AdfsAdministratorAccountSplit = $AdfsAdministratorAccount.Split("\");
if ($AdfsAdministratorAccountSplit.Length -ne 2)
{
	Write-error "Specify the AdfsAdministratorAccount identifier in 'domain\username' format"
	exit 1
}

#######################################
## Verify AD module is installed
#######################################
$m = "ActiveDirectory"
if (Get-Module | Where-Object {$_.Name -eq $m})
{
    write-verbose "Module $m is already imported."
}
else
{
    if (Get-Module -ListAvailable | Where-Object {$_.Name -eq $m})
    {
        Import-Module $m -Verbose
    }
    else
    {
        write-error "Module $m was not imported, install the Active Directory RSAT package and retry."
        exit 1
    }
}

push-location ad:

#######################################
## Generate random DKM container name
## The OU Name is a randomly generated Guid
#######################################
[string]$guid = [Guid]::NewGuid()
write-verbose ("OU Name" + $guid)

$ouName = $guid
$initialPath = "CN=Microsoft,CN=Program Data," + (Get-ADDomain).DistinguishedName
$ouPath = "CN=ADFS," + $initialPath
$ou = "CN=" + $ouName + "," + $ouPath

#######################################
## Create DKM container and assign default ACE which allows AD FS admin read access
#######################################

if ($pscmdlet.ShouldProcess("$ou", "Creating DKM container and assigning access"))
{
    Write-Verbose ("Creating organizational unit with DN: " + $ou)

    if ($AdfsAdministratorAccount.EndsWith("$"))
    {
        write-verbose "AD FS administrator account passed with $ suffix indicating a computer account"
        $userNameSplit = $AdfsAdministratorAccount.Split("\");
        $strSID = (Get-ADServiceAccount -Identity $userNameSplit[1]).SID
    }
    else
    {
        write-verbose "AD FS administrator account is a standard AD user"
        $objUser = New-Object System.Security.Principal.NTAccount($AdfsAdministratorAccount)
        $strSID = $objUser.Translate([System.Security.Principal.SecurityIdentifier])
    }

    if ($null -eq (Get-ADObject -Filter {distinguishedName -eq $ouPath}))
    {
        Write-Verbose ("First creating initial path " + $ouPath)
        New-ADObject -Name "ADFS" -Type Container -Path $initialPath
    }

    $acl = get-acl -Path $ouPath
    [System.DirectoryServices.ActiveDirectorySecurityInheritance]$adSecInEnum = [System.DirectoryServices.ActiveDirectorySecurityInheritance]::All
    $ace1 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"GenericRead","Allow",$adSecInEnum

    $acl.AddAccessRule($ace1)
    set-acl -Path $ouPath -AclObject $acl

    New-ADObject -Name $ouName -Type Container -Path $ouPath
}


#######################################
## Grant the following permission to the service account
# Read
# Create Child
# Write Owner
# Delete Tree
# Write DACL
# Write Property
#######################################
if ($ServiceAccount.EndsWith("$"))
{
    write-verbose "service account passed with $ suffix indicating a gMSA"
    $userNameSplit = $ServiceAccount.Split("\");
    $strSID = (Get-ADServiceAccount -Identity $userNameSplit[1]).SID
}
else
{
    write-verbose "service account is a standard AD user"
    $objUser = New-Object System.Security.Principal.NTAccount($ServiceAccount)
    $strSID = $objUser.Translate([System.Security.Principal.SecurityIdentifier])
}

if ($pscmdlet.ShouldProcess("$strSID", "Granting GenericRead, CreateChild, WriteOwner, DeleteTree, WriteDacl and WriteProperty"))
{
    [System.DirectoryServices.ActiveDirectorySecurityInheritance]$adSecInEnum = [System.DirectoryServices.ActiveDirectorySecurityInheritance]::All
    $ace1 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"GenericRead","Allow",$adSecInEnum
    $ace2 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"CreateChild","Allow",$adSecInEnum
    $ace3 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"WriteOwner","Allow",$adSecInEnum
    $ace4 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"DeleteTree","Allow",$adSecInEnum
    $ace5 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"WriteDacl","Allow",$adSecInEnum
    $ace6 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"WriteProperty","Allow",$adSecInEnum

    $acl = get-acl -Path $ou

    $acl.AddAccessRule($ace1)
    $acl.AddAccessRule($ace2)
    $acl.AddAccessRule($ace3)
    $acl.AddAccessRule($ace4)
    $acl.AddAccessRule($ace5)
    $acl.AddAccessRule($ace6)

    $acl.SetOwner($strSID)

    set-acl -Path $ou -AclObject $acl
}

#######################################
## Grant the following permission to the adfs admin account
# Read
# Create Child
# Write Owner
# Delete Tree
# Write DACL
# Write Property
#######################################

if ($AdfsAdministratorAccount.EndsWith("$"))
{
    write-verbose "AD FS administrator account passed with $ suffix indicating a gMSA"
    $userNameSplit = $AdfsAdministratorAccount.Split("\");
    $strSID = (Get-ADServiceAccount -Identity $userNameSplit[1]).SID
}
else
{
    write-verbose "AD FS administrator account is a standard AD user"
    $objUser = New-Object System.Security.Principal.NTAccount($AdfsAdministratorAccount)
    $strSID = $objUser.Translate([System.Security.Principal.SecurityIdentifier])
}

if ($pscmdlet.ShouldProcess("$strSID", "Granting GenericRead, CreateChild, WriteOwner, DeleteTree, WriteDacl and WriteProperty"))
{
    [System.DirectoryServices.ActiveDirectorySecurityInheritance]$adSecInEnum = [System.DirectoryServices.ActiveDirectorySecurityInheritance]::All
    $ace1 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"GenericRead","Allow",$adSecInEnum
    $ace2 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"CreateChild","Allow",$adSecInEnum
    $ace3 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"WriteOwner","Allow",$adSecInEnum
    $ace4 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"DeleteTree","Allow",$adSecInEnum
    $ace5 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"WriteDacl","Allow",$adSecInEnum
    $ace6 = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $strSID,"WriteProperty","Allow",$adSecInEnum

    $acl = get-acl -Path $ou

    $acl.AddAccessRule($ace1)
    $acl.AddAccessRule($ace2)
    $acl.AddAccessRule($ace3)
    $acl.AddAccessRule($ace4)
    $acl.AddAccessRule($ace5)
    $acl.AddAccessRule($ace6)

    $acl.SetOwner($strSID)

    set-acl -Path $ou -AclObject $acl

    $adminConfig = @{"DKMContainerDn"=$ou}

    Write-Output $adminConfig
}

pop-location