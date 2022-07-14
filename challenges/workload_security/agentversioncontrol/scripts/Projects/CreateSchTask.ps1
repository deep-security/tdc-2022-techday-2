#Set the XML information necessary to build the Windows Scheduled Task from the PoSH CLI
[xml]$xmlinfo = {<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2021-12-24T08:55:54.255108</Date>
    <Author></Author>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <Repetition>
        <Interval>PT5M</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <StartBoundary>2022-06-09T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId></UserId>
      <LogonType>Password</LogonType>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>"C:\Python310\python.exe"</Command>
      <Arguments>c:\Projects\VersionChecker.py</Arguments>
    </Exec>
  </Actions>
</Task>}

#Variables used for the creation
$loggeduser = $env:username
$localuser = $env:USERDOMAIN +"\"+ $env:username
#These next three lines are necessary for SID Mapping
$user = New-Object System.Security.Principal.NTAccount($loggeduser)
$usersid = $user.Translate([System.Security.Principal.SecurityIdentifier])
$sid = $usersid.Value
#More variables for the task creation
$taskname = 'Version_Checker'
$filepath = 'C:\Projects\Ver_Check.xml'

#Sets the Author and SID in the XML file that's output to the system dynamically.
$xmlinfo.Task.RegistrationInfo.Author = $localuser
$xmlinfo.Task.Principals.Principal.UserId = $sid

#Write the XML file
$xmlinfo.Save($filepath)

#Create the Windows Scheduled Task from the PoSH CLI
Register-ScheduledTask -xml (Get-Content 'C:\Projects\Ver_Check.xml' | out-string) -TaskName $taskname -Password 'TrendMicro0!' -User $localuser  | Out-Host
#Start the Scheduled Task created with the CreateSchTask script
Start-ScheduledTask -TaskName "Version_Checker"

#reboot after Schedule task creation
Start-Sleep -Seconds 10
Restart-Computer -Force