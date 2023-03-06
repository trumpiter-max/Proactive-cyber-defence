# Chapter 3: Securing Your Server with a Firewall - Part 1

 - The `demilitarized zone (DMZ)` where your internet-facing servers are kept
 - The major command-line firewall interfaces, ranging from `iptables` to the new kid on the block, `nftables`

## Table of content

- [Chapter 3: Securing Your Server with a Firewall - Part 1](#chapter-3-securing-your-server-with-a-firewall---part-1)
  - [Table of content](#table-of-content)
  - [Technical requirements](#technical-requirements)
  - [An overview of firewalld](#an-overview-of-firewalld)
  - [An overview of iptables](#an-overview-of-iptables)
  - [Mastering the basics of iptables](#mastering-the-basics-of-iptables)
  - [Blocking ICMP with iptables](#blocking-icmp-with-iptables)
    - [Blocking everything that isn't allowed with iptables](#blocking-everything-that-isnt-allowed-with-iptables)
    - [Hands-on lab for basic iptables usage](#hands-on-lab-for-basic-iptables-usage)
  - [Blocking invalid packets with iptables](#blocking-invalid-packets-with-iptables)
    - [Restoring the deleted rules](#restoring-the-deleted-rules)
    - [Hands-on lab for blocking invalid IPv4 packets](#hands-on-lab-for-blocking-invalid-ipv4-packets)
  - [Protecting IPv6](#protecting-ipv6)
    - [Hands-on lab for ip6tables](#hands-on-lab-for-ip6tables)
  - [Uncomplicated firewall for Ubuntu systems](#uncomplicated-firewall-for-ubuntu-systems)
    - [Configuring ufw](#configuring-ufw)
    - [Working with the ufw configuration files](#working-with-the-ufw-configuration-files)
    - [Hands-on lab for basic ufw usage](#hands-on-lab-for-basic-ufw-usage)


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
 - `nftables` has replaced `iptables` as the default backend for `firewalld` on Red Hat 8/CentOS 8 systems

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

 - Blocking `Internet Control Message Protocol (ICMP)` makes servers invisible to hackers by blocking ping packets and some vulnerabilities are associated with `ICMP`:
     - By using a botnet, hackers could inundate the server with ping packets from multiple sources at once, exhausting the server's ability to cope
     - Certain vulnerabilities that are associated with the `ICMP` protocol can allow a hacker to either gain administrative privileges on the system, redirect your traffic to a malicious server, or crash your operating system 
     - By using some simple hacking tools, someone could embed sensitive data in the data field of an ICMP packet to secretly exfiltrate it from the organization

### Blocking everything that isn't allowed with iptables

 - Set a default `DROP` or `REJECT` policy for the `INPUT` chain, or leave the policy set to `ACCEPT `and create a `DROP` or `REJECT` rule at the end of the `INPUT` chain
 - The difference between `DROP` and `REJECT`
     - `DROP` blocks packets without sending any message back to the sender
     - `REJECT` blocks packets, and then sends a message back to the sender about why the packets were blocked
 - To make them permanent on an Ubuntu machine is to install the `iptables-persistent` package (won't save subsequent changes to iptables rules)

### Hands-on lab for basic iptables usage

```sh
  # List all rules of iptables
  sudo iptables -L
  sleep 1

  # Add new rules
  sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
  sudo iptables -A INPUT -p tcp --dport ssh -j ACCEPT
  sudo iptables -A INPUT -p tcp --dport 53 -j ACCEPT
  sudo iptables -A INPUT -p udp --dport 53 -j ACCEPT
  sudo iptables -A INPUT -m conntrack -p icmp --icmp-type 3 --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
  sudo iptables -A INPUT -m conntrack -p icmp --icmp-type 11 --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
  sudo iptables -A INPUT -m conntrack -p icmp --icmp-type 12 --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
  sudo iptables -A INPUT -j DROP
  sudo iptables -I INPUT 1 -i lo -j ACCEPT
  sudo iptables -L -v

  PKG_OK=$(dpkg-query -W --showformat='${Status}\n' iptables-persistent | grep "install ok installed")
  echo Checking for iptables-persistent: $PKG_OK
  if [ "" = "$PKG_OK" ]; then
    echo "No iptables-persistent. Setting up iptables-persistent."
    sudo apt-get --yes install iptables-persistent
  fi;
   
```

## Blocking invalid packets with iptables

 - Explanation of TCP three-way handshake
     - The client sends a packet with only the `SYN` flag set to the web server offer making a connection
     - After receiving the `SYN` packet, the web server sends back a packet with the `SYN` and `ACK` flags set to accept the opening connection 
     - Upon receipt of the `SYN-ACK` packet, the client sends back a packet with only the `ACK` flag set to start a connection
     - Upon receipt of the `ACK` packet, the server sets up the connection with the client so that they can exchange information
 - The invalid packets are weird combinations of flags:
     - Used to elicit responses from the target machine to find out what running operating system, services
     - Trigger certain sorts of security vulnerabilities on the target machine 
     - Make them useful for performing DoS attacks

### Restoring the deleted rules

 - `iptables -D` command delete `rules.v4` configuration file
 - To restore the rules, reboot the machine or restart the `netfilter-persistent` service `sudo systemctl restart netfilter-persistent`

### Hands-on lab for blocking invalid IPv4 packets

## Protecting IPv6

 - Protecting IPv6 means doing everything twice
 - Most Linux distros come with IPv6 networking enabled by default, so you either need to protect it with a firewall or disable it 
 - Some examples with `ip6tables` command
 ![](https://i.ibb.co/7kfsR5T/Screenshot-2023-03-02-135303.png)
 - Allow more types of ICMP messages than you need to for IPv4:
     - New types of ICMP messages have replaced the `Address Resolution Protocol (ARP)`
     - Dynamic IP address assignments exchange ICMP discovery messages with other hosts, rather than by DHCP
     - Echo requests and echo replies, the infamous ping packets, are required when users need to tunnel IPv6 packets through an IPv4 network

### Hands-on lab for ip6tables

```sh
  sudo ip6tables -L

  sudo ip6tables -t mangle -A PREROUTING -m conntrack --ctstate INVALID -j DROP
  sudo ip6tables -t mangle -A PREROUTING -p tcp ! --syn -m conntrack --ctstate NEW -j DROP

  sudo ip6tables-save > rules.v6
  sudo cp rules.v6 /etc/iptables/

  ip a

  sudo nmap -6 -sW fe80::a00:27ff:fe9f:d923

  sudo ip6tables -t mangle -L -v

  # Test new iptables rules with nmap
  sudo nmap -6 -sX fe80::a00:27ff:fe9f:d923

  sudo ip6tables -t mangle -L -v

```

## Uncomplicated firewall for Ubuntu systems

 - `ufw` is a simplified set of commands using the iptables service on Ubuntu
 - Automatically configure both
the IPv4 and the IPv6 rules, save time and configure by hand with `iptables` is already there by default
 
### Configuring ufw

 - `sudo systemctl enable --now ufw` to enable `ufw` service
 - `sudo ufw allow 22/tcp` open port 22 to allow it to connect to the machine with Secure Shell
 - Setting up a DNS server, port 53 open for both protocols: `sudo ufw allow 53`

### Working with the ufw configuration files

 - `ufw` firewall rules in the /etc/ufw directory
 - `user6.rules` and `user.rules` files can't be hand-edited. Save the files after editing, then using `sudo ufw reload` to load the new changes
 - Example of opening the DNS ports look like
 ![](https://i.ibb.co/x2vT2NR/Screenshot-2023-03-03-065746.png)
 - These messages get sent to the var/log/kern.log file, 
 - Not overwhelm the logging system by sending three messages per minute to the log file, with a burst rate of 10 messages per minute
 ![](https://i.ibb.co/TMBWQPc/Screenshot-2023-03-03-070159.png)
 - To store rules that will run before the rules in the `user.rules` and `user6.rules` files, using `before.rules` file and the `before6.rules` file and after the rules using `after.rules` file and the `after6.rules` file

### Hands-on lab for basic ufw usage

```sh
  sudo iptables -L

  sudo ufw status
  sudo ufw allow 22/tcp
  sudo ufw enable
  sudo ufw status
  sudo iptables -L
  sudo ip6tables -L

  sudo ufw allow 53
  sudo iptables -L
  sudo ip6tables -L
  sudo ufw status
  
  # Add new rules for user Donnie for both IPv4 & IPv6
  sudo echo -n "# Mangle table added by Donnie /n
                *mangle /n
                :PREROUTING ACCEPT [0:0] /n
                -A PREROUTING -m conntrack --ctstate INVALID -j DROP /n
                -A PREROUTING -p tcp -m tcp ! --tcp-flags FIN,SYN,RST,ACK SYN -m /n
                conntrack --ctstate /n
                NEW -j DROP /n
                COMMIT" >> /etc/ufw/before.rules

  sudo echo -n "# Mangle table added by Donnie /n
                *mangle /n
                :PREROUTING ACCEPT [0:0] /n
                -A PREROUTING -m conntrack --ctstate INVALID -j DROP /n
                -A PREROUTING -p tcp -m tcp ! --tcp-flags FIN,SYN,RST,ACK SYN -m /n
                conntrack --ctstate /n
                NEW -j DROP /n
                COMMIT" >> /etc/ufw/before6.rules

  # Apply changes
  sudo ufw reload

  sudo iptables -L
  sudo iptables -t mangle -L
  sudo ip6tables -L
  sudo ip6tables -t mangle -L

  sudo ufw status

```




