# Securing Your Server with a Firewall - Part 2

## Table of content

- [Securing Your Server with a Firewall - Part 2](#securing-your-server-with-a-firewall---part-2)
  - [Table of content](#table-of-content)
  - [Technical requirements](#technical-requirements)
  - [nftables – a more universal type of firewall system](#nftables--a-more-universal-type-of-firewall-system)
  - [Learning about nftables tables and chains](#learning-about-nftables-tables-and-chains)
    - [Getting started with nftables](#getting-started-with-nftables)
      - [Configuring nftables on Ubuntu 16.04](#configuring-nftables-on-ubuntu-1604)
      - [Configuring nftables on Ubuntu 18.04](#configuring-nftables-on-ubuntu-1804)


## Technical requirements

The code files are available [here](https://github.com/PacktPublishing/Mastering-Linux-Security-and-Hardening-Second-Edition)

## nftables – a more universal type of firewall system

 - Benefit of `nftables`
    - The `nft` utility is now the only needed firewall utility 
    - Create multi-dimensional trees to display rulesets to troubleshoot vastly easier
    - Having the filter, NAT, mangle, and security tables installed by default
    - Only creating the tables intending to use that enhance performance
    - Specify multiple actions in one rule
    - New rules get added atomically
    - Having its built-in scripting engine that make scripts more efficient and more human-readable
    - Can install a set of utilities to convert them into `nftables` format
  - `sudo nft -v` to check version of `nftables`

## Learning about nftables tables and chains

 - `Tables`: Tables in `nftables` refer to a particular protocol family
 - `Chains`: Chains in `nftables` roughly equate to tables in iptables

### Getting started with nftables

 - Install `nftables` on Ubuntu: `sudo apt install nftables`
 - List all tables `sudo nft list tables`

#### Configuring nftables on Ubuntu 16.04

 - default `nftables.conf` file in the /etc directory

#### Configuring nftables on Ubuntu 18.04