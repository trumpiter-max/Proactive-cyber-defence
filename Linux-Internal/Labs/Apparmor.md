# Apparmor

Mandatory Access Control (MAC) system which is a kernel (LSM) enhancement to confine programs to a limited set of resources

Some differences from SElinux and Apparmor

![](https://i.ibb.co/LSxN7sD/Screenshot-2023-04-11-142423.png)

## Table of contents

- [Apparmor](#apparmor)
  - [Table of contents](#table-of-contents)
  - [Get started](#get-started)
    - [Pros \& cons](#pros--cons)
      - [Pros](#pros)
      - [Cons](#cons)
    - [Mechanism](#mechanism)
    - [Check status of apparmor](#check-status-of-apparmor)
      - [Change mode of profile](#change-mode-of-profile)
      - [Config profiles](#config-profiles)


## Get started

### Pros & cons

#### Pros

- User-friendly and works directly with profiles (text files) for access control
- Protects any file on the system and allows for rules to be specified even for files that do not exist yet

#### Cons

- Does not have Multi-Level Security (MLS) and Multi-Category Security (MCS)
- Policy loading takes long

### Mechanism

![](https://i.ibb.co/dr2vxkW/Screenshot-2023-04-11-142651.png)

Rules:
- *Path entries* determine which files application can access 
- *Capability entries* specify the privileges process
- *Network entries* determines the connection-type. For example: tcp. For a packet-analyzer network can be raw or packet etc

Modes:
- *Complain mode*: the system reports policy violation attempts but does not enforce rules
- *Enforce mode*: inspected and all violations are stopped

### Check status of apparmor

```sh
    sudo apparmor_status
```
#### Change mode of profile

Enforce
```sh
    sudo aa-enforce /usr/sbin/tcpdump
```

Complain
```sh
    sudo aa-complain /usr/sbin/tcpdump
```
#### Config profiles

Profiles can be found at `/etc/apparmor.d/`



