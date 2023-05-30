# Virtual private network

## Table of contents

- [Virtual private network](#virtual-private-network)
  - [Table of contents](#table-of-contents)
  - [Features](#features)
    - [Introduction](#introduction)
    - [How a VPN Helps with Network Security for business](#how-a-vpn-helps-with-network-security-for-business)
    - [VPN prevents attacks](#vpn-prevents-attacks)
    - [Types of VPN Protocols](#types-of-vpn-protocols)
  - [VPN tunnel](#vpn-tunnel)
      - [Split tunnel](#split-tunnel)
        - [Pros](#pros)
        - [Cons](#cons)
      - [Full tunnel](#full-tunnel)
        - [Pros](#pros-1)
        - [Cons](#cons-1)
    - [Overview OpenVPN access server](#overview-openvpn-access-server)
  - [Deploy](#deploy)
    - [Basic setup](#basic-setup)
    - [Configuration](#configuration)
      - [Network](#network)
  - [Hand-on labs](#hand-on-labs)


## Features

### Introduction

- Encrypt server and hides user IP address from third-party
- Make connection from shared or public network more secure

### How a VPN Helps with Network Security for business

- Secure connection
- Have servers in different countries
- Conceal internet activity
- Hide browsing history from ISPs
- Have capacity for large volumes of network traffic
- Include a `kill switch` - automatically disconnect user from the internet whenever VPN connection fails

### VPN prevents attacks

- `Spoofing`: block all packets with internal origins, from specific hosts, or ARP poisoning attack
- `Man-In-The-Middle attacks`: connection is encrypted
- `Logging`: encrypt record activities from ISP and others
- `DDoS`: generate high amount of bandwidth
- `Port Scanning`: limits number of ports or use port knocking 

### Types of VPN Protocols

- Internet Protocol Security or IPSec
- Layer 2 Tunneling Protocol (L2TP)
- Point–to–Point Tunneling Protocol (PPTP)
- Secure Sockets Layer (SSL) and Transport Layer Security (TLS)
- Secure Shell (SSH)

## VPN tunnel

`VPN tunnel` is an encrypted connection between your device and a `VPN server`

![](https://i.ibb.co/MNK7P9n/VPN-Tunneling-structure.png)

#### Split tunnel 

##### Pros

- Split tunneling the corporate data allows the VPN to require a smaller ethernet connection
- Corporate data is secured through IPSEC connectivity
- Data will flow out of the Internet connection and not go through the corporate network in cloud services
- Company updates can come through the IPSEC connection to the company
- Virus updates can come through the IPSEC connection to the company
- IDS/IPS still protects the company in the incoming/outgoing VPN interface activity

##### Cons
- Web activity goes out of the Internet and does not get inspected by the corporate network 
- Port scans can still happen to the laptop as it sits in a coffee shop
- Attackers can still use exploits to compromise the computer, gain access, and attach keyboard loggers to the laptop
- No change on the laptop attack surface except all traffic is encapsulated in an IPSEC tunnel
    
#### Full tunnel

##### Pros

- All traffic goes through the company for inspection
- All systems connected to the company for updates
- Internal AV systems can do updates if needed
- Host Inspection keeps systems off that are insecure
- IDS/IPS protects rouge laptops
- Web traffic can work through the web filter

##### Cons

- Increased bandwidth to the VPN to support ALL traffic going to the company
- Increased need for privacy controls
- Increased bandwidth to the company Internet connection so ALL systems can work
- Network roundtrip delays can be a problem as ALL traffic goes in and out the corporate network
- Port scans can still happen on the laptop as it sits in a coffee shop
- Remember security in layers on the laptop, because if the laptop gets compromised, then the attacker still has direct access to the laptops out of band scenarios
- Attackers can still use exploits to compromise the computer, gain access, and attach keyboard loggers to the laptop
- No change on the laptop attack surface except all traffic is encapsulated in an IPSEC tunnel

### Overview OpenVPN access server

- User authentication includes a built-in system with web-based management or external authentication with `PAM (Pluggable Authentication Modules)`, `LDAP (Lightweight Directory Access Protocol)`, `(SAML) Security Assertion Markup Language`, or `RADIUS (Remote Authentication Dial-In User Service)`
- `External PKI` is also possible for full control over an existing integrated PKI
- `VPN tunnels` are secured with the `OpenVPN protocol` using `TLS` authentication, credentials, certificates, and `MAC` address lock 
- `Access Control rules` can specify user or group access to IP address and subnets, and allow or disallow direct `VPN client connections`
- `Full-tunnel` and `split-tunnel` redirection: All `VPN client` internet traffic goes through the `VPN tunnel`, or only specified traffic, respectively
- Its type is `SSL VPN`

## Deploy

### Basic setup

Get started from [this post](https://openvpn.net/vpn-server-resources/installing-openvpn-access-server-on-a-linux-system/). Then go to [OpenVPN portal](https://as-portal.openvpn.com/get-access-server/ubuntu) to view instructions and install `Access server`. After installing, it will show admin account or use this command to view 

```bash
    sudo cat /usr/local/openvpn_as/init.log
```

Go to browser and login with above account, go back OpenVPN portal to get license key (Subscriptions) with free (limit 2 connection) or paid plan

### Configuration

#### Network

Go to network config in Admin UI dashboard, change type of connection to TCP then apply changes

IP of machine should be public in the Internet, simple method is using [Ngrok](https://ngrok.com/). Installing ngrok with snapd of Ubuntu

```bash
  sudo apt install snapd
  sudo snap install ngrok
```

Run ngrok with tcp protocal and port 443, it will generate address like this `0.tcp.ap.ngrok.io XXXXXX`

Go to above website and export ovpn file, it will show protocols with ports for connecting 

```bash
  remote <ip-address> 
```

Change it to 

```bash
  remote 0.tcp.ap.ngrok.io XXXXXX
```
## Hand-on labs