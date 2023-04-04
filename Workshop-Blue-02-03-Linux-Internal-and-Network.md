# Workshop-Blue-02-03

## Table of content
- [Workshop-Blue-02-03](#workshop-blue-02-03)
  - [Table of content](#table-of-content)
  - [Linux hardening](#linux-hardening)
    - [Use AppArmor](#use-apparmor)
  - [Deployment snort](#deployment-snort)
    - [Detect and prevent DoS](#detect-and-prevent-dos)
  - [Detect and prevent SQLi](#detect-and-prevent-sqli)
  - [Wireshark - Packet Analysis for Security](#wireshark---packet-analysis-for-security)
    - [ARP cache poisoning](#arp-cache-poisoning)
    - [Session Hijacking](#session-hijacking)
    - [Operation Aurora](#operation-aurora)
    - [Remote Access Trojan](#remote-access-trojan)
  




## Linux hardening

### Use AppArmor
[What is AppArmor](Linux-Internal\Section-3-Advanced-System-Hardening-Techniques\Chapter-9-Implementing-Mandatory-Access-Control-with-SELinux-and-AppArmor.md)

Create a policy for a process
- Create a new AppArmor profile for the process (apache2)
  - > sudo aa-genprof /usr/sbin/apache2
- Reload the profile to the kernel
  - > sudo apparmor_parser -r /etc/apparmor.d/usr.sbin.apache2

## Deployment snort
Perform a network attack (Ping of Death, Network Scanning, DoS...) and write a Snort rule for detection.
Snort rule detects abnormal Payload
Perform protected content (Hash) related attack/intrusion and write Snort rules.

### Detect and prevent DoS

- Tool to attack: Slowloris
  - > python3 slowloris.py [website url] -s [number of sockets]
  
Victim: 192.168.4.200 (DVWA)

- Run snort
  - > sudo snort -A console -c /etc/snort/nhom4-snort.conf -Q -i ens37:ens38
  
> alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS 80 (msg:"Potential DoS Attack"; flow:to_server,established; content:"GET"; http_method; depth:4; flowbits:set,dos; threshold:type both, track by_src, count 10, seconds 10; classtype:attempted-dos; sid:1000003; rev:1;)

> drop tcp $EXTERNAL_NET any -> $HTTP_SERVERS 80 (msg:"Possible Slowloris DoS Attack"; flow:stateless; content:"GET"; depth:4; flowbits:set,sloris; threshold:type threshold, track by_src, count 50, seconds 10; sid:1000001; rev:1;)


## Detect and prevent SQLi

- Use DVWA - SQLi low to demo

alert tcp any any -> 192.168.4.200 80 (msg:"SQLi Prevention - UNION Keyword"; flow:established,to_server; content:"UNION"; nocase; content:"SELECT"; nocase; sid:10000005; rev:1;)

## Wireshark - Packet Analysis for Security

### ARP cache poisoning

### Session Hijacking

### Operation Aurora

### Remote Access Trojan





