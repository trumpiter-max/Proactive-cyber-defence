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
- [Network APIs](#network-apis)
    - [Windows Sockets](#windows-sockets)
    - [Winsock client operation](#winsock-client-operation)
    - [Winsock server operation](#winsock-server-operation)
    - [Window Extension](#extending-winsock)
    - [Winsock Implementation](#winsock-implementation)
    - [Winsock kernel](#winsock-kernel)
    - [WSK Implementation](#wsk-implementation)
- [Remote Procedure Call](#remote-procedure-call)
    - [RPC Operation](#rpc-operation)
    - [RPC Security](#rpc-security)
    - [RPC Implementation](#rpc-implementation)
- [Web Access APIs](#web-access-apis)
    - [Wininet](#wininet)
    - [Http](#http)
- [Named-pipes and mailslots](#named-pipes-and-mailslots)
    - [Named-Pipe Operation](#named-pipe-operation)
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

- `The Windows Filtering Platform (WFP)` is a set of APIs and system services that provide the ability to create network filtering applications

- `WFP callout drivers` are kernel-mode drivers that implement one or more callouts

- `NDIS library (Ndis.sys)` provides an abstraction mechanism that encapsulates `Network Interface Card (NIC) drivers` (also known as NDIS miniports)

- `NDIS miniport drivers` are kernel-mode drivers that are responsible for interfacing the network stack to a particular NIC

![](https://i.ibb.co/cLq3zsw/Screenshot-2023-02-20-114922.png)

---

## Network APIs

## Windows Sockets

Including most of the functionality of `BSD (Berkeley Software Distribution) Sockets` but also include Microsoft-specific enhancements, there are several features:
- *Scatter-gather* and *asynchronous* application I/O
- *Quality of Service (QoS)* conventions
- Can be used with *third-party* protocols
- Integrated namespaces with *third-party* namespace providers
- Multicast messages

## Winsock Client Operation

The client can send and receive data over its socket using the `recv` and send APIs

## Winsock Server Operation

![](https://i.ibb.co/4WHmsc3/Screenshot-2023-02-21-134143.png)

Servers can use the select and `WSAPoll` functions to query the state of one or more sockets; however, the Winsock `WSAEventSelect` function and overlapped (asynchronous) I/O extensions are preferred for better scalability

## Winsock Extensions

- `AcceptEx` (the Ex suffix is short for Extended): used for establishing connection, return address, and first message of client. It allows servera queue multiple accept 
operations so that high volumes of incoming connection requests can be handled
- `TransmitFile`:  integrated with the `Windows cache manager` so this sending is called *zero-copy* (not require read to send)
- `ConnectEx` establishes a connection and sends the first message on the connection
- `DisconnectEx` closes a connection and allows the socket handle representing the connection to be reused in a call to AcceptEx or ConnectE
- `TransmitPackets` is similar to `TransmitFile`, but sending of in-memory data in addition to, or in lieu of, file data

## Extending Winsock

- Third parties can add a *transport service provider* and *namespace service provider*
- Service providers plug in to Winsock by using the `Winsock service provider interface (SPI)`
- Namespace service providers supply this functionality to Winsock by implementing 
standard Winsock name-resolution functions such as `getaddrinfo` and `getnameinfo`

## Winsock Implementation

Consists of an API DLL:
- `Ws2_32.dll` (%SystemRoot%\System32\Ws2_32.dll): calls on the services of namespace and transport service providers
- `Mswsock.dll` (%SystemRoot%\System32\mswsock.dll): transport service provider for the protocols supported by Microsoft and uses Winsock Helper
libraries that are protocol specific to communicate with kernel-mode protocol drivers
- `Wshtcpip.dll` (%SystemRoot%\System32\wshtcpip.dll) is the TCP/IP helper
- `Mswsock.dll` implements the 
Microsoft Winsock extension functions

![](https://i.ibb.co/gVky5dr/Screenshot-2023-02-21-142429.png)

## Winsock Kernel

- Windows implements a socket-based networking programming interface called Winsock Kernel (WSK) - replaces the legacy `TDI API interface` with better performance, better security, better scalability, and a 
much easier programming paradigm
- Supported full features of `Windows TCP/IP stack``
- Using of the `Network Module Registrar (NMR)` component of Windows (part of %SystemRoot%\System32\drivers\NetIO.sys)
- Support many types of network clients
- Restricting address sharing

## WSK Implementation

- Using the Next Generation TCP/IP Stack (%SystemRoot%\System32\Drivers\Tcpip.sys) and the NetIO support library/ (%SystemRoot%\System32\Drivers\NetIO.sys) but is actually implemented in AFD

![](https://i.ibb.co/zxMdj78/Screenshot-2023-02-21-151753.png)

- `WSK subsystem` defines four kinds of socket categories:
    - Basic sockets: get and set information
    - Listening sockets: accept incoming connections
    - Datagram sockets: sending and receiving datagrams.
    - Connection-oriented sockets
- Providing events through which clients 
are notified of network status

---

## Remote Procedure Call

`Remote procedure call (RPC)` is a network programming standard

## RPC Operation

An RPC facility is one that allows a programmer to create an application consisting of any number of 
procedures, some that execute locally and others that execute on remote computers via a network

![](https://i.ibb.co/rK9JvHc/Screenshot-2023-02-21-153049.png)

## RPC Security

Including integration with `security support providers (SSPs)` so that RPC clients and 
servers can use authenticated or encrypted communications

## RPC Implementation

- RPC-based application links 
with the RPC run-time DLL (%SystemRoot%\System32\Rpcrt4.dll)
-  The RPC subsystem (RPCSS—%SystemRoot%\System32\Rpcss.dll)

![](https://i.ibb.co/88NYT7v/Screenshot-2023-02-21-153442.png)

---

## Web Access APIs

Applications can provide HTTP services and use FTP and HTTP services without knowledge of the intricacie

## WinInet

- WinInet supports the HTTP, FTP, and Gopher protocols
- Using the FTP-related APIs
- WinInet is used by core Windows components 

## HTTP

The HTTP Server API, which applications access through %SystemRoot%\System32\Httpapi.dll, relies on 
the kernel-mode %SystemRoot%\System32\Drivers\Http.sys driver

![](https://i.ibb.co/yf63Sxq/Screenshot-2023-02-21-154551.png)

---

## Named Pipes and Mailslots

## Named-Pipe Operation

![](https://i.ibb.co/njgnywQ/Screenshot-2023-02-21-155720.png)