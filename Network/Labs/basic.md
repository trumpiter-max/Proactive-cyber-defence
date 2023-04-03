# Basic cases

Some known cases with basic setup 

## Table of contents:

- [Basic cases](#basic-cases)
  - [Table of contents:](#table-of-contents)
  - [Analyze nmap scanning](#analyze-nmap-scanning)
  - [Analyze PHP CGI Argument Injection](#analyze-php-cgi-argument-injection)
  - [Analyze UnrealIRCD 3.2.8.1 Backdoor Command Execution](#analyze-unrealircd-3281-backdoor-command-execution)

---

## Analyze nmap scanning

Uisng nmap with option -O to scan OS of victim, check the `pcap` file [here](/Network/Labs/Material/Attack/Basic/nmap.pcap)

## Analyze PHP CGI Argument Injection

Using `Metasploit`, choose `exploit/multi/http/php_cgi_injection` with payload `php/meterpreter/reverse_tcp` to attack, check the `pcap` file [here](/Network/Labs/Material/Attack/Basic/php.pcap)

## Analyze UnrealIRCD 3.2.8.1 Backdoor Command Execution

Using `Metasploit`, choose `exploit/unix/irc/unreal/_ircd_3281_backdoor` with payload `cmd/unix/reverse_perl` to attack, check the `pcap` file [here](/Network/Labs/Material/Attack/Basic/backdoor.pcap)