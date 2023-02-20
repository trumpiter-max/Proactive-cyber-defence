# Network

Including windows `networking software` components and the `Open Systems 
Interconnection (OSI)` reference model

`Windows Networking Architectures`
- The goal of network software is to take a request among machines in the network
- Requests must be altered for transmission across a network
- Requests  must be checked for completeness, decoded, and sent to the correct operating system (OS) component for execution

## Table of content
- [The OSI Reference Mode](#the-osi-reference-model)
- [Windows Networking Components](#windows-networking-components)

---

## The OSI Reference Model

A *software model* for sending 
messages between machines, including 7 layers as the below graph, provide services to higher layers and abstract how the services are implemented at lower layers

![](https://i.ibb.co/JzMCVWV/Screenshot-2023-02-20-095447.png)

Description for per layers :
- `Layer 7 - Application`: 
    - Handling the information transfer between two network applications
    - Used by two communicating applications, and is application specific

- `Layer 6 - Presentation`:
    - Responsible for preserving the information content of data sent over the network
    - Handling data formatting, including issues

- `Layer 5 - Session`:
    - Implementing a *connection* (own address aka `port`) or *pipe* between cooperating applications
    - Providing communications:
        - two-way simultaneous (full-duplex)
        - two-way alternate (single-duplex)
        - one-way

- `Layer 4 - Transport`:
    - Providing a transparent data-transfer mechanism between end nodes
    - Providing *reliable data* transfer and will re-transmit lost or corrupted *packets* to ensure that the data stream received is identical to the data stream that was sent

- `Layer 3 - Network`: 
    - Implementing node addresses and routing functions to allow 
packets to traverse multiple `datalinks`
    - Understand the network topology, and know how to direct packets to the nearest router

- `Layer 2 - Datalink`:
    - Exchanges `data frames` (aka `packets`) between physically adjacent network entities (known as stations) 
    - Provides each station with its unique address on the network, and provides `point-to-point` communications 
    - Divided into 2 sublayers: 
        - `Logical Link Control (LLC)`: provides a single access method for the network layer to communicate with any 
`802.x MAC`
        - `Medium Access Control (MAC)`: provides 
access-control functions to the shared network medium, and it specifies signaling, the sharing 
protocol, address recognition, frame generation, CRC generation, and so on

- `Layer 1 - Physics` (aka node): 
    - Exchanges signals between cooperating network entities over some physical medium 
    - Specifying the mechanical, electrical, functional, and procedural standards 

---

## Windows Networking Components

- `Networking APIs`: `protocol-independent` way for applications to communicate across 
a network in user mode or both user & kernel mode, see details at [here](https://blogs.windows.com/windowsdeveloper/2015/07/02/networking-api-improvements-in-windows-10/)

- `Transport Driver Interface (TDI) clients` are legacy kernel-mode. TDI interface is deprecated and will be removed in a future version of Windows. Kernel-mode network 
clients should now use the `Winsock Kernel (WSK)` interface

- `TDI transports` (also known as transports) and `Network Driver Interface Specification (NDIS)` 
protocol drivers (or protocol drivers) 
    - Are kernel-mode network protocol drivers
    - Adding protocol-specific headers (for example, TCP, UDP, and/or IP) to data passed in the IRP, and to communicate with adapter drivers using NDIS functions (also documented in the Windows Driver Kit)
- The interface between the `TCP/IP` protocol driver and Winsock is known as the `Transport Layer Network Provider Interface (TLNPI)`

- `Winsock Kernel (WSK)` is a transport-independent, kernel-mode networking API that replaces 
the legacy TDI

- The Windows Filtering Platform (WFP) ) is a set of APIs and system services that provide the 
ability to create network filtering applications

![cu be](https://i.ibb.co/xjvsnnv/giphy.gif)