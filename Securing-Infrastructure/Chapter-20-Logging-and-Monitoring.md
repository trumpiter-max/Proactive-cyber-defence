# Chapter 20. Logging and Monitoring

## Table of contents

- [Chapter 20. Logging and Monitoring](#chapter-20-logging-and-monitoring)
  - [Table of contents](#table-of-contents)
  - [What to Log](#what-to-log)
  - [Where to Log](#where-to-log)
  - [Security Information and Event Management](#security-information-and-event-management)
  - [Designing the SIEM](#designing-the-siem)
  - [Log Analysis](#log-analysis)
  - [Logging and Alerting Examples](#logging-and-alerting-examples)
    - [Authentication Systems](#authentication-systems)
    - [Application Logs](#application-logs)
    - [Proxy and Firewall Logs](#proxy-and-firewall-logs)
  - [Log Aggregation](#log-aggregation)
  - [Use Case Analysis](#use-case-analysis)


## What to Log

- Everything provides access to all the possible data that may be required, but also provides more of a challenge when it comes to
storage, indexing, and in some cases transmitting the data
- Only what you need is best to start slowly with what is needed and then build upon it

## Where to Log

- Collect and aggregate logs at a central location because:
  - Logs are no longer stored on the host that created them
  - Aggregated logs provide better data for analysis
- `Unix` host with a large amount of storage running syslogd and collecting the logs for the
environment to its own `/var/log/` directory. Moreover, Security Information & Event Management (SIEM) can platforms that perform this role 

## Security Information and Event Management

- Not only collects logs, it takes those logs and other security-related documentation and correlates them for analysis
- Allows more intelligent security-related alerts, trends, and reports to be created
- Can be set up in one of several different configurations; software installed on a local server, a hardware appliance, a virtual appliance, or a cloud-based service

## Designing the SIEM

Steps prior to implementation include:
- Define the coverage scope
- Establish threat scenarios/use cases
- Define the priority of threats
- Perform a proof of concept

## Log Analysis

- Many higher-end SIEMs come preconfigured with at least a default set of alert rules, some of which are integrated with threat intelligence feeds
- Once the rules are tuned to an acceptable level of false positives and false negatives, they can be moved to real-time alerting

## Logging and Alerting Examples

Illustrate the sorts of alerts that can be easily generated via log analysis

### Authentication Systems

Several tests that can yield immediate results:
- Users logging into systems at unusual hours
- Repeated login failures
- Users logging in from unusual or multiple locations
- Insecure authentication
- Default accounts
- Domain admin group changes

### Application Logs

These logs can provide useful insight into adversaries performing attacks against these hosts or performing reconnaissance:
- Too many 4XX responses from a web server
- Too many hits on one specific URL on a web server
- Connects and disconnects with no transaction on multiple types of servers
- New services, processes, and ports should not be an unplanned configuration change, especially on servers

### Proxy and Firewall Logs

Discovering unexpected outbound traffic and other anomalies that could indicate a threat from an insider or an intrusion:
- Outbound connections to unexpected services
- Matching IP addresses or hostnames on blacklists
- Connections of unexpected length or bandwidth

## Log Aggregation

- Is useful for purposes other than centralized management of
logs
- Easily be written off as a mistyped password or a user accidentally
connecting to the wrong host

## Use Case Analysis

There are always new threats to model, and new indicators to monitor:
- Brute-force attack
- Data exfiltration
- Impossible or unlikely user movements
- Ransomware