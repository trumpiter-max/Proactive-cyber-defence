# DDoS Prevention

## Table of contents

- [DDoS Prevention](#ddos-prevention)
  - [Table of contents](#table-of-contents)
  - [Reasons](#reasons)
  - [Types](#types)
    - [Application layer attacks](#application-layer-attacks)
    - [Protocol attacks](#protocol-attacks)
    - [Volumetric attacks](#volumetric-attacks)
  - [Usual DDoS symptoms](#usual-ddos-symptoms)
  - [Responding to a DDoS attack](#responding-to-a-ddos-attack)
  - [How to prevent](#how-to-prevent)

## Reasons

- `Ransomwares` are usually be demanded after conducting DDoS attacks
- `Hacktivism` is used to voice opinion to support or opposition to a regulation, person, or company
- `Competition` of cyber criminal enterprises, gangs, and syndicates

## Types

### Application layer attacks

Such as `HTTP flood attack` in which malicious actors just keep sending various HTTP requests to a server using different IP addresses

![](https://www.onelogin.com/images/patterns/text-image/ddos-app-layer-attack.png)

### Protocol attacks

Such as `SYN flood attack`, the attacker floods the server with numerous SYN packets, each containing spoofed IP addresses. The server responds to each packet (via SYN-ACKs), requesting the client to complete the handshake

![](https://www.onelogin.com/images/patterns/text-image/ddos-protocol-attack.png)

### Volumetric attacks

Such as `DNS amplification attack`, a malicious actor sends requests to a DNS server, using the spoofed IP address of the target. The DNS server then sends its response to the target server. When done at scale, the deluge of DNS responses can wreak havoc on the target server

![](https://www.onelogin.com/images/patterns/text-image/ddos-volumetric-attack.png)

## Usual DDoS symptoms

- Large amounts of traffic coming from clients with same or similar characteristics
- An exponential, unexpected rise in traffic at a single endpoint/server
- A server starts repeatedly crashing for no reason
- The website is taking too long to respond to requests

## Responding to a DDoS attack

- `Blackhole filtering` makes criterion to route malicious traffic into a blackhole, essentially dropping it
- `Casting` distributes the traffic across multiple servers, increasing your capacity, and decreasing the chances of individual servers getting overwhelmed
- `IP Blocking` blocks unexpectedly high traffic from the same range of IP addresse

## How to prevent

- Real-time packet analysis
- DDoS defense system (DDS)
- Web application firewall (WAF)
- Rate limiting

