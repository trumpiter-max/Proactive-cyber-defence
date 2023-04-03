# Intermediate cases

Some unknown cases

## Table of contents

- [Intermediate cases](#intermediate-cases)
  - [Table of contents](#table-of-contents)
  - [Attack trace](#attack-trace)
    - [Sumary](#sumary)
    - [Details](#details)
      - [Session 1](#session-1)
      - [Session 2](#session-2)

---

## Attack trace

### Sumary

- Session 1: `89.114.205.102:1821` attack to `192.150.11.111:445` to check if SMB service is running (for file transfering) 
- Session 2: null attack to call DsRoleUpgradeDownlevelServer function

### Details

#### Session 1

Check at Statistics->Endpoints, and there are 2 hosts: `98.114.205.102` and `192.150.11.111` (attacker `98.114.205.102:445` (SMB) and victim `192.150.11.111:1821` (TCP/UDP)). Note: using [this tool](https://www.adminsub.net/tcp-udp-port-finder/) to check port

![](https://i.ibb.co/vwqNRx8/Screenshot-2023-03-24-131504.png)

Then, using [this tool](https://www.whatismyip.com/ip-address-lookup/) to find location of above addresses:

![](https://i.ibb.co/tqSV26v/Screenshot-2023-03-24-131815.png)

![](https://i.ibb.co/fHStvPs/Screenshot-2023-03-24-131923.png)

Check at Statistics->Capture file properties to find Timespan, Average Packages

![](https://i.ibb.co/9cxLXyg/Screenshot-2023-03-24-132536.png)

Using filter in wireshark `tcp.flags==0x02` to find tcp dump (The hexadecimal number 0x02 the TCP SYN flag is present in the TCP header)

![](https://i.ibb.co/6vhF3KC/Screenshot-2023-03-24-132059.png)

#### Session 2

Using TCP flow (tcp.stream eq 1) to view what happen

![](https://i.ibb.co/98SKBGj/Screenshot-2023-04-03-100119.png)

Some noticeable keywords in above photo:
- Windows for Workgroups 3.1 is extension for Windows 3.1, built-in file transfering of SMB, more at [here](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-smb2/8df1a501-ce4e-4287-8848-5f1d4733e280)
- NTLMSSP is a binary messaging protocol used by the Microsoft Security Support Provider Interface (SSPI) to facilitate NTLM challenge-response authentication, details at [here](https://learn.microsoft.com/vi-vn/windows/win32/com/ntlmssp)
- \PIPE\lsass is the local security authentication server, and it generates the
process responsible for authenticating users for the Winlogon service

Using find packet with above keyword to view details from 14th packet

![](https://i.ibb.co/Pcz746T/Screenshot-2023-04-03-133750.png)

- 14th - 18th: NTLM user authentication with user: \
- 19th - 23th: send requests to connect $IPC (Inter Process Communication) with path \\\192.150.11.111\ipc\$ through \lsarpc (Remote Procedure Call)
  
![](https://i.ibb.co/YZ2M1rv/Screenshot-2023-04-03-135949.png)

- 25th - 33rd: using DSSETUP V0.0 (32bit NDR) to call function DsRoleUpgradeDownlevelServer 








