# Instrusion detection and prevention system

Scanning processes for harmful patterns, comparing system files, and monitoring user behavior and system patterns

## Table of contents

- [Instrusion detection and prevention system](#instrusion-detection-and-prevention-system)
  - [Table of contents](#table-of-contents)
  - [Key features](#key-features)
  - [Types of IDPS](#types-of-idps)
  - [Mechanism](#mechanism)
    - [Detection](#detection)
      - [Threshold monitoring](#threshold-monitoring)
      - [Profiling](#profiling)
      - [Prevention](#prevention)
  - [Techniques](#techniques)
  - [Some open source IDPS](#some-open-source-idps)
    - [Snort](#snort)
    - [Suricata](#suricata)

## Key features

- `Guarding technology infrastructure` and `sensitive data` are reactive, alerting security experts of such possible incidents, proactive, allowing security teams to mitigate these attacks that may cause financial and reputational damage
- `Reviewing existing user` and `security policies` reduce the attack surface by providing access to critical resources to only a few trusted user groups and system, spot any holes in these policy frameworks right away, tweak policies to test for maximum security and efficiency
- `Gathering information` about network resources allows them to modify a system in case of traffic overload or under-usage of servers
- `Helping meet compliance regulations` ensures consumer data privacy and security

## Types of IDPS

- `Network-based intrusion prevention system (NIPS)` analyzes protocol activity for malicious traffic
- `Wireless intrusion prevention system (WIPS)` analyzes wireless networking specific protocols
- `Network behavior analysis (NBA) system` analyzes deviations in protocol activity, network behavior analysis systems identify threats by checking for unusual traffic patterns
- `Host-based intrusion prevention system (HIPS)` monitors the traffic flowing in and out of that particular host by monitoring running processes, network activity, system logs, application activity, and configuration changes

## Mechanism

### Detection

#### Threshold monitoring

- Setting accepted levels associated with each user, application, and system behavior
- The monitoring system alerts admins and sometimes triggers automated responses when a threshold is crossed

#### Profiling

- `User profiling` involves monitoring if a user with a particular role or user group only generates traffic that is allowed. This comes in handy while creating a baseline for normal behavior and for creating a user role itself
- `Resource profiling` measures how each system, host, and application consumes and generates data

#### Prevention

- `Stopping the attack` blocks users or traffic originating from a particular IP address. It also involves terminating or resetting a network connection
- `Security environment` changes involves changing security configurations to prevent attacks
- `Attack content modification` makes content more benign is to remove the offending segments

## Techniques

- `Signature-based` maintains a database of known malware or attack signatures
- `Anomaly-based` works on threshold monitoring and profiling
- `Stateful protocol` analysis goes one step further and uses the predefined standards of each protocol state to check for deviations

## Some open source IDPS

### Snort

### Suricata