# Chapter 14. Network Infrastructure


## Firmware/Software Patching

- Network equipment runs software or firmware => Requires patching to stay up-to-date

-  Patches should be 
   -  Tested, approved, and deployed under your internal change control processes.
   - Deploy as fast as possible
     - To close security holes
     - Remain on a vendor-supported version

- On consumer-grade equipment, the process is generally as simple as 
  - downloading a binary package from a website
  - verifying the signature
  - installing via a web interface by uploading to the relevant form

- On enterprise grade equipment, the process is more complicated. It contains one of preparation and one of upgrade:
  - Steps to prepare:
    - Select the correct system image for download from the network equipment manufacturer
    - Verify prerequisites
    - Verify the signature of the image
    - Backup existing configuration
  - Steps to upgrading:
    - Copy the verified image to the device
    - Upgrade
    - Reboot
    - Verify successful operation

## Device Hardening

- This is an effective way to drastically reduce the risk of a network device by extension, your environment.
  
- Services:
  - Networking infrastructure will typically run services of sorts for remote management, time synchronization, telemetry data, etc
  - Disabling unused services on network infrastructure reduces the opportunity for an attacker to find a flaw.
is listening on the network

- SNMP:
  - Simple Network Management Protocol: 
    - Has many uses:    
        - The most common use is for collecting telemetry data :
          - bandwidth usage per interface
          - CPU usage
          - memory consumption
        - also be used to obtain more sensitive configuration data 
    - We need to change the default configuration of SNMP:
      - The community strings:
        - Data that can be obtained via the public community string
        - The private community string allows an attacker to reconfigure devices
        - SNMP produces vastly disproportionate output compared to its input

- Encrypted Protocols
  - Checking the documentation to determine if encrypted versions of management protocols can be used

- Management Network:
  - By restrict access to interfaces, an attacker will need to compromise the management network before he can attempt to compromise the management interface of the device


## Routers

- Routers typically contain options to provide some rudimentary packet filtering
in the form of Access Control Lists (ACLs).
  - ACLs are very much like simplified
firewall rules, which allow a router to drop packets based on simple criteria
    - ACLs can drop all traffic to the router unless it originates from specific networks authorized to manage the router
    - Provide coarse filters for other equipment or networks

- Router depending on vendor and default configuration, ship with dynamic routing protocols such as: 
  - Interior Gateway Protocol (IGP)
  - Routing Information Protocol version 2 (RIPv2)
  - Enhanced Interior Gateway Routing Protocol (EIGRP)
  - Open Shortest Path First (OSPF)


## Switches

- Switches have much higher port density than other devices and are used to directly connect devices to the network. It have some additional options
  - Virtual Local Area Networks (VLANs):
    - provide logical segmentation
    - Can use to contain groups of devices together and restrict broadcast protocols such as DHCP from reaching other hosts.
  - Port security:
    - Use to prevent an attacker from gaining access to a network by unplugging a legitimate device and plugging in a malicious device in its place
    - It do not allow MAC address of a port to change without administrator authorization
  - 802.1X
    - A standard for providing port-level authentication
    - The host has to authenticate
    in order for the network port to be connected to the rest of the network

## Egress Filtering

- Use to filtering outbound traffic
- By restricting outbound traffic only to protocols and IP addresses that are
expected as part of normal use, command and control infrastructure running on other ports and IP addresses will be unavailable to the malware
- By blocking access to all
but the expected resources, data exfiltration can be made more difficult to
achieve

## TACACS+

- TACACS+ (Terminal Access Controller Access-Control System Plus) provides AAA architecture for networking equipment.
  - AAA architecture:
    - Authentication
    - Authorization
    - Accounting

- Setting up a TACACS+ server can help networking equipment can make use of central authentication
  - Give benefits as a single point of provisioning and deprovisioning of users
  - The accounting features provide centralized storage of accounting data in a central logging repository