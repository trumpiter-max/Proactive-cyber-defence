## Table of content
- [Security rating](#security-rating)
- [Influenced the design of Windows](#influenced-the-design-of-windows)
- [Virtualization-based security](#virtualization-based-security)
    - [Credential Guard](#credential-guard)
    - [Device Guard](#device-guard)
- [Protecting objects](#protecting-objects)
- [The AuthZ API](#the-authz-api)
- [Account rights and privileges](#account-rights-and-privileges)
- [Access tokens of processes and threads](#access-tokens-of-processes-and-threads)
- [Security auditing](#security-auditing)
- [AppContainers](#appcontainers)
- [Logon](#logon)

Influenced design and implementation by `stringent requirements` 

## Security rating

Current security rating standard: `Common Criteria (CC) - 1996`:

- More **flexible and closer** to the `ITSEC` than the `TCSEC`  
- `Security system components`: core components and databases 
- `Security reference monitor (SRM)`: in the `Windows executive - Ntoskrnl.exe`, represent a *security context, security access check, user right, security audit messages*
- `Local Security Authority Subsystem Service (Lsass)`: local system *security policy*, *user authentication*, send security audit messages to the event log, `Lsasrv.dll` - a library that `Lsass` loads
- `LSAIso.exe (Credential Guard)`: used by `Lsass`, store *users’ token hashes*
- `Lsass policy database`: under `HKLM\SECURITY`, contains the local system security policy settings, logon information used for cached *domain logons* and Windows service *user-account logons*
- `Security Accounts Manager (SAM)`:  in `Samsrv.dll`, manage the database containing the user names and groups defined on the *local machine*
- `SAM database`: in the *registry* under `HKLM\SAMstore` defined local users and groups, system’s administrator recovery account
- `Active Directory`: directory service containing a database of objects in *single entity*, implemented as `Ntdsa.dll`
-  `Authentication packages`:  include `dynamic link libraries (DLLs)` , authenticate user’s security identity
- `Interactive logon manager (Winlogon)`:  `Winlogon.exe`, response to the SAS, manage interactive logon sessions
- `Logon user interface (LogonUI)`: `LogonUI.exe`, presents users with the user interface to authenticate, query user credentials through various methods
- `Credential providers (CPs)`:  are `authui.dll`, `SmartcardCredentialProvider.dll`, `BioCredProv.Dll`, `FaceCredentialProvider.dll`, a face-detection provider
- `Network logon service (Netlogon)`: `Netlogon.dll` sets up the secure channel to a domain controller
- `Kernel Security Device Driver (KSecDD)`: kernel-mode library `(%SystemRoot%\System32\Drivers\Ksecdd.sys)`, `Encrypting File System (EFS)`, use to communicate with `Lsass`
- `AppLocker`: consists of a driver `(%SystemRoot%\System32\Drivers\AppId.sys)` and `AppIdSvc.dll`, allow administrators to specify executable files, DLLs, and scripts

---

## Influenced the design of Windows

The `Trusted Computer System Evaluation Criteria (TCSEC) - 1981` includes `levels-of-trust` ratings. Core
requirements for any secure operating system `(C2)`:
- `Secure logon facility`: access to the computer only after being been authenticated
- `Discretionary access control`: allows the owner of a resource to determine 
- `Security auditing`: detect, record *security-related events* or *resources actions*
- `Object reuse protection`: prevents users from seeing data that another user has deleted `B-level` security:
- `Trusted path functionality`: prevents Trojan from intercept user data
- `Trusted facility management`: separate account roles for administrative functions

---

## Virtualization-based security

- Common to refer to the `kernel` as *trusted*
- `Virtualization-based security (VBS)`
- `Virtual trust level (VTL)`
- `normal user-mode` and `kernel` code runs in `VTL0`; `VTL1` requires Secure Boot
- `Isolated User Mode`: cannot gain access to anything stored in `VTL1`

### Credential Guard

Some or all of these components in the memory of `Lsass`
- `LSA (Lsass.exe)` and `Isolated LSA (LsaIso.exe)`
- `Password`: primary credential 
- `NT one-way function (NT OWF)`: MD4 hash used by legacy components, using the `NT LAN Manager (NTLM)` protocol
- `Ticket-granting ticket (TGT)`: using `Kerberos`, default on `Windows Active Directory–based` domains
- `Protecting the password`:  encrypted, stored to provide `single sign-on (SSO)`. Biometric credentials  against hardware tracking application.  Similar method `Two-factor authentication (TFA)` 
- `Protecting the NTOWF/TGT key`: protecting `Lsass` - config DWORD value `RunAsPPL` in `HKLM\System\CurrentControlSet\Consol\Lsa` registry key to 1. Moreover, use `Lsaiso.exe`(`VTL 1`) alter `Lsass`is more secure
- `Secure communication`: `Advanced Local Procedure Call (ALPC)` - `Secure Kernel` supported by `NtAlpc` calls to the `Normal Kernel`. `Isolated User Mode` support for the `RPC runtime library (Rpcrt4.dll)` over the ALPC protocol allowing VTL 0 and 1 to communicate using local `RPC`
- `UEFI lock`: prevent from disabling `Credential Guard`
- `Authentication policies` and armored `Kerberos`: `VTL 1` Secure Kernel using `TPM`, two security guarantees are provided:
- The user is authenticating from a known machine
-  The `NTLM` response/user ticket is coming from isolated `LSA` and has not been manually
generated from `Lsass`
- `Future improvements`: combined with `BioIso.exe` and `FsIso.exe`

### Device Guard

- `Hypervisor-Based Code Integrity (HVCI)` and `Kernel-Mode Code Integrity (KMCI)`
- Fully configurable, protect machine from different kinds of `software-based` and `hardware-based` attacks
- Moving all `code-signing` enforcement into `VTL1` (in a library called `SKCI.DLL`, or
`Secure Kernel Code Integrity`)

---

## Protecting objects 

Using with WinObj Sysinternals tool. The Windows integrity mechanism is used by `User Account Control (UAC)` elevations
- Access checks with `SRM` (object manager) and three inputs: the security identity of a thread, the access that the thread wants to an object, and the security settings of the object
- Security identifiers: using `Windows uses security identifiers (SIDs)`  used to uniquely identify a security principal or security group
- Integrity levels ( or `AppContainer` used by `UWP apps`): `Mandatory Integrity Control (MIC)` allows the SRM to have more detailed information, obtained with the `GetTokenInformation API`
- `Tokens` used by `SRM`  to identify the security context of a process or thread including `session ID`
- Impersonation provides access to resources, lets a server notify the `SRM`
- `Restricted tokens`  is created from a primary or `impersonation token` using the `CreateRestrictedToken` function, impersonate a client at a reduced security level, primarily for safety reasons when running `untrusted code`, also used by `UAC` to create the `filtered admin token`
- `Virtual service accounts` improves the security isolation and access control
- `Security descriptors` and `access control`
- `ACL assignment`
- `Trust ACEs`:   is part of a `token object` that exists for tokens attached to protected or `PPL processes`
- `Determining access`: `mandatory integrity check` and `discretionary access check`
- `User Interface Privilege Isolation`: prevents processes with a lower integrity level (IL) from sending messages to higher IL processes
- `Owner Rights` improves service hardening in the operating system and allow more flexibility for specific usage scenarios
- `A warning regarding the GUI security editors` shows the order of ACEs in the
DACL to know what access a particular user or group will have to an object
- `Dynamic Access Control`: flexible mechanism used to define rules based on custom attributes defined in `Active Directory`

---

## The AuthZ API

- Same security model as the `security reference monitor (SRM)` but in user mode in the `%SystemRoot%\System32\Authz.dll` library, improve subsequent checks.
- Allow applications to perform customizable access checks with better performance and more simplified development than `Low-level Access Control` and cache access checks for improved performance, to query and modify client contexts, and to define business rules that can be used to evaluate access permission dynamically
- `Conditional ACEs`: are a form of `CALLBACK ACEs` with a special format of the application data, allows a conditional expression to be evaluated when an access check

---

## Account rights and privileges
- A `privilege` allows account to perform a particular system-related operation
- An `account right` grants or denies the account to perform a particular type of logon
- A `system administrator` assigns privileges to groups and accounts using tools such as the `Active Directory Users` and `Groups MMC` snap-in for domain accounts or the `Local Security Policy editor (%SystemRoot%\System32\secpol.msc)`
- `Account rights`: the function responsible for
logon is `LsaLogonUser` - takes a parameter
that indicates the type of logon being performed
- `Privileges`: is a privilege constant
- `Super privileges`: full control over a computer, gain unauthorized access to otherwise off-limit resources and to perform unauthorized operations 

---

## Access tokens of processes and threads

![basic process
and thread security structures](https://www.oreilly.com/api/v2/epubs/9780735671294/files/httpatomoreillycomsourcemspimages1568995.png.jpg)

---

## Security auditing

- `Object manager` can generate `audit events` as a result of an access check, and Windows functions
available to user applications can generate them directly
- A process must have the `SeSecurityPrivilege` privilege to manage the security event
log and to view or set an object’s `SACL`
- The `audit policy` configuration (both the basic settings under `Local Policies` and the `Advanced Audit Policy Configuration`) is stored in the registry as a bitmapped value in the `HKEY_LOCAL_MACHINE\SECURITY\Policy\PolAdtEv`
- `Object access auditing` has two types of audit ACEs: access allowed and access denied
- `Global audit policy` is defined for the
system that enables `object-access` auditing for all `file-system objects`, all `registry keys`, or for both. Using `AuditPol` command with the
/resourceSACL option to set or query the global audit policy
- `Advanced Audit Policy settings`: the security audit policy settings under `Security Settings\Advanced Audit Policy Configuration` can help your organization audit compliance with iAppContainers
mportant business-related and security-related rules by tracking precisely defined activities

---

## AppContainers

- Security sandbox created primarily to host `UWP processes`
- `Overview of UWP apps`: `Universal Windows Platform (UWP)` use `WinRT APIs` to provide powerful UI and advanced asynchronous features
    - Produce normal executables, just like desktop apps. `Wwahost.exe` `(%SystemRoot%\System32\wwahost.exe)` is used to host `HTML/JavaScript-based` UWP apps, as those produce a DLL, not an executable
- `The AppContainer`: characteristics of packaged processes running inside
    - The process token integrity level is set to Low
    - UWP processes are always created inside a job
    - The token for UWP processes has an AppContainer SID
    - The token may contain a set of capabilities
    - Containing a set of capabilities, each represented with a SID
    - Containing privileges: `SeChangeNotifyPrivilege, SeIncrease-WorkingSetPrivilege, SeShutdownPrivilege, SeTimeZonePrivilege`, and `SeUndockPrivilege`
    - The token will contain up to four security attributes
        - WIN://PKG
        - WIN://SYSAPPID
        - WIN://PKGHOSTID
        - WIN://BGKD
- `AppContainer security environment`
- `AppContainer capabilities`
- `AppContainer and object namespace`
- `AppContainer handles`
- `Brokers`: Windows provides helper processes, called brokers, managed by the system broker process, `RuntimeBroker.exe`

---

## Logon

<<<<<<< Updated upstream
=======
## User Account Control and virtualization

## Exploit mitigations

## Application Identification

- AppID providing a single set of APIs and data structures to identify and distinguish the application from other applications, provide a consistent and recognizable way to refer to the application.
- AppID contains:
    - Fields
    - File hash
    - The partial or complete path to the file
- AppID stored in process access token

## AppLocker
- Allows an administrator to lock down a system to prevent unauthorized programs from being run.
- AppLocker's auditing mode allows an administrator to create an AppLocker policy and examine the results
- Two types of rule in AppLocker:
    - Allow the specified files to run, denying everything else.
    - Deny the specified files from being run, allowing everything else. Deny rules take precedence over allow rules.
- AppLocker can created rule with the following criteria:
    - Fields within a code-signing certificate embedded within the file, allowing for different combinations of publisher name, product name, file name, and version
    - Directory path, allowing only files within a particular directory tree to run
    - File hash

- AppLocker stored in registry
    - HKLM\Software\Policies\Microsoft\Windows\SrpV2
    - HKLM\SYSTEM\CurrentControlSet\Control\Srp\Gp\Exe
    - HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Group Policy
Objects\\{GUID}Machine\Software\Policies\Microsoft\Windows\SrpV2


## Software Restriction Policies

## Kernel Patch Protection

## PatchGuard

## HyperGuard

## Conclusion

>>>>>>> Stashed changes
