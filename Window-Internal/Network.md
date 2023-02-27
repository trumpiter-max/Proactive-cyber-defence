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
    - [Mailslot Operation](#mailslot-operation)
    - [Named Pipe and Mailslot Implementation](#named-pipe-and-mailslot-implementation)
- [NetBIOS](#netbios)
    - [NetBIOS names](#netbios-names)
    - [NetBIOS Operation](#netbios-operation)
    - [NetBIOS API Implementation](#netbios-api-implementation)
- [Other Networking APIs](#other-networking-apis)
    - [Background Intelligent Transfer Service](#background-intelligent-transfer-service)
    - [DCOM](#dcom)
    - [Message Queuing](#message-queuing)
    - [UPnP with PnP-X](#upnp-with-pnp-x)
- [Multiple Redirector Support](#multiple-redirector-support)
    - [Multiple Provider Router](#multiple-provider-router)
    - [Multiple UNC Provider](#multiple-unc-provider)
- [Surrogate Providers](#surrogate-providers)
    - [Redirector](#redirector)
    - [Mini-Redirectors](#mini-redirectors)
    - [Server Message Block and Sub-Redirectors](#server-message-block-and-sub-redirectors)
- [Distributed File System Namespace](#distributed-file-system-namespace)
    - [Distributed File System Replication](#distributed-file-system-replication)
- [Offline Files](#offline-files)
    - [Caching Modes](#caching-modes)
    - [Online](#online)
    - [Offline (Slow Connection)](#offline-slow-connection)
    - [Offline (Working Offline)](#offline-working-offline)
    - [Offline (Not connected)](#offline-not-connected)
    - [Offline (Need to Sync)](#offline-need-to-sync)
- [Ghosts](#ghosts)
- [Data Security](#data-security)
- [BranchCache](#branchcache)
    - [Caching Modes](#caching-modes)

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

- `Transport Driver Interface (TDI) clients` are legacy kernel-mode. TDI interface is deprecated and will be removed in a future version of Windows. Kernel-mode network clients should now use the `Winsock Kernel (WSK)` interface

- `TDI transports` (also known as transports) and `Network Driver Interface Specification (NDIS)` 
protocol drivers (or protocol drivers) 
    - Are kernel-mode network protocol drivers
    - Adding protocol-specific headers (for example, TCP, UDP, and/or IP) to data passed in the IRP, and to communicate with adapter drivers using NDIS functions (also documented in the Windows Driver Kit)

- The interface between the `TCP/IP` protocol driver and Winsock is known as the `Transport Layer Network Provider Interface (TLNPI)`

- `Winsock Kernel (WSK)` is a transport-independent, kernel-mode networking API that replaces 
the legacy TDI

- `The Windows Filtering Platform (WFP)` is a set of APIs and system services that provide the ability to create network filtering applications, example can be found [here](https://github.com/microsoft/windows-driver-samples/tree/main/network/trans/WFPSampler)

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

Make program with Winsock, get started [here](https://learn.microsoft.com/en-us/windows/win32/winsock/creating-a-basic-winsock-application)

Winsock client:
```c++
    #define WIN32_LEAN_AND_MEAN

    #include <windows.h>
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #include <stdlib.h>
    #include <stdio.h>


    // Need to link with Ws2_32.lib, Mswsock.lib, and Advapi32.lib
    #pragma comment (lib, "Ws2_32.lib")
    #pragma comment (lib, "Mswsock.lib")
    #pragma comment (lib, "AdvApi32.lib")


    #define DEFAULT_BUFLEN 512
    #define DEFAULT_PORT "27015"

    int __cdecl main(int argc, char **argv) 
    {
        WSADATA wsaData;
        SOCKET ConnectSocket = INVALID_SOCKET;
        struct addrinfo *result = NULL,
                        *ptr = NULL,
                        hints;
        const char *sendbuf = "this is a test";
        char recvbuf[DEFAULT_BUFLEN];
        int iResult;
        int recvbuflen = DEFAULT_BUFLEN;
        
        // Validate the parameters
        if (argc != 2) {
            printf("usage: %s server-name\n", argv[0]);
            return 1;
        }

        // Initialize Winsock
        iResult = WSAStartup(MAKEWORD(2,2), &wsaData);
        if (iResult != 0) {
            printf("WSAStartup failed with error: %d\n", iResult);
            return 1;
        }

        ZeroMemory( &hints, sizeof(hints) );
        hints.ai_family = AF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;
        hints.ai_protocol = IPPROTO_TCP;

        // Resolve the server address and port
        iResult = getaddrinfo(argv[1], DEFAULT_PORT, &hints, &result);
        if ( iResult != 0 ) {
            printf("getaddrinfo failed with error: %d\n", iResult);
            WSACleanup();
            return 1;
        }

        // Attempt to connect to an address until one succeeds
        for(ptr=result; ptr != NULL ;ptr=ptr->ai_next) {

            // Create a SOCKET for connecting to server
            ConnectSocket = socket(ptr->ai_family, ptr->ai_socktype, 
                ptr->ai_protocol);
            if (ConnectSocket == INVALID_SOCKET) {
                printf("socket failed with error: %ld\n", WSAGetLastError());
                WSACleanup();
                return 1;
            }

            // Connect to server.
            iResult = connect( ConnectSocket, ptr->ai_addr, (int)ptr->ai_addrlen);
            if (iResult == SOCKET_ERROR) {
                closesocket(ConnectSocket);
                ConnectSocket = INVALID_SOCKET;
                continue;
            }
            break;
        }

        freeaddrinfo(result);

        if (ConnectSocket == INVALID_SOCKET) {
            printf("Unable to connect to server!\n");
            WSACleanup();
            return 1;
        }

        // Send an initial buffer
        iResult = send( ConnectSocket, sendbuf, (int)strlen(sendbuf), 0 );
        if (iResult == SOCKET_ERROR) {
            printf("send failed with error: %d\n", WSAGetLastError());
            closesocket(ConnectSocket);
            WSACleanup();
            return 1;
        }

        printf("Bytes Sent: %ld\n", iResult);

        // shutdown the connection since no more data will be sent
        iResult = shutdown(ConnectSocket, SD_SEND);
        if (iResult == SOCKET_ERROR) {
            printf("shutdown failed with error: %d\n", WSAGetLastError());
            closesocket(ConnectSocket);
            WSACleanup();
            return 1;
        }

        // Receive until the peer closes the connection
        do {

            iResult = recv(ConnectSocket, recvbuf, recvbuflen, 0);
            if ( iResult > 0 )
                printf("Bytes received: %d\n", iResult);
            else if ( iResult == 0 )
                printf("Connection closed\n");
            else
                printf("recv failed with error: %d\n", WSAGetLastError());

        } while( iResult > 0 );

        // cleanup
        closesocket(ConnectSocket);
        WSACleanup();

        return 0;
    }
```

Winsock server:

```c++
    #undef UNICODE

    #define WIN32_LEAN_AND_MEAN

    #include <windows.h>
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #include <stdlib.h>
    #include <stdio.h>

    // Need to link with Ws2_32.lib
    #pragma comment (lib, "Ws2_32.lib")
    // #pragma comment (lib, "Mswsock.lib")

    #define DEFAULT_BUFLEN 512
    #define DEFAULT_PORT "27015"

    int __cdecl main(void) 
    {
        WSADATA wsaData;
        int iResult;

        SOCKET ListenSocket = INVALID_SOCKET;
        SOCKET ClientSocket = INVALID_SOCKET;

        struct addrinfo *result = NULL;
        struct addrinfo hints;

        int iSendResult;
        char recvbuf[DEFAULT_BUFLEN];
        int recvbuflen = DEFAULT_BUFLEN;
        
        // Initialize Winsock
        iResult = WSAStartup(MAKEWORD(2,2), &wsaData);
        if (iResult != 0) {
            printf("WSAStartup failed with error: %d\n", iResult);
            return 1;
        }

        ZeroMemory(&hints, sizeof(hints));
        hints.ai_family = AF_INET;
        hints.ai_socktype = SOCK_STREAM;
        hints.ai_protocol = IPPROTO_TCP;
        hints.ai_flags = AI_PASSIVE;

        // Resolve the server address and port
        iResult = getaddrinfo(NULL, DEFAULT_PORT, &hints, &result);
        if ( iResult != 0 ) {
            printf("getaddrinfo failed with error: %d\n", iResult);
            WSACleanup();
            return 1;
        }

        // Create a SOCKET for the server to listen for client connections.
        ListenSocket = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
        if (ListenSocket == INVALID_SOCKET) {
            printf("socket failed with error: %ld\n", WSAGetLastError());
            freeaddrinfo(result);
            WSACleanup();
            return 1;
        }

        // Setup the TCP listening socket
        iResult = bind( ListenSocket, result->ai_addr, (int)result->ai_addrlen);
        if (iResult == SOCKET_ERROR) {
            printf("bind failed with error: %d\n", WSAGetLastError());
            freeaddrinfo(result);
            closesocket(ListenSocket);
            WSACleanup();
            return 1;
        }

        freeaddrinfo(result);

        iResult = listen(ListenSocket, SOMAXCONN);
        if (iResult == SOCKET_ERROR) {
            printf("listen failed with error: %d\n", WSAGetLastError());
            closesocket(ListenSocket);
            WSACleanup();
            return 1;
        }

        // Accept a client socket
        ClientSocket = accept(ListenSocket, NULL, NULL);
        if (ClientSocket == INVALID_SOCKET) {
            printf("accept failed with error: %d\n", WSAGetLastError());
            closesocket(ListenSocket);
            WSACleanup();
            return 1;
        }

        // No longer need server socket
        closesocket(ListenSocket);

        // Receive until the peer shuts down the connection
        do {

            iResult = recv(ClientSocket, recvbuf, recvbuflen, 0);
            if (iResult > 0) {
                printf("Bytes received: %d\n", iResult);

            // Echo the buffer back to the sender
                iSendResult = send( ClientSocket, recvbuf, iResult, 0 );
                if (iSendResult == SOCKET_ERROR) {
                    printf("send failed with error: %d\n", WSAGetLastError());
                    closesocket(ClientSocket);
                    WSACleanup();
                    return 1;
                }
                printf("Bytes sent: %d\n", iSendResult);
            }
            else if (iResult == 0)
                printf("Connection closing...\n");
            else  {
                printf("recv failed with error: %d\n", WSAGetLastError());
                closesocket(ClientSocket);
                WSACleanup();
                return 1;
            }

        } while (iResult > 0);

        // shutdown the connection since we're done
        iResult = shutdown(ClientSocket, SD_SEND);
        if (iResult == SOCKET_ERROR) {
            printf("shutdown failed with error: %d\n", WSAGetLastError());
            closesocket(ClientSocket);
            WSACleanup();
            return 1;
        }

        // cleanup
        closesocket(ClientSocket);
        WSACleanup();

        return 0;
    }

```

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
- `Mswsock.dll` implements the Microsoft Winsock extension functions

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
- Providing events through which clients are notified of network status

---

## Remote Procedure Call

`Remote procedure call (RPC)` is a network programming standard

## RPC Operation

An RPC facility is one that allows a programmer to create an application consisting of any number of procedures, some that execute locally and others that execute on remote computers via a network

![](https://i.ibb.co/rK9JvHc/Screenshot-2023-02-21-153049.png)

## RPC Security

Including integration with `security support providers (SSPs)` so that RPC clients and servers can use authenticated or encrypted communications

## RPC Implementation

- RPC-based application links with the RPC run-time DLL (%SystemRoot%\System32\Rpcrt4.dll)
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

Provide for reliable bidirectional communications, whereas mailslots provide unreliable, unidirectional data transmission

## Named-Pipe Operation

- Consisting of 
    - Named-pipe server use the `ReadFile` and 
WriteFile Windows functions to read from and write to the pipe after named-pipe connection is established
    - Named-pipe client: same sever. Moreover, useing the Windows CreateFile or CallNamedPipe function
- A server to impersonate a client by using the `ImpersonateNamedPipeClient` function
- Atomic send and receive operations through the `TransactNamedPipe API`

![](https://i.ibb.co/njgnywQ/Screenshot-2023-02-21-155720.png)

## Mailslot Operation

-  Provide an unreliable, unidirectional, multicast network transport
- `Multicast` is a term used to describe a sender sending a message on the network to one or more specific listeners, which is different from a broadcast, which all systems would receive
- A mailslot server creates a mailslot by using the `CreateMailslot` function (accepts a UNC name of the form *\\.\Mailslot\MailslotName* as an input parameter)

![](https://i.ibb.co/Nx1hSrD/Screenshot-2023-02-21-210352.png)

## Named Pipe and Mailslot Implementation

- Named-pipe and mailslot functions are all 
implemented in the Kernel32.dll Windows client-side DLL
- The CreateFile function, which a client uses to open either a named pipe or a mailslot, is also a standard Windows I/O routine.

![](https://i.ibb.co/59hjSYp/Screenshot-2023-02-21-210929.png)

---

## NetBIOS

`Network Basic Input/Output System (NetBIOS)` programming API, allows for both reliable connection oriented and unreliable connectionless communication,  is supported by the `TCP/IP` protocol on Windows

![](https://i.ibb.co/RYgNPmM/Screenshot-2023-02-27-131207.png)

## NetBIOS Names

- Including 16-byte:
    - First 15 bytes of the leftmost Domain Name System (DNS) name that an administrator assigns to the domain
    - 16th byte of a `NetBIOS name` is treated as a modifier that can specify a name as unique or as part of a group
- Another concept is LAN adapter (LANA) numbers - assigned to every `NetBIOS-compatible` protocol that layers above a network adapter

## NetBIOS Operation

- A NetBIOS server application uses the NetBIOS API to enumerate the LANAs present on a system and assign a NetBIOS name representing the application’s service to each LANA
- A connection-oriented client uses NetBIOS functions to establish a connection with a NetBIOS server and then executes further NetBIOS functions to send and receive data

## NetBIOS API Implementation

- NetBIOS emulator requires the presence of the NetBT driver (%SystemRoot%\System32\Drivers\Netbt.sys) over TCP/IP protocol
- NetBT is known as the `NetBIOS` over TCP/IP driver and is responsible for supporting NetBIOS semantics that are inherent to the `NetBIOS Extended User Interface (NetBEUI)` protocol but not the TCP/IP protocol

![](https://i.ibb.co/p4hJCwx/Screenshot-2023-02-22-064531.png)

---

## Other Networking APIs

Windows includes other networking APIs that are used less frequently or are layered on the APIs which are important enough to the operation of a Windows system and many applications to merit brief descriptions

## Background Intelligent Transfer Service

-  A service and an API runnning in background that provides reliable asynchronous transfer of files between systems, using either the SMB, HTTP, or HTTPS protocol
- Tracking of ongoing, or scheduled, transfers in what are known as transfer jobs
- Providing the following capabilities:
    - Seamless data transfer
    - Multiple transfer types
    - Prioritization of transfers
    - Secure data transfer
    - Management
- BITS writes the file to a temporary hidden file in the destination 
directory when downloading files

## DCOM

- Microsoft’s COM API lets applications consist of different components, each component being a replaceable
- DCOM (Distributed Component Object Model) extends COM by letting an application’s components reside on different computers

## Message Queuing
- a general-purpose platform for developing distributed applications that take advantage of loosely coupled messaging

## UPnP with PnP-X

- `Universal Plug and Play (UPnP)`: 
    - An architecture for peer-to-peer network connectivity of intelligent 
appliances, devices, and *control points*
    - Easy-to-use, flexible, standards-based 
connectivity
    - Zero-configuration, invisible networking, and automatic discovery 
- `Plug and Play Extensions (PnP-X)`
    - Allow network-attached devices to integrate with the Plug and Play manager in the kernel
    - Use a virtual network bus driver that uses an IP bus enumerator service (%SystemRoot%\System32\Ipbusenum.dll) 
    ![](https://i.ibb.co/tK3TzP1/Screenshot-2023-02-23-091138.png)

---

## Multiple Redirector Support

File shares using UNC paths, resources can be accessed directly using the UNC name if it is already known and the logged-on user’s credentials are sufficient, and responsible components:
- `Multiple Provider Router (MPR)` is a DLL (%SystemRoot%\System32\Mpr.dll): browse 
remote file resources
- `Multiple UNC Provider (MUP)` is a driver (%SystemRoot%\System32\Drivers\Mup.sys): determine network 

## Multiple Provider Router

`Windows WNet` functions allow applications to 
connect to network resources

![](https://i.ibb.co/0ZkDVj0/Screenshot-2023-02-23-092352.png)

## Multiple UNC Provider

`Multiple UNC Provider (MUP %SystemRoot%\System32\Drivers\mup.sys)` is a file-system driver that exposes remote file systems to Windows

`MUP`(aka prefix cache) which is a list of which remote file system paths (\\<server name>[\<share name>]) that are handled by each redirector

![](https://i.ibb.co/0QsXd0M/Screenshot-2023-02-23-093557.png)

---

## Surrogate Providers

There are two surrogate providers:
- Offline Files (%SystemRoot%\System32\Drivers\csc.sys)
- Distributed File System Client (%SystemRoot%\System32\Drivers\dfsc.sys)

## Redirector

- Include the following components:
    - A DLL loaded by MPR in user mode
    - A kernel-mode driver known as a mini-redirector

- Optional components:
    - A service process to assist the DLL and possibly store sensitive information or information
    - A network protocol driver that implements the legacy Transport Driver Interface (TDI) 
    - A service process to assist the redirector

## Mini-Redirectors

Making access to remote resources as transparent as possible to the local client application, some included with Windows:
- RDPDR (Remote Desktop Protocol Device Redirection)
- SMB (Server Message Block)
- WebDAV (Web Differencing and Versioning)
- MailSlot (part of MRxSMB.SYS)
- Network File System (NFS) 

## Server Message Block and Sub-Redirectors

- Server Message Block (SMB) protocol is the primary remote file-access protocol used by Windows 
clients and servers
- The common portions are implemented by %SystemRoot%\System32\Drivers\MRxSMB.sys
- The SMB 1 protocol is implemented by %SystemRoot%\System32\Drivers\MRxSMB10.sys
- The SMB 2 protocol is implemented by %SystemRoot%\System32\Drivers\MRxSMB20.sys

--- 

## Distributed File System Namespace

- Distributed File System Namespace (DFS-N) is a namespace aggregation and availability feature 
of Windows
- Allow an administrator to create a new file share (also known as a root or namespace) 
- Providing are redundancy and location-aware redirection
- Is implemented in a MUP surrogate provider driver 
(%SystemRoot%\System32\Drivers\Dfsc.sys) and an MPR/WNet provider implemented in 
%SystemRoot%\System32\Ntlanman.dll

## Distributed File System Replication

- Providing bandwidth-efficient, asynchronous, multimaster replication of file-system changes between servers
- Using several technologies to conserve network bandwidth
- Compressing content before sending it to a remote partner, providing additional bandwidth savings
- Is implemented as a Windows service (%SystemRoot%\System32\DfsrS.exe) that uses authenticated RPC with encryption

## Offline Files

- Transparently caches files from a remote system (a file server) on the local machine which is available in offline
- All cached files are stored in an ACL-protected directory (default is %SystemRoot%\CSC)
- Understanding two types of objects:
    - Files: files, folders, and symbolic links
    - Scope: the portion of a namespace that corresponds to a physical share
- Some limitations:
    - Offline Files does not cache alternate data streams
    - Offline Files does not cache Extended Attributes (EAs)
- Consists of the following components:
    - A user-mode agent (%SystemRoot%\System32\cscsvc.dll) running as a service in an SVCHOST 
process
    - A remote file system driver (%SystemRoot%\System32\Drivers\csc.sys)
    - An Explorer extension DLL (%SystemRoot%\System32\cscui.dll)
    - A DLL (%SystemRoot%\System32\cscapi.dll) 
    - An in-process COM object (%SystemRoot%\System32\cscobj.dll)

    ![](https://i.ibb.co/tXPB7bV/Screenshot-2023-02-23-105956.png)

---

## Caching Modes

Is determined by whether or not the local system has a network connection to the file server.

## Online

- Default mode, the server is available
- File system metadata operations and write operations flow to the server, and the cache state is updated as required

## Offline (Slow Connection)

- Happen when the network performance meets the configured slow-link latency 
or bandwidth thresholds
- Can be controlled via the Group Policy editor (%SystemRoot%\gpedit.msc)

## Offline (Working Offline)

- All file-system operations are satisfied from the cache

## Offline (Not Connected)

- Happern when the server is not accessible
- When the network connection to the server is re-established, any changes written to the file are 
synchronized back to the server by the Offline Files agent

## Offline (Need to Sync)

- The status of this file will be Offline (Need to Sync) until the changes are synchronized back to the server
- Keep the user working offline for the affected files until that synchronization is complete

---

## Ghosts

- Selected files are available offline, they must be copied from the server to the client. Until the transfer is complete, not all the files will be visible on the client
- Offline Files creates ghosts (markers for files and directories that have not been copied and are unavailable in the cache) of the files and directories on the server within the cache as soon as caching is enabled

## Data Security

- Offline Files caches access for a given user as the data is accessed or synchronized on behalf of that user
- Files protected with EFS remain protected but are encrypted in the security context of the first user

## Cache Structure

- Located in %SystemRoot%\CSC and is protected with a DACL that grants Administrators full control of the directory and everyone else read
- The files consist of the Priority Queue (pq) and SID Map (sm) databases
- The namespace directory is the root of the cache and contains a directory for each server that Offline Files is caching

![](https://i.ibb.co/JFjkKXb/Screenshot-2023-02-23-144143.png)

## BranchCache

- Is a generalized content-caching mechanism designed to reduce network bandwidth, especially over WANs
- Is fully compatible with end-to-end encryption, such as IPsec
- Is similar to `Offline Files`
- A variety of protocols make use of BranchCache:
    - Server Message Block (SMB)
    - HTTP(S) Web pages, video streams, and other content identified by a URL
    - Background Intelligent Transfer Service (BITS) Used to transfer files, and runs over HTTP/TLS 1.1
    
![](https://i.ibb.co/gTT5TWB/Screenshot-2023-02-27-082008.png)

- BranchCache’s operation is transparent to the applications accessing the content being cached, has 2 caching mode
    - Hosted Cache: a single server, contains the entire content cache for all BranchCache-enabled systems
    - Distributed Cache: the cache is spread across all the clients on the same subnet, is implemented using peer-to-peer networking, using the Web Services Discovery (WS-D) multicast protocol

![](https://i.ibb.co/Tg1JBWT/Screenshot-2023-02-27-082804.png)

- Some BranchCache features the following behaviors:
    - Data transfer uses `AES encryption`
    - caches only content that is larger than 64 KB (can modify at HKLM\System\CurrentControlSet\Services\PeerDistKM\Parameters\MinContentLength)

## Caching Modes

Maintains two different local caches on each BranchCache-enabled system
- `The publication cache` stores content information metadata for content published using the 
`BranchCache Server APIs` 
- `Publishing`
    - An application and/or protocol that uses BranchCache acceleration can ask BranchCache to store content information metadata on its behalf
    - Alternatively, an application/protocol that wants to use BranchCache acceleration can ask BranchCache to generate only content information metadata without storing it, and instead simply return the metadata to the application or protocols
    - Change with NetSh:
        -  netsh branchcache set publicationcache directory=C:\PublicationCacheFolder
        - netsh branchcache set publicationcachesize size=20 percent=TRUE
- `The republication cache` contains both metadata (but no secrets) and actual data (chunked 
in segments and blocks) for the BranchCache content retrieved by the local BranchCache client. Using NetSh to change value
    - netsh branchcache set localcache directory=C:\BranchCache\Localcache
    - netsh branchcache set localcache size=20 percent=TRUE

