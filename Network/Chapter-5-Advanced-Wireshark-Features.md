# Chapter 5: Advanced Wireshark Features

## Table of contents

- [Chapter 5: Advanced Wireshark Features](#chapter-5-advanced-wireshark-features)
  - [Table of contents](#table-of-contents)
  - [Network Endpoints and Conversations](#network-endpoints-and-conversations)
  - [Name Resolution](#name-resolution)
  - [Protocol Dissection](#protocol-dissection)
  - [Following TCP Streams](#following-tcp-streams)
  - [Packet Lengths](#packet-lengths)
  - [Graphing](#graphing)
    - [Viewing IO Graphs](#viewing-io-graphs)
    - [Round-Trip Time Graphing](#round-trip-time-graphing)
    - [Flow Graphing](#flow-graphing)
  - [Expert Information](#expert-information)

## Network Endpoints and Conversations

- `Endpoint` is a device that sends or receives data on the network
- `Conversation` describes the communication that takes place between two hosts (endpoints) on a network
- Viewing Endpoints (Statistics/Endpoints)
- Viewing Network Conversations (Statistics/Conversations)
- Troubleshooting with the Endpoints and Conversations Windows 
  - Using whois to find what IP address belong
  - Conversations window with IPv4 tab, able to indeed verify this by sorting the list by bytes 
- Protocol Hierarchy Statistics (Statistics/Protocol Hierarchy)
  - Giving a good snapshot of the type of activity occurring on a network  

## Name Resolution
- Name resolution (aka name lookup) is the process a protocol uses to convert one identifying address into another
- Enabling Name Resolution (Capture/Options)
- Potential Drawbacks to Name Resolution
  - Can fail
  - Take place every time
  - Generate additional packets

## Protocol Dissection

- Changing the Dissector
  - Right-click one of the SSL packets and select `Decode As`
  - Decode all TCP source port 443 traffic by selecting destination (443) and FTP
- Viewing Dissector Source Code
  - Can be found in the `epan/dissectors` folder
  - Each dissector is labeled with `packets-protocolname.c` 

## Following TCP Streams

Click any of the TCP or HTTP packets in the file, right-click the file, and choose Follow TCP Stream

## Packet Lengths

- Open at `Statistics/Packet Lengths`
- The maximum size of a frame on an Ethernet network is 1518 bytes
- TCP headers are 1460 bytes when subtracting the Ethernet
- TCP packet with no data or options is also 20 bytes, TCP control packets will be around 54 bytes in size 
- The Ethernet header is 14 bytes (plus a 4-byte CRC)
- The IP header is a minimum of 20 bytes

## Graphing

### Viewing IO Graphs

- Open at `Statistics/IO Graphs`
- Using to visualize and compare the throughput of data on a network

### Round-Trip Time Graphing

- Open at `Statistics/TCP/Stream Graph/Round Trip Time Graph`
- `Fast download` has RTT values mostly under 0.05 seconds, a few slower points between 0.10 and 0.25 seconds

### Flow Graphing

- Open at `Statistics/Flow Graph`
- Visualizing connections and showing the flow of data over time

## Expert Information

- States of the packet are separated into four categories:
  - Chat: normal packets
  - Note: unusual packets of normal communication
  - Warning: unusual packets of anomaly communication 
  - Error: error packets

- Flag an individual packet when it meets certain criteria
  - Chat messages
  - Note messages
  - Warning messages
  - Error messages

