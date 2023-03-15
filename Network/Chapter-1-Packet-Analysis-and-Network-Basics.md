# Chapter 1: Packet Analysis and Network Basics

## Table of contents

- [Chapter 1: Packet Analysis and Network Basics](#chapter-1-packet-analysis-and-network-basics)
  - [Table of contents](#table-of-contents)
  - [Packet Analysis and Packet Sniffers](#packet-analysis-and-packet-sniffers)
    - [Evaluating a Packet Sniffer](#evaluating-a-packet-sniffer)
    - [How Packet Sniffers Works](#how-packet-sniffers-works)
    - [How Computers Communicate](#how-computers-communicate)
    - [Traffic Classifications](#traffic-classifications)

---

## Packet Analysis and Packet Sniffers

Capturing and interpreting live data as it flows across a network to understand what is happening on that network 

### Evaluating a Packet Sniffer

Selection factors:
- Supported protocols
- User-friendliness
- Cost
- Program support
- Operating system support

### How Packet Sniffers Works

Three main steps:
- Collection: listen to all traffic on a network segment in `promiscuous mode` (aka monitor mode wifi)
- Conversion: the network data is in a form that can be interpreted 
only on a very basic level
- Analysis: verifies protocol, and analysis of that protocol’s specific features

### How Computers Communicate

- Protocols are sets of common languages
- The Seven-Layer OSI Model makes it much easier to understand network communication. The application layer at the top represents the actual programs used to access network resources
- Data Encapsulation adds a header or footer—extra bits of information that allow the layers to communicate—to the data being communicated
- Network Hardware includes hubs, switches, and routers

### Traffic Classifications

- Broadcast Traffic sends to all ports on a network segment
- Multicast Traffic transmits a packet from a single source to multiple 
destinations simultaneously
- Unicast Traffic is transmitted from one computer directly to another