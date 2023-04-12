# Windows event 

Is an in-depth record of events related to the system, security, and application stored on a Windows operating system

## Table of contents

- [Windows event](#windows-event)
  - [Table of contents](#table-of-contents)
  - [About Windows Event](#about-windows-event)
    - [Event Log Format](#event-log-format)
    - [Account Logon and Logon Events](#account-logon-and-logon-events)
    - [Access to Shared Objects](#access-to-shared-objects)
    - [Scheduled Task Logging](#scheduled-task-logging)
    - [Object Access Auditing](#object-access-auditing)
    - [Audit Policy Changes](#audit-policy-changes)
    - [Auditing Windows Services](#auditing-windows-services)
    - [Process Tracking](#process-tracking)
    - [Additional Program Execution Logging](#additional-program-execution-logging)
    - [Auditing PowerShell Use](#auditing-powershell-use)
  - [Analyze evtx](#analyze-evtx)
    - [Event viewer](#event-viewer)
    - [XML format](#xml-format)
  - [Sysmon](#sysmon)

---

## About Windows Event

EventID can be looked up at [here](https://www.myeventlog.com/search/find)

### Event Log Format

- Stored in the `%SystemRoot%\System32\winevt\logs` directory by default in the binary XML Windows Event Logging format, designated by the `.evtx` extension
- Transported over `HTTPS` on port `5986` using `WinRM`(Windows Remote Management)

### Account Logon and Logon Events

- Account Logon is for authentication, performed by a domain controller
- Logon is used to refer to an account gaining access to a resource
- Easily set by `Group Policy`

### Access to Shared Objects

- Can be editted in `Group Policy Management Console` by navigating to `Computer Configuration -> Policies -> Windows Settings -> Security Settings -> Advanced Audit Policy Configuration -> Audit Policies -> Object Access -> Audit File Share`
- the access can be found in the registry key `NTUSER\Software\Microsoft\Windows\CurrentVersion\Explorer\MountPoints2`

### Scheduled Task Logging

- Record activity relating to scheduled tasks
- Check at `%SystemRoot%\System32\winevt\Logs\Microsoft-Windows-TaskScheduler`

### Object Access Auditing

-  Audited for object access
- Config at `Local Security Policy to set Security Settings -> Local Policies -> Audit Policy -> Audit object access` 

### Audit Policy Changes

- Logging these changes when audit policy occur 
- The Event ID used for this auditing is 4719 & 1102

### Auditing Windows Services

- Recording events related to starting and stopping of services 
- Config at `Advanced Audit Policy Configuration > System Audit Policies > System > Audit Security`

### Process Tracking

- Loggin full command lines in process creation events and providing a trail to uncover the actions 
- Located in Group Policy settings
  - `Computer Configuration -> Windows Settings -> Security Settings -> Local Policies -> Audit Policy -> Audit process tracking`
  - `Computer Configuration -> Administrative Templates -> System -> Audit Process Creation -> Include`

### Additional Program Execution Logging

- `AppLocker` presented in Event Viewer under `Application and Services Logs\Microsoft\Windows\AppLocker` and stored with the other event logs in `C:\Windows\System32\winevt\Logs` (aka Microsoft-WindowsAppLocker%4EXE and DLL.evtx)
- `Windows Defender` logs are located at `C:\Windows\System32\winevt\Logs\Microsoft-Windows-Windows Defender%4Operational.evtx` and `Microsoft-Windows-Windows Defender%4WHC.evtx`
- `Sysmon` logs are located at `Applications and Services \Logs\Microsoft\Windows\Sysmon\Operational` and `C:\Windows\System32\winevt\Logs\Microsoft-Windows-Sysmon%4Operational.evtx`

### Auditing PowerShell Use

- Config at `Computer Configuration -> Policies -> Administrative Templates -> Windows Components -> Windows PowerShell`
- Located 

## Analyze evtx

There are 2 method to views:
- Use Event viewer to view directly
- Convert file into `XML format` to use with third-party application 

### Event viewer

Some general information in `Event viewer`:
- *Level*: it shows which type of event (Error/Warning/Information/Audit Success/Audit Failureg)
- *Date and time*: when log created
- *Source*: name of the software that logs the event 
- *EventID*: useful to detect what actions
  
Details data:
- *Provider*: service logs events - Guid: unique ID that is computed by Windows and Windows applications
- *UserID*: visualize when SIDs are converted from a binary to a string format by using standard notation, details at [here](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers)
- *SourceImage* & *TargetImage*: process opens another process
- *GrantedAccess*: grant users one or more access rights to event logs. These access rights include Read, Write, and Clear
- *CallTrace*: which processes called

### XML format

Using `Powershell` to convert and save XML file (designed to store and transport data) 
```powershell
  get-winevent -Path ".\CA_teamviewer-dumper_sysmon_10.evtx" -oldest | convertto-xml -as Stream -depth 10 > ".\teamviewer.xml"
```
## Sysmon 

Aka system monitor

![](https://i.ibb.co/yf82p5M/Screenshot-2023-04-10-090043.png)