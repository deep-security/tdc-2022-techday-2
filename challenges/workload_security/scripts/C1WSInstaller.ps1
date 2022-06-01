<powershell>
#requires -version 4.0

# PowerShell 4 or up is required to run this script
# This script detects platform and architecture.  It then downloads and installs the relevant Deep Security Agent package

[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
iex ((new-object net.webclient).DownloadString('https://chocolatey.org/install.ps1'))
choco install python --version=3.10.4 -y
choco install awscli -y
pip install requests
pip install boto3

if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
   Write-Warning "You are not running as an Administrator. Please try again with admin privileges."
   exit 1
}

$C1WSRegion = [IO.File]::ReadAllText("c:\Projects\C1WSRegion.txt")
$managerUrl="https://workload." + C1WSRegion + ".cloudone.trendmicro.com:443/"

$env:LogPath = "$env:appdata\Trend Micro\Deep Security Agent\installer"
New-Item -path $env:LogPath -type directory
Start-Transcript -path "$env:LogPath\dsa_deploy.log" -append

echo "$(Get-Date -format T) - DSA download started"
if ( [intptr]::Size -eq 8 ) { 
   $sourceUrl=-join($managerUrl, "software/agent/Windows/x86_64/20.0.0.3288/agent.msi") }
else {
   $sourceUrl=-join($managerUrl, "software/agent/Windows/i386/20.0.0.3288/agent.msi") }
echo "$(Get-Date -format T) - Download Deep Security Agent Package" $sourceUrl

$ACTIVATIONURL = [IO.File]::ReadAllText("c:\Projects\C1WSActivationURL.txt")
$C1WStenantID = [IO.File]::ReadAllText("c:\Projects\C1WStenant.txt")
$C1WStokenID = [IO.File]::ReadAllText('c:\Projects\C1WStoken.txt')

$WebClient = New-Object System.Net.WebClient

# Add agent version control info
$WebClient.Headers.Add("Agent-Version-Control", "off")
$WebClient.QueryString.Add("windowsVersion", (Get-CimInstance Win32_OperatingSystem).Version)
$WebClient.QueryString.Add("windowsProductType", (Get-CimInstance Win32_OperatingSystem).ProductType)

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12;

Try
{
     $WebClient.DownloadFile($sourceUrl,  "$env:temp\agent.msi")
} Catch [System.Net.WebException]
{
      echo " Please check that your Workload Security Manager TLS certificate is signed by a trusted root certificate authority."
      exit 2;
}

if ( (Get-Item "$env:temp\agent.msi").length -eq 0 ) {
    echo "Failed to download the Deep Security Agent. Please check if the package is imported into the Workload Security Manager. "
 exit 1
}
echo "$(Get-Date -format T) - Downloaded File Size:" (Get-Item "$env:temp\agent.msi").length

echo "$(Get-Date -format T) - DSA install started"
echo "$(Get-Date -format T) - Installer Exit Code:" (Start-Process -FilePath msiexec -ArgumentList "/i $env:temp\agent.msi /qn ADDLOCAL=ALL /l*v `"$env:LogPath\dsa_install.log`"" -Wait -PassThru).ExitCode 
echo "$(Get-Date -format T) - DSA activation started"

Start-Sleep -s 50
& $Env:ProgramFiles"\Trend Micro\Deep Security Agent\dsa_control" -r
& $Env:ProgramFiles"\Trend Micro\Deep Security Agent\dsa_control" -a $ACTIVATIONURL ""tenantID:"$DStenantID" ""token:"$DStokenID"
Stop-Transcript
echo "$(Get-Date -format T) - DSA Deployment Finished" 