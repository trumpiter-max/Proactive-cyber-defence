# Chapter 6: Common Lower-Layer Protocols

## Table of contents

- [Chapter 6: Common Lower-Layer Protocols](#chapter-6-common-lower-layer-protocols)
  - [Table of contents](#table-of-contents)
  - [Address Resolution Protocol](#address-resolution-protocol)
    - [The ARP Header](#the-arp-header)
  - [Internet Protocol](#internet-protocol)
    - [IP Addresses](#ip-addresses)
    - [The IPv4 Header](#the-ipv4-header)
    - [Time to Live](#time-to-live)
    - [IP Fragmentation](#ip-fragmentation)
  - [Transmission Control Protocol](#transmission-control-protocol)
    - [The TCP Header](#the-tcp-header)
    - [TCP Ports](#tcp-ports)
    - [The TCP Three-Way Handshake](#the-tcp-three-way-handshake)
    - [TCP Teardown](#tcp-teardown)
    - [TCP Resets](#tcp-resets)
  - [User Datagram Protocol](#user-datagram-protocol)
    - [The UDP Header](#the-udp-header)
  - [Internet Control Message Protocol](#internet-control-message-protocol)
    - [The ICMP Header](#the-icmp-header)
    - [ICMP Types and Messages](#icmp-types-and-messages)
    - [Echo Requests and Responses](#echo-requests-and-responses)
    - [Traceroute](#traceroute)

## Address Resolution Protocol

- MAC addresses are needed because a switch that interconnects devices on a network uses a `Content Addressable Memory (CAM)` table
- The resolution process that TCP/IP networking (with IPv4) uses to resolve an IP address to a MAC address is called the `Address Resolution Protocol (ARP)`

### The ARP Header

- Includes the following fields
  - Hardware Type (layer 2)
  - Protocol Type
  - Hardware Address Length
  - Protocol Address Length
  - Operation
  - Sender Hardware Address
  - Sender Protocol Address
  - Target Hardware Address
  - Target Protocol Address

- Gratuitous ARP packet is transmitted on the network to force any device to prevent this from causing communication errors

## Internet Protocol

IPv4 is the workhorse of the communication 
process and is ultimately responsible for carrying data between devices

### IP Addresses

- Is 32-bit address to identify unique devices connected to a network
- Consists of two parts: a network address and a host address
- Determined by another set of addressing information which portion of the IP address belongs to the network address and which part belongs to the host address called the `network mask (netmask)`, also referred to as `subnet mask`
- IP addresses and netmasks are commonly written in `Classless Inter-Domain Routing (CIDR)` notation for shorthand includes forward slash (/) and the number of bits that represent the network portion of the IP address

### The IPv4 Header

![](https://i.ibb.co/QvyD1T8/Screenshot-2023-03-20-154330.png)

### Time to Live

- Define a period of time that can be elapsed or a maximum number of routers a packet can traverse before the packet is discarded
- Is safe to assume that one routing device 
will decrement a TTL by only 1 most of the time
- Encounter a misconfigured router and lose the path to its final destination
- Create TTL field to prevent number of looping packets

### IP Fragmentation

- Permit reliable delivery of data across varying types of networks by splitting a data stream into smaller fragments
- Based on the `maximum transmission unit   (MTU)` - the largest packet or frame size
- Fragmenting a packet involves the following steps:
  - Device splits the data into multiple packets
  - Total Length field of each IP header is set each fragment
  - More Fragments flag is set to 1 on all packets except last one
  - Fragment Offset field is set in the IP header
  - Transmitted packets

## Transmission Control Protocol

TCP provides end-to-end reliability for the delivery of data with built-in error checking

### The TCP Header

![](https://i.ibb.co/mbxz4ty/Screenshot-2023-03-20-160157.png)

### TCP Ports

- Every call needed to have a source port (the caller) and a 
destination port (the recipient)
- Divide into two groups
  - The `standard port` group is from 1 through 1023
  - The `ephemeral port` group is from 1024 through 65535
- All TCP-based communication works the same way: a random source port is chosen to communicate to a known destination port

### The TCP Three-Way Handshake

Serve a few different purposes:
- Ensure that the destination host is up 
and able to communicate
- Check that it is listening on the port on which the source is attempting to communicate
- Both hosts can keep the stream of packets in proper sequence

![](https://i.ibb.co/jhX2rvx/Screenshot-2023-03-20-163242.png)

### TCP Teardown

Used to gracefully end a connection between two devices with `FIN` flag

![](https://i.ibb.co/31VyDWD/Screenshot-2023-03-20-163830.png)

### TCP Resets

`RST` flag is used to indicate a connection was closed abruptly or to refuse a connection attempt

## User Datagram Protocol

UDP aims to provide speedy transmission, is best-effort service, commonly referred to as a connectionless protocol

### The UDP Header

![](https://i.ibb.co/68ZBfHT/Screenshot-2023-03-20-164413.png)

## Internet Control Message Protocol

ICMP is the utility protocol of TCP/IP, 
responsible for providing information regarding the availability of devices, 
services, or routes on a TCP/IP network

### The ICMP Header

![](https://i.ibb.co/ThScWRF/Screenshot-2023-03-20-164942.png)

### ICMP Types and Messages

Defined by the values in the Type and Code fields, details at [here](http://www.iana.org/assignments/icmp-parameters)

### Echo Requests and Responses

- Ping is used to test for connectivity to a device
- Providing a summary detailing how many packets were sent, received, and lost

![](https://i.ibb.co/4mS0T1Z/Screenshot-2023-03-20-165455.png)

### Traceroute

Used to identify the path from one device to another