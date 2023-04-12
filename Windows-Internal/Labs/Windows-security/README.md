# Windows defender

## Table of contents

- [Windows defender](#windows-defender)
  - [Table of contents](#table-of-contents)
  - [Registry](#registry)
    - [About](#about)
      - [Hive](#hive)
      - [Value](#value)
      - [Boot Keys](#boot-keys)
      - [User Log-on](#user-log-on)
      - [Run/RunOnce Keys, ASEPs, and Startup](#runrunonce-keys-aseps-and-startup)
      - [Startup Keys](#startup-keys)
      - [AppInit DLLs](#appinit-dlls)
      - [Known DLLs](#known-dlls)
      - [File Type Association](#file-type-association)
      - [Bypass UAC](#bypass-uac)
      - [Create simple malware](#create-simple-malware)
  - [Windows defender](#windows-defender-1)
    - [About](#about-1)
    - [Bypass Windows defender](#bypass-windows-defender)
  - [Trusted platform module](#trusted-platform-module)

---

## Registry

`Windows Register`’ is a central, hierarchical database of keys and values

### About

Some noticeable paths:

- `System-wide registry`: C:\Windows\System32\Config
- `user-specific`: \Windows\Users\{UserName}\NTUSER.dat

#### Hive

![](https://i.ibb.co/FWz09fC/Screenshot-2023-04-12-065335.png)

#### Value

![](https://i.ibb.co/g3bv8Hn/Screenshot-2023-04-12-065634.png)

#### Boot Keys

The Session Manager (ssms.exe) manages the sessions for each of your users in the Windows environment, `autochk.exe` or `authochk` are used to verify the integrity of the disks before the startup

```
  HKLM\SYSTEM\ControlSet002\Control\Session Manager\BootExecute
```

#### User Log-on

- `UserInit` key is used by Windows to launch login
- `Shell` key points to explorer.exe

```
  HKLM\Software\Microsoft\WindowsNT\CurrentVersion\Winlogon\UserInit
  HKCU\Software\Microsoft\WindowsNT\CurrentVersion\Winlogon\Shell 
  HKLM\Software\Microsoft\WindowsNT\CurrentVersion\Winlogon\Shell 
  HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\IniFileMapping\system.ini\boot
```
#### Run/RunOnce Keys, ASEPs, and Startup

- `Run and RunOnce` keys are used to launch programs whenever a user logs on to the system
- `RunServices and services` and relevant keys are used to start up background services

```
  HKCU\Software\Microsoft\Windows\CurrentVersion\Run 
  HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce 
  HKLM\Software\Microsoft\Windows\CurrentVersion\Run 
  HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
  HKLM\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
  HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
  HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices
  HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce
  HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup
  HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services
```

#### Startup Keys

Set up user’s personal folders

```
  HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders 
  HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders
  HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders
  HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders
```
#### AppInit DLLs

Several DLL files are loaded by the `User32.dll` file.  This registry key is worth mentioning and monitoring for malware residence

```
  HKLM\Software\Microsoft\WindowsNT\CurrentVersion\Windows\AppInit_DLLs
```

#### Known DLLs

This key makes sure the DLLs are known to the system and can be included from a path that’s purposefully placed before the path of the original file

```
  HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs 
```

#### File Type Association

Run from this CLASSES_ROOT hive as this is where the associations are kept when openning application

```
  HKLM\Software\Classes\
  HKEY_CLASSES_ROOT\
```
#### Bypass UAC

What will do in this part:
- Find an EXE file in system32 having administrator privallage (in manifest has 2 values are true)
- Find DLL in import table of above file (is not DLL supplys api-ms-win and not in KnownDlls)
- Inject malicious code into above DLL
- Inject WinExecEXE code into explorer.exe to run malicious DLL

#### Create simple malware

For education purpose, create a malware can download malicoius DLL from Internet, and this DLL will pop up MessageBox (in real scenarios, this DLL will change value or add new registry for illegal purpose), all materials can be found [here](/Windows-Internal/Labs/Windows-security/Material/)

To compile DLL:

```shell
  g++ -shared -o evil.dll evil.cpp -fpermissive
```

To compile injection:

```
  g++ -O2 inject.cpp -o inject.exe -mconsole -lwininet -s -ffunction-sections -fdata-sections -Wno-write-strings -fno-exceptions -fmerge-all-constants -static-libstdc++ -static-libgcc -fpermissive
```

## Windows defender

### About

It is built-in mododule software application that safeguards a system from malware, some useful features:

- `Virus & threat protection`
  - `Real-time protection` automatically locate and stop malware
  - `Cloud-delivered protection`
  - `Automatic sample submission` sends sample files to Microsoft
  - `Tamper Protection`
  - `Controlled folder access` protect files, folders, and memory areas
  - `Exclusions` makes Microsoft Defender Antivirus won't scan items that have been excluded
- `Account protection`
  - `Window Hello` uses biometrc to secure sign-in
  - `Dynamic lock` when paired device away
- `Firewall & network protection`
- `App & browser control`
  - `Smart app control` protect from untrusted app
  - `Reputation-based protection` protect from malicious or potentially unwanted websites, apps, files
    - `SmartScreen` protect unrecognized apps
    - `Phishing protection`
    - `Potentially unwanted app blocking`
  - `Exploit protection` protect from attacks
- `Device security`
  - `Core Isolation` (Virtualization-based)
    - `Memory integrity` prevents attacks from inserting malicious code
    - `Local Security Authority protection` protects user credentials by preventing unsigned drivers and plugins 
    - `Microsoft Vulnerable Driver Blocklist` blocks drivers with security vulnerabilities 

### Bypass Windows defender

Check regedit with Powershell, it will shows some above features

```powershell
  reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows Defender"
```
In fact, `Exclusions` allow app run without scanning, so attackers can transfer malware to `Exclusions` folder with Powershell command 
```powershell
  reg query "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows Defender\Exclusions\Paths"
```

Start transfer malware to above path
```powershell
  Start-BitsTransfer -Priority foreground -Source <path-of-malware> -Destination <path-of-exclusions>
``` 

## Trusted platform module

TPM 2.0 includes Windows Hello for identity protection and BitLocker for data protection. Some of the advantages of using TPM technology are:

- Generate, store, and limit the use of cryptographic keys
- Use it for device authentication by using the TPM's unique RSA key, which is burned into the chip
- Help ensure platform integrity by taking and storing security measurements of the boot process


