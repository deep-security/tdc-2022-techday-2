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
      <Command>"C:\Program Files\Python310\python.exe"</Command>
      <Arguments>c:\Projects\VersionChecker.py</Arguments>
    </Exec>
  </Actions>
</Task>}

$loggeduser = $env:username
$localuser = $env:USERDOMAIN +"\"+ $env:username
$user = New-Object System.Security.Principal.NTAccount($loggeduser) 
$usersid = $user.Translate([System.Security.Principal.SecurityIdentifier]) 
$sid = $usersid.Value
$taskname = 'Version_Checker'
$filepath = 'C:\Projects\Ver_Check.xml'

$xmlinfo.Task.RegistrationInfo.Author = $localuser
$xmlinfo.Task.Principals.Principal.UserId = $sid

$xmlinfo.Save($filepath)

Register-ScheduledTask -xml (Get-Content 'C:\Projects\Ver_Check.xml' | out-string) -TaskName $taskname -Password 'TrendMicro0!' -User $localuser 
