# Chapter 2: Tapping into the Wire

## Tables of contents

- [Chapter 2: Tapping into the Wire](#chapter-2-tapping-into-the-wire)
  - [Tables of contents](#tables-of-contents)
  - [Living Promiscuously](#living-promiscuously)
  - [Sniffing Around Hubs](#sniffing-around-hubs)
  - [Sniffing in a Switched Environment](#sniffing-in-a-switched-environment)
    - [Port Mirroring/Spanning](#port-mirroringspanning)
    - [Hubbing Out](#hubbing-out)
    - [Using a Tap](#using-a-tap)
    - [ARP Cache Poisoning](#arp-cache-poisoning)
      - [The ARP Process](#the-arp-process)
      - [How ARP Cache Poisoning Works](#how-arp-cache-poisoning-works)
    - [Using Cain \& Abel](#using-cain--abel)
    - [A Word of Caution on ARP Cache Poisoning](#a-word-of-caution-on-arp-cache-poisoning)
  - [Sniffing in a Routed Environment](#sniffing-in-a-routed-environment)
  - [Sniffer Placement in Practice](#sniffer-placement-in-practice)

## Living Promiscuously

- `Promiscuous mode` is what allows a NIC to view all packets crossing the wire
- A broadcast domain consists of several computers, but only one client on that domain should be interested in the ARP broadcast packet that is transmitted
- Once the packet makes it to the CPU, it can then be grabbed by a packet-sniffing application for analysis

## Sniffing Around Hubs

- Hub-based networks are pretty rare
- The result may be packet loss and the communicating devices will compensate for that loss by retransmitting packets

## Sniffing in a Switched Environment

### Port Mirroring/Spanning

![](https://i.ibb.co/ScTZ912/Screenshot-2023-03-15-142603.png)

- The easiest way to capture the traffic from a target device on a switched network
- The switch must support port mirroring and have an empty port into which you can plug your sniffer
- Aware of some situations making packet loss or network slowdowns if the traffic reached a certain level

### Hubbing Out

- Capturing the traffic through a target device on a switched network
- Put the target device and your analyzer in the same 
broadcast domain
- Reducing the duplex of the target device from full to half 

### Using a Tap

- Is a hardware device that you can place between two points 
on your cabling system 
- Two primary types of network taps: 
  - Aggregated (three ports) have only one physical monitor 
port for sniffing bidirectional traffic
  ![](https://i.ibb.co/mcL3fq3/Screenshot-2023-03-15-145604.png)
  - Nonaggregated (four ports) have one monitor port for 
sniffing traffic in one direction and another one in another direction
  ![](https://i.ibb.co/n0ykkSS/Screenshot-2023-03-15-150043.png)
- Choosing a Network Tap
  - Aggregated taps are required less cabling and do not need two NICs
  - Nonaggregated taps capture a high volume of traffic or care about traffic going in only one direction

### ARP Cache Poisoning

#### The ARP Process

- The ARP process, for computers connected to Ethernet networks, begins when one computer wishes to communicate with another
- Devices without the destination computer's IP address simply discard 
this ARP request

#### How ARP Cache Poisoning Works
  
- Also known as ARP spoofing is the process of sending ARP messages to an Ethernet switch or router with a fake MAC
- Sending falsely addressed packets to client systems to intercept certain traffic or cause denial-of-service (DoS) attacks on a target
  ![](https://i.ibb.co/PZwV95T/Screenshot-2023-03-15-151328.png)

### Using Cain & Abel

Collect certain information, including the IP address of your analyzer system, the remote system, and the router 

### A Word of Caution on ARP Cache Poisoning

- Aware of the roles of the systems which implement this process such as very high network utilization 
- Rerouting can create a DoS-type effect on the machine being analyzed

## Sniffing in a Routed Environment

- In situations where data must traverse multiple routers, it is important to analyze the traffic on all sides of the route
- A network map, or network diagram, is a diagram that shows all technical 
resources on a network and how they are connected

## Sniffer Placement in Practice

A flowchart is simply a general reference

![](https://i.ibb.co/SBqz4Vn/Screenshot-2023-03-15-153349.png)