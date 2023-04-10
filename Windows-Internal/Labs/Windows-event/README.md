# Windows event 

Is an in-depth record of events related to the system, security, and application stored on a Windows operating system

## Table of contents

- [Windows event](#windows-event)
  - [Table of contents](#table-of-contents)
  - [Analyze evtx](#analyze-evtx)
    - [Event viewer](#event-viewer)
    - [XML format](#xml-format)
  - [Sysmon](#sysmon)

---

## Analyze evtx

There are 2 method to views:
- Use Event viewer to view directly
- Convert file into XML format to use with third-party application 

### Event viewer

Some general information in `Event viewer`:
- *Level*: it shows which type of event (Error/Warning/Information/Audit Success/Audit Failureg)
- *Date and time*: when log created
- *Source*: name of the software that logs the event 
- *EventID*: can be found [here](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)

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