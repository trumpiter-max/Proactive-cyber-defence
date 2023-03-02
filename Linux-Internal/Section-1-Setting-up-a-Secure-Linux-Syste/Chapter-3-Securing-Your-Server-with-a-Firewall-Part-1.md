# Chapter 3: Securing Your Server with a Firewall - Part 1

 - The `demilitarized zone (DMZ)` where your internet-facing servers are kept
 - The major command-line firewall interfaces, ranging from `iptables` to the new kid on the block, `nftables`

## Table of content

## Technical requirements

The code of this chapter can be found [here](https://github.com/PacktPublishing/Mastering-Linux-Security-and-Hardening-Second-Edition)

## An overview of firewalld

Some examples in a typical business setting encounter various types of firewalld in various places:
 - Edge devices that separate the internet from an internal network translate routable public IP addresses to non-routable private IP addresses
 - Large enterprise networks are normally divided into subnetworks, or subnets, with each corporate department having a subnet to call its own
 - Configured to prevent certain types of port scanning and `denial-of-service (DoS)` attacks

## An overview of iptables

 - Advantages:
     - Long enough that most Linux admins already know how to use
     - Easy to use, create custom firewall configuration in the shell script
     - Flexibility, set up a simple port filter, a router, or a virtual private network
     - Pre-installed on pretty much every Linux distro
     - well & free documents
 - Disadvantages:
     - IPv4 and IPv6 each require their special implementation of iptables
     - Require `ebtables` having unique syntax for MAC bridging
     - `arptables` require their daemon and syntax
     - The entire `iptables` ruleset has to be reloaded which impact on performance after adding new rules
 - Ubuntu comes with `Uncomplicated Firewall (ufw)` which is easy to use frontend for iptables
 - `nftables` has replaced `iptables` as the default backend for firewalld on Red Hat 8/CentOS 8 systems

## Mastering the basics of iptables

 - Five tables of rules:
     - Filter table: protect server & clients
         - Consist of the `INPUT`, `FORWARD`, and `OUTPUT` chains 
     - Network Address Translation (NAT) table: connect the public internet to private networks
     - Mangle table: alter network packets through the firewall
     - Raw table: for packets not require connection tracking
     - Security table: only used for `SELinux`
 - `sudo iptables -L` to see current configuration IPv4, and `sudo ip6tables -L` for IPv6
 - Example for allow users to pass incoming packets from servers `sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT`

## Blocking ICMP with iptables

 - Blocking `Internet Control Message Protocol (ICMP)` makes server invisible to hackers by blocking ping packets and there are some vulnerabilities that are associated with ICMP:
     - By using a botnet, hackers could inundate server with ping packets from multiple sources at once, exhausting server's ability to cope
     - Certain vulnerabilities that are associated with the ICMP protocol can allow a hacker to either gain administrative privileges on the system, redirect your traffic to a malicious server, or crash your operating system 
     - By using some simple hacking tools, someone could embed sensitive data in the data field of an ICMP packet to secretly exfiltrate it from organization