Chapter 7: Common Upper-Layer Protocols


## Table of contents

- [Table of contents](#table-of-contents)
- [Dynamic Host Configuration Protocol](#dynamic-host-configuration-protocol)
- [Domain Name System](#domain-name-system)
- [Hypertext Transfer Protocol](#hypertext-transfer-protocol)


## Dynamic Host Configuration Protocol
  
- An application layer protocol allowing a devices to automatically obtain an IP address
- DHCP servers provide other parameters to clients: address of the default gateway and DNS servers,..

- The DHCP Packet Struture:
    ![](IMG/2023-03-17-09-54-25.png)

- The DHCP Renewal Process
  - The `renewal process` (DORA process) takes place between a single client and a DHCP server, use four types of DHCP packet:
    - Discover: Find a DHCP server that will listen
      - DCHP message type
      - Client Identifier
      - Requested IP Address
      - Parameter Request List
    - Offer
    - Request
    - Acknowledgment
    ![](IMG/2023-03-17-13-13-31.png)

## Domain Name System

## Hypertext Transfer Protocol

