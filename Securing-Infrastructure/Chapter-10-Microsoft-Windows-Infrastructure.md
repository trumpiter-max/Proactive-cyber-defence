# Chapter 10. Microsoft Windows Infrastructure

## Table of contents

- [Chapter 10. Microsoft Windows Infrastructure](#chapter-10-microsoft-windows-infrastructure)
  - [Table of contents](#table-of-contents)
  - [Quick wins](#quick-wins)
    - [Upgrade](#upgrade)
    - [Third-Party Patches](#third-party-patches)
    - [Open Shares](#open-shares)
  - [Active Directory Domain Services](#active-directory-domain-services)
    - [Forest](#forest)
    - [Domain](#domain)
    - [Domain Controllers](#domain-controllers)


## Quick wins

### Upgrade

Upgrading endpoints to a supported operating system

### Third-Party Patches

- Windows Server Update Services (WSUS), System Center Configuration Manager (SCCM), and other third-party applications can keep the endpoints up-to-date with the latest security patches
- Focus on outdated versions of commonly exploited software such as Java, Adobe Reader,
Firefox, and others that are currently in use

### Open Shares

Cause all kinds of security problems such as saved credentials and trade secrets to PII and other sensitive data is leaked

## Active Directory Domain Services

### Forest

- The forest acts as a security boundary for an organization and defines the scope of authority for administrators
- The risks surrounding trusts are in the authentication ability from one domain or
forest to another

### Domain

Should be used purely as a structural container

### Domain Controllers

- Are the building blocks of Active Directory Domain Services
- There are a few standard rules to abide by to ensure they are placed properly