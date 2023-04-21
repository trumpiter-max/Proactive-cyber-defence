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
    - [Organizational Units](#organizational-units)
    - [Groups](#groups)
    - [Accounts](#accounts)
  - [Group Policy Objects](#group-policy-objects)
  - [EMET](#emet)
  - [MS-SQL Server](#ms-sql-server)
    - [When Third-Party Vendors Have Access](#when-third-party-vendors-have-access)
    - [MS SQL Authentication](#ms-sql-authentication)
    - [SA User Security](#sa-user-security)


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

### Organizational Units 

Can be used for the purpose of delegating rights/permissions to perform certain actions to the objects located in it as well
as implementing a well thought-out structure for Group Policy Objects (GPOs)

### Groups

There are strict guidelines for what AD groups are and are not used for, because the nesting and assigning of groups can get quite messy

### Accounts

`Local Administrator Password Solution (LAPS)` is a free software from Microsoft that will perform random password allocations to local administrator accounts. This provides another added layer of security, making it difficult for an attacker to perform lateral movements from one device to the next

## Group Policy Objects

- Used to centrally manage hardware and software settings in a domain configuration to maintain in some domains
- National Institute of Science and Technology, or NIST, has a secure base set of GPOs that can be downloaded off of its website. A great first step for any  organization would be to include these on any base image in the local policy

## EMET

- `The Enhanced Mitigation Experience Toolkit (EMET)` is a utility that helps prevent vulnerabilities in software from being successfully exploited
- Works by injecting an EMET.dll into running executables to provide memory-level protections and mitigations against common exploit techniques

## MS-SQL Server

SQL Servers can be a very easy target for attackers if not configured and patchedproperly. A wide variety of tools and methods provide privilege escalation and access to database information

### When Third-Party Vendors Have Access

Some security considerations that are vendor-specific are:
- Require the vendors to use SQL Server’s native security instead of one predefined account for all user connections
- Ensure that clients will not be connected to the SQL Server using a login and password stored in a connection string
- Audit vendor configurations
- Ensure that the vendor does not store unencrypted logins and passwords required by the application
- Ensure the authentication and activity of vendor accounts are monitored
- Do not allow the vendor to control/use the SA login
- Do not store SQL logins and passwords unencrypted in plain text

### MS SQL Authentication

- Windows Authentication mode relies solely on Windows authentication of the login. Connections using this mode are known as trusted connections
- Mixed Authentication mode is available for backward compatibility with legacy systems. In order to access data from a SQL Server database, a user must pass through two stages of authentication

### SA User Security

Some general SQL authentication:
- Have a strong password
- Limit the number of logins with sysadmin privileges
- The service account running MS SQL needs to be a sysadmin with a strong password
- Always run SQL Server services by using the lowest possible user rights, such as a minimally privileged domain account
- Never connect clients to the database using the SA account in any connection string
- Never store the SA password in a file
- Avoid using the SA login

