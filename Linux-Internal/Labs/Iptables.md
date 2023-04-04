# Setup iptables to prevent some attack method

Work at layer 3 OSI (aka Network layer) 

## Table of content

- [Setup iptables to prevent some attack method](#setup-iptables-to-prevent-some-attack-method)
  - [Table of content](#table-of-content)
  - [Prepare](#prepare)
  - [Proceed](#proceed)
    - [Scanning](#scanning)
      - [Null scan](#null-scan)
      - [XMAS scan](#xmas-scan)
    - [DDoS](#ddos)
      - [ICMP flood](#icmp-flood)
      - [UDP flood](#udp-flood)
    - [Other attack](#other-attack)
---

## Prepare

Goal: config iptables rules to prevent Null, Xmass, FIN, ACK, SYN SCAN AND TCP CONNECT, UDP SCAN, and ICMP FLOOD, UDP FLOOD, SYN FLOOD

*Note:* Reset `iptables` (accept all) `iptables -F` and this [tool](https://explainshell.com/) helps understand rules quickly 

Setup environment:
 - Using 2 virtual machines for the client (Debian/Ubuntu) and the attacker (Kali Linux) 
 - The IP address of the attacker and client: `192.168.220.132` and `192.168.220.134`

## Proceed

### Scanning

#### Null scan

The attacker sends a packet to the target without any flags set within it. If the target responds with an RST packet, this means the port is closed on the device else the port is opened

Test without rules: `sudo nmap -sN 192.168.220.134` and it shows port `22/tcp` is opened

![](https://i.ibb.co/x8k42tW/Screenshot-2023-03-10-082116.png)

Apply these rules to the client:

```sh
    # Log attack
    sudo iptables -A INPUT -p tcp --tcp-flags ALL NONE -m limit --limit 3/m --limit-burst 5 -j LOG --log-prefix "Detect Null scan: "

    # Drop and blacklist for 60 seconds IP of attacker
    sudo iptables -A INPUT -p tcp --tcp-flags ALL NONE -m recent --name blacklist_60 --set -m comment --comment "Drop/Blacklist Null scan: " -j DROP  
```
Test with rules, seems `nmap` can not detect port `22/tcp`

![](https://i.ibb.co/X8RXdPR/Screenshot-2023-03-10-083644.png)

Check logs to verify and determine the attacker `sudo cat /var/log/syslog | grep Null`

![](https://i.ibb.co/JscBw9v/Screenshot-2023-03-10-090321.png)

#### XMAS scan

Sets the FIN, PSH, and URG flags, lighting the packet up like a Christmas tree to identify listening ports on a targeted system will send a specific packet

Test without rules: `sudo nmap -sX 192.168.220.134` and it shows port `22/tcp` is opened


![](https://i.ibb.co/3T41VXd/Screenshot-2023-03-10-092451.png)

Apply these rules to the client:

```sh
    # Log attacks
    sudo iptables -A INPUT -p tcp --tcp-flags ALL FIN,PSH,URG -m limit --limit 3/m --limit-burst 5 -j LOG --log-prefix "Detect XMAS scan: "
    sudo iptables -A INPUT -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -m limit --limit 3/m --limit-burst 5 -j LOG --log-prefix "Detect XMAS-PSH scan: "
    sudo iptables -A INPUT -p tcp --tcp-flags ALL ALL -m limit --limit 3/m --limit-burst 5 -j LOG --log-prefix "Detect XMAS-ALL scan: "

    # Drop and blacklist for 60 seconds IP of attacker
    sudo iptables -A INPUT -p tcp --tcp-flags ALL SYN,RST,ACK,FIN,URG -m recent --name blacklist_60 --set -m comment --comment "Drop/Blacklist Xmas/PSH scan" -j DROP 
    sudo iptables -A INPUT -p tcp --tcp-flags ALL FIN,PSH,URG -m recent --name blacklist_60 --set -m comment --comment "Drop/Blacklist Xmas scan" -j DROP 
    sudo iptables -A INPUT -p tcp --tcp-flags ALL ALL -m recent --name blacklist_60 --set -m comment --comment "Drop/Blacklist Xmas/All scan" -j DROP 
```

Test with rules, seems `nmap` can not detect port `22/tcp`

![](https://i.ibb.co/jLk5CBw/Screenshot-2023-03-10-094005.png)

Check logs to verify and determine the attacker `sudo cat /var/log/syslog | grep XMASS`

![](https://i.ibb.co/23XbdMN/Screenshot-2023-03-10-095028.png)

---

### DDoS

#### ICMP flood

Send a maximum ICMP data to a machine in the minimum amount of time

Test on attacker without rules: `sudo hping3 -q -n -a 10.0.0.1 --id 0 --icmp -d 56 --flood 192.168.220.134` and client using `sudo tcpdump -nni ens33 icmp` to capture icmp packets on ens33 interface

Attacker:

![](https://i.ibb.co/bmt23xf/Screenshot-2023-03-10-101136.png)

Client:

![](https://i.ibb.co/Ns5rGPB/Screenshot-2023-03-10-100840.png)

Apply these rules to the client:

```sh
  # Create chain dedicated to ICMP flood
  sudo iptables -N icmp-flood
  # Jump to that chain when ICMP detected
  sudo iptables -A INPUT -p icmp -j icmp-flood
  # Get out of chain if packet rate for the same IP is below 4 per second with a burst of 8 per second
  sudo iptables -A icmp-flood -m limit --limit 4/s --limit-burst 8 -m comment --comment "Limit ICMP rate" -j RETURN
  # Log as flood when rate is higher
  sudo iptables -A icmp-flood -m limit --limit 6/h --limit-burst 1 -j LOG --log-prefix "Detect icmp flood: "
  # Blacklist IP for 3 minutes
  sudo iptables -A icmp-flood -m recent --name blacklist_180 --set -m comment --comment "Blacklist source IP" -j DROP
```

Check logs to verify and determine the attacker `sudo cat /var/log/syslog | grep icmp`

![](https://i.ibb.co/znCp1Cz/Screenshot-2023-03-10-101839.png)

#### UDP flood

Same concept as in ICMP flood except that you send a huge amount of UDP data

Test on attacker without rules: `sudo hping3 -q -n -a 10.0.0.1 --udp -s 53 --keep -p 68 --flood 192.168.220.134` and client using `sudo tcpdump -nni ens33 udp` to capture SYN packets on ens33 interface

Attacker:

![](https://i.ibb.co/tJWH2gW/Screenshot-2023-03-10-102704.png)

Client:

![](https://i.ibb.co/c6br4HN/Screenshot-2023-03-10-102829.png)

Apply these rules to the client:

```sh
  # Create chain for UDP flood
  sudo iptables -N udp-flood
  # Jump to chain if UDP
  sudo iptables -A INPUT -p udp -j udp-flood
  # Limit UDP rate to 10/sec with burst at 20
  sudo iptables -A udp-flood -m limit --limit 10/s --limit-burst 20 -m comment --comment "Limit UDP rate" -j RETURN

  # Save Log
  sudo iptables -A udp-flood -m limit --limit 6/h --limit-burst 1 -j LOG --log-prefix "Detect udp flood: "
  # 3 minutes ban for flooders
  sudo iptables -A udp-flood -m recent --name blacklist_180 --set -m comment --comment "Blacklist source IP" -j DROP
```

Check logs to verify and determine the attacker `sudo cat /var/log/syslog | grep udp`

![](https://i.ibb.co/7bFqtfb/Screenshot-2023-03-10-103622.png)

---

### Other attack

Used to prevent some specific attack with signature-based method. Some examples of this technique:

For SQLi

![](https://i.ibb.co/g4p071q/Screenshot-2023-04-04-091745.png)

```sh
  # Create chain for SQLi
  sudo iptables -N sql-injection
  # Jump to chain 
  sudo iptables -A INPUT --dport 0:65535 -j sql-injection
  # Drop packet including content: ' or '1'='1
  sudo iptables -A sql-injection -m string --string %27%20or%20%271%27%3D%271 -j DROP 
```
