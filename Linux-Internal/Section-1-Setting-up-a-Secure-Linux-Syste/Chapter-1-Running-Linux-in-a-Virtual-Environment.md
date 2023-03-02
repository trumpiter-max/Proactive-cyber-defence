# Chapter 1: Running Linux in a Virtual Environment

- Linux was designed from the ground up as a multiuser operating system
- Linux offers a better separation between administrative users and unprivileged 
- Linux is much more resistant to viruses and malware infections than Windows is
- Linux is a free and open-source software

## Table of content
 - [Looking at the threat landscape](#looking-at-the-threat-landscape)
 - [Why do security breaches happen?](#why-do-security-breaches-happen)
 - [Keeping up with security news](#keeping-up-with-security-news)
 - [Differences between physical, virtual, and cloud setups](#differences-between-physical-virtual-and-cloud-setups)
 - [Introducing VirtualBox and Cygwin](#introducing-virtualbox-and-cygwin)
 - [Installing a virtual machine in VirtualBox](#installing-a-virtual-machine-in-virtualbox)
 - [Keeping the Linux systems updated](#keeping-the-linux-systems-updated)


## Looking at the threat landscape

Several cases where attackers have planted other types of malware on Linux servers
- `Botnet malware` used for denial-of-service (DoS) attacks against other networks
- `Ransomware` encrypts user data until the server owner pays a ransom fee
- `Cryptocoin mining software` causes the CPUs of the server on which it's
planted to work extra hard and consume more energy

## Why do security breaches happen?

- Could be *security bugs* in the operating system or *security bugs* in an application that's running on that operating system
- *Out-of-the-box configuration* of a Linux server is quite insecure and can cause a whole ton of problems
- *Internet of Things (IoT)* has been many security problems with these devices, in large part because people just don't know how to configure them securely

## Keeping up with security news

The IT business should keep up with the latest security news, somethings can be done:
- There are quite a few websites that specialize in network security news (Packet Storm Security, The Hacker News, Ars Technica, Fudzilla, The Register, ZDNet, and LXer, etc.)
- Keep up with the news and current documentation for your Linux distribution 

## Differences between physical, virtual, and cloud setups

`Virtual machine`:
 - Is now cheaper and more convenient to install multiple virtual machines on each server
 - Risks can be found in the physical server that hosts these virtual machines, and each virtual machine
 - Ensuring that the virtual machines remain properly isolated from each other, especially ones that contain sensitive data
- Cloud where a person or a company can spin up an instance of either Windows or their choice of Linux distro

## Introducing VirtualBox and Cygwin

 - There are several different virtualization platforms that you can use, but the preferred choice is `VirtualBox` (free to use)
 - If your host machine is running Windows, install some sort of Bash shell, which you can do by either installing `Cygwin` ( a large collection of GNU and Open Source tools that provide functionality similar to a Linux distribution on Windows)
 - Using the `Bash shell` that's built into `Windows 10 Pro` (can access physics resources which `Cygwin`` can not do cause of its own sandboxed directory structure)

## Installing a virtual machine in VirtualBox

Download [VirtualBox and the VirtualBox Extension Pack](https://www.virtualbox.org/) and follow installing steps, then download the ISO Linux file to get started

## Keeping the Linux systems updated

[Common Vulnerabilities and Exposures](https://cve.mitre.org/) database where identity, define, and catalog publicly disclosed cybersecurity vulnerabilities

![](https://i.ibb.co/HDpGZpN/Screenshot-2023-02-27-212327.png)