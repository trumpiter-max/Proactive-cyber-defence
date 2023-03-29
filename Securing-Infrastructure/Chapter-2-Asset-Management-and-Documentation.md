# Chapter 2. Asset Management and Documentation


Asset management is not an information security function but it assist in strengthening the overall security posture.
- Ensure there is one source of truth
- This is a process, not a project

## Information Classification
 
- HIPPAA and PCI DSS standards dictate the type of information that should be specifically guarded and segregated

- Steps to correctly classify data:
  1. Identify data sources to be protected
  2. Identify information classes
  3. Map protection to set information classifications levels.
  4. Classify and protect information
  5. Repeat as a necessary part of a yearly audit

## Implementation Steps
    
- The asset management process can be separated out into four distinct steps:
  - Defining the lifecycle
    - *Procure*: 
      - The initial device information (serial number, PO, asset owner, criticality, and model name and number) can be added to the tracking system
    - *Deploy*:
      - When an asset is deployed by a admin, the location of the device can now be updated and any automated population can be tested
    - *Manage*:
      - Contain many subsections depending on the level of documentation and tracking.
      - Items can be moved to storage, upgraded, replaced, or returned, or may change users, locations, or departments.
    - *Decommission*:
      - There are many different ways to destroy data, and these have varying levels of security and cost:
        - Staging for disposal
          - A single pass wipe
          - Multiple wipes
          - Degaussing 
          - Full disk encryption
        - Physical disposal
          - Crushing/drilling/pinning
          - Shredding
          - Remove as asset from inventory
  - Information gathering
    - Several  methods to obtaining information about network-connected assets:
      - Address Resolution Protocol (ARP) cache
      - Dynamic Host Configuration Protocol (DHCP)
      - Nmap
      - PowerShell
      - Simple Network Management Protocol (SNMP)
      - Vulnerability management software
      - Windows Management Interface (WMI)
  - Change tracking:
    - Keeping track of changes in hardware, software, and performance is a necessary step to having an up-to-date inventory.
  - Monitoring and reporting:
    - Provides notifications of upcoming software licensing renewals and hardware warranty expirations.

## Guidelines

- Automation:
  - Attempt to automate as many as possible
  - Everything that can be automated leads to a more efficient process.

- Open Source of Truth:
  - When choosing a software of method, it should be well communicated that it alone is the one source of truth regarding assets, and any deviation should be dealt with.

- Organize a Company-wide team

- Executive Champions

- Software Licensing

## Documentation

