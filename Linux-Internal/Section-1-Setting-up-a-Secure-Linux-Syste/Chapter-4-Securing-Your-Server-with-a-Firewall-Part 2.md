# Securing Your Server with a Firewall - Part 2

## Table of content

- [Securing Your Server with a Firewall - Part 2](#securing-your-server-with-a-firewall---part-2)
  - [Table of content](#table-of-content)
  - [Technical requirements](#technical-requirements)
  - [nftables – a more universal type of firewall system](#nftables--a-more-universal-type-of-firewall-system)
  - [Learning about nftables tables and chains](#learning-about-nftables-tables-and-chains)
    - [Getting started with nftables](#getting-started-with-nftables)
      - [Configuring nftables on Ubuntu 16.04](#configuring-nftables-on-ubuntu-1604)
      - [Configuring nftables on Ubuntu 18.04](#configuring-nftables-on-ubuntu-1804)
    - [Using nft commands](#using-nft-commands)
    - [Hands-on lab for nftables on Ubuntu](#hands-on-lab-for-nftables-on-ubuntu)
  - [firewalld for Red Hat systems](#firewalld-for-red-hat-systems)
    - [Verifying the status of firewalld](#verifying-the-status-of-firewalld)
    - [Working with firewalld zones](#working-with-firewalld-zones)
    - [Adding services to a firewalld zone](#adding-services-to-a-firewalld-zone)
    - [Adding ports to a firewalld zone](#adding-ports-to-a-firewalld-zone)
    - [Blocking ICMP](#blocking-icmp)
    - [Using panic mode](#using-panic-mode)
    - [Logging dropped packets](#logging-dropped-packets)
    - [Using firewalld rich language rules](#using-firewalld-rich-language-rules)
    - [Looking at iptables rules in RHEL/CentOS 7 firewalld](#looking-at-iptables-rules-in-rhelcentos-7-firewalld)
    - [Creating direct rules in RHEL/CentOS 7 firewalld](#creating-direct-rules-in-rhelcentos-7-firewalld)
    - [Looking at nftables rules in RHEL/CentOS 8 firewalld](#looking-at-nftables-rules-in-rhelcentos-8-firewalld)
    - [Creating direct rules in RHEL/CentOS 8 firewalld](#creating-direct-rules-in-rhelcentos-8-firewalld)
    - [Hands-on lab for firewalld commands](#hands-on-lab-for-firewalld-commands)


## Technical requirements

The code files are available [here](https://github.com/PacktPublishing/Mastering-Linux-Security-and-Hardening-Second-Edition)

## nftables – a more universal type of firewall system

 - Benefit of `nftables`
    - The `nft` utility is now the only needed firewall utility 
    - Create multi-dimensional trees to display rulesets to troubleshoot vastly easier
    - Having the filter, NAT, mangle, and security tables installed by default
    - Only creating the tables intending to use that enhance performance
    - Specify multiple actions in one rule
    - New rules get added atomically
    - Having its built-in scripting engine that make scripts more efficient and more human-readable
    - Can install a set of utilities to convert them into `nftables` format
  - `sudo nft -v` to check version of `nftables`

## Learning about nftables tables and chains

 - `Tables`: Tables in `nftables` refer to a particular protocol family
 - `Chains`: Chains in `nftables` roughly equate to tables in iptables

### Getting started with nftables

 - Install `nftables` on Ubuntu: `sudo apt install nftables`
 - List all tables `sudo nft list tables`

#### Configuring nftables on Ubuntu 16.04

 - default `nftables.conf` file in the /etc directory

#### Configuring nftables on Ubuntu 18.04

 - Comment in /usr/share/doc/nftables/examples/syntax/workstation file is the same as the old default `nftables.conf` file on Ubuntu 16.04, then copy this file to /etc/nftables.conf (overwrite old `nftables.conf)` with the command `sudo cp /usr/share/doc/nftables/examples/syntax/workstation /etc/nftables.conf`
 - Breakdown in `nftables.conf`:
   - `#!/usr/sbin/nft -f`
   - `flush ruleset`
   - `table inet filter`

### Using nft commands

First, delete the previous configuration and create an inet table for both IPv4 and IPv6 called ubuntu_filter:
```
  sudo nft delete table inet filter
  sudo nft list tables
  sudo nft add table inet ubuntu_filter
  sudo nft list tables
```

Adding an input filter chain to the table

```
  sudo nft add chain inet ubuntu_filter input { type filter hook input priority 0\; policy drop\; }
```

Concerned with the `ip/ip6/inet` families, which have the following hooks:
 - Prerouting
 - Input
 - Forward
 - Output
 - Postrouting

### Hands-on lab for nftables on Ubuntu

```sh
  # Disable ufw on Ubuntu
  sudo systemctl disable --now ufw
  sudo iptables -L
  # Install nftables
  PKG_OK=$(dpkg-query -W --showformat='${Status}\n' nftables | grep "install ok installed")
  echo Checking for nftables: $PKG_OK
  if [ "" = "$PKG_OK" ]; then
    echo "No nftables. Setting up nftables."
    sudo apt-get --yes install nftables;
  fi;

  sudo cp /usr/share/doc/nftables/examples/syntax/workstation /etc/nftables.conf
  
  # View current config file and create backup
  sudo cat /etc/nftables.conf 
  sleep 1
  sudo cp /etc/nftables.conf ~/Backup_nftables.conf

  # Create new config file
  sudo echo -e "#!/usr/sbin/nft -f flush ruleset 
  table inet filter {

    chain prerouting { 
      type filter hook prerouting priority 0; 
      ct state invalid counter log prefix "Invalid Packets: " drop tcp flags & (fin|syn|rst|ack) != syn ct state new 
      counter log prefix "Invalid Packets 2: " drop 
    } 

    chain input {
      type filter hook input priority 0; 
      # accept any localhost traffic
      iif lo accept
      # accept traffic originated from us
      ct state established,related accept
      # activate the following line to accept common
      local services
      tcp dport 22 ip saddr { 192.168.0.7, 192.168.0.10 }
      log prefix "Blocked SSH packets: " drop
      tcp dport { 22, 53 } ct state new accept
      udp dport 53 ct state new accept
      ct state new,related,established icmp type {
      destination-unreachable, time-exceeded, parameter-problem } accept
    } 

    chain forward { 
      type filter hook forward priority 0; 
    } 

    chain output { 
      type filter hook output priority 0; 
    } 

  }" > /etc/nftables.conf 

  # Apply changes
  sudo systemctl reload nftables
  sudo nft list tables
  sudo nft list tables
  sudo nft list table inet filter
  sudo nft list ruleset

```

---

## firewalld for Red Hat systems

- RHEL/CentOS 7, firewalld uses the iptables engine as its backend but On RHEL/CentOS 8 firewalld uses nftables as its backend
- firewalld is dynamically managed so that user can change the firewall configuration without restarting the firewall service, and without interrupting any existing connections to the server

### Verifying the status of firewalld

`sudo firewall-cmd --state` or `sudo systemctl status firewalld` check state/service firewall

### Working with firewalld zones

 - In /usr/lib/firewalld/zones directory of the CentOS machine, you'll see the zones files, all in .xml format including specifies which ports are to be open and which ones are to be blocked for various given scenarios
 - `firewall-cmd` utility is what you would use to configure firewalld
 - `sudo firewall-cmd --list-all-zones` list all zone

### Adding services to a firewalld zone

 - The services files are in the /usr/lib/firewalld/services directory
 - Open specific ports to run services
  
### Adding ports to a firewalld zone

 - `sudo firewall-cmd --add-port=10000/tcp` open port `10000/tcp`
 - `sudo firewall-cmd --runtime-to-permanent` make all permanent at once by typing

### Blocking ICMP

 - `sudo firewall-cmd --query-icmp-block=host-redirect` see if blocking any specific ICMP packets
 - `sudo firewall-cmd --add-icmp-block=host-redirect` block host-redirect packets
 - `sudo firewall-cmd --add-icmp-block={host-redirect,network-redirect}` block host-redirect and network-redirect packets

### Using panic mode

 - Panic mode cuts off all network communications
 - `sudo firewall-cmd --panic-on` turn on panic mode
 - `sudo firewall-cmd --query-panic` check status panic mode

### Logging dropped packets

 - `sudo firewall-cmd --get-log-denied` check status
 - `sudo firewall-cmd --set-log-denied=all` deny all type of log
 - `sudo firewall-cmd --set-log-denied=multicast` deny only log of multicast (multicast
 can be changed to unicast, or broadcast)

### Using firewalld rich language rules

 - For general use scenarios, but for more granular control
 - Example: `sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="200.192.0.024" service name="http" drop'`


### Looking at iptables rules in RHEL/CentOS 7 firewalld

 - `iptables -L` view the active rules
 - /usr/lib/python2.7/site-packages/firewall/core/ directory is a set of Python scripts that set up the initial default firewall

### Creating direct rules in RHEL/CentOS 7 firewalld

`firewall-cmd` commands on RHEL/CentOS 7, firewalld automatically translates those commands into iptables rules and inserts them into the proper place

### Looking at nftables rules in RHEL/CentOS 8 firewalld

Default rules in the /usr/lib/python3.6/site-packages/firewall/core/nftables.py script, which runs every time you boot up the machine

### Creating direct rules in RHEL/CentOS 8 firewalld

There's nothing about this in the Red Hat 8 documentation, but there is the firewalld.direct man page 

### Hands-on lab for firewalld commands

```sh
  #!/bin/bash

  # Setup zones
  sudo firewall-cmd --get-zones
  sudo firewall-cmd --get-default-zone
  sudo firewall-cmd --get-active-zones

  man firewalld.zones
  man firewalld.zone

  # Get details and allow some services and ports
  sudo firewall-cmd --list-all-zones
  sudo firewall-cmd --get-services
  sudo firewall-cmd --info-service=dropbox-lansync 

  sudo firewall-cmd --permanent --set-default-zone=dmz
  sudo firewall-cmd --permanent --add-service={http,https}
  sudo firewall-cmd --info-zone=dmz
  sudo firewall-cmd --permanent --info-zone=dmz

  sudo firewall-cmd --reload
  sudo firewall-cmd --info-zone=dmz
  sudo firewall-cmd --list-services

  sudo firewall-cmd --permanent --add-port=10000/tcp
  sudo firewall-cmd --list-ports
  sudo firewall-cmd --reload
  sudo firewall-cmd --list-ports
  sudo firewall-cmd --info-zone=dmz

  sudo firewall-cmd --permanent --remove-port=10000/tcp
  sudo firewall-cmd --reload
  sudo firewall-cmd --list-ports
  sudo firewall-cmd --info-zone=dmz

  sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="200.192.0.0/24" service name="http" drop'
  sudo firewall-cmd --add-icmp-block={host-redirect,network-redirect}
  sudo firewall-cmd --set-log-denied=all

  sudo firewall-cmd --info-zone=public
  sudo firewall-cmd --info-zone=public --permanent

  sudo firewall-cmd --runtime-to-permanent
  sudo firewall-cmd --info-zone=public --permanent

  # View changes
  sudo iptables -L
  sudo nft list ruleset

  # Set new rules
  sudo firewall-cmd --direct --add-rule ipv4 mangle PREROUTING 0 -m conntrack --ctstate INVALID -j DROP
  sudo firewall-cmd --direct --add-rule ipv4 mangle PREROUTING 1 -p tcp ! --syn -m conntrack --ctstate NEW -j DROP
  sudo firewall-cmd --direct --add-rule ipv6 mangle PREROUTING 0 -m conntrack --ctstate INVALID -j DROP
  sudo firewall-cmd --direct --add-rule ipv6 mangle PREROUTING 1 -p tcp ! --syn -m conntrack --ctstate NEW -j DROP

  sudo firewall-cmd --direct --get-rules ipv4 mangle PREROUTING
  sudo firewall-cmd --direct --get-rules ipv6 mangle PREROUTING
  sudo firewall-cmd --runtime-to-permanent

  sudo less /etc/firewalld/direct.xml

  apropos firewall
```






