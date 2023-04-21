# Chapter 19. IDS and IPS


**Intrusion detection systems (IDS)**
- Monitors network traffic and system logs for signs of potential security breaches
  - Unauthorized access attempts
  - Malware infections
  - ..
- When an IDS detect a security threats, it generates alerts or notifications

**Intrusion Prevention Systems (IPS)**
- Not only detects potential security breaches but also takes active measures to prevent them
- Automatically block or quarantine suspicious traffic
- Restrict network access for users or devices that violate security policies
- Terminate connections with malicious actors

**Attack detection techniques**:
- Signature-based
- Anomaly-based
- Specification-based
- Hybrid

## Type of IDS and IPS

- Network-based IDS/IPS:
  - operate at the network level
  - analyzing traffic as it passes through the network
  - detect and prevent attacks that may not be detected by firewalls
  - techniques:
    - signature-based detection
    - anomaly detection
    - protocol analysis


- Host-based IDS/IPS:
  - operate on individual hosts
  - monitoring activities and events that occur on a particular computer system
  - techniques:
    - file integrity monitoring
    - log analysis
    - system call monitoring

- Snort is a Network-based IDS/IPS 

## Writing Your Own Signatures

![](IMG/2023-04-05-08-41-49.png)
![](IMG/2023-04-05-08-42-31.png)

