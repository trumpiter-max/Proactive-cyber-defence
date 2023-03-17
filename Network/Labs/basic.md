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

Using `nmap` scanning to detect the OS of the victim with a command: `nmap -O <victim-ip>`, check the `pcap` file [here](/Network/Labs/Material/Basic/nmap.pcap)

First, to get an overview of this `.pcap` file, we can use `Statistics`:
- `Capture File Properties`: number of packets, time packet, name, length, hash
- `Protocol Hierarchy Statistics`: 
  - Types of traffic are present on the network and 
  - which protocols are most commonly used.
  - shows the volume of traffic for each protocol
    ![](IMG/2023-03-16-22-15-42.png)
- `Endpoints`:
  - IP addresses of the endpoint
  - transport protocols used
    ![](IMG/2023-03-16-22-17-35.png)
- `Conversation`:
  - total number of conversations
  - type of communication that is taking place between the endpoints
  - Easily visualize the data flow between endpoints.
    ![](IMG/2023-03-16-23-03-06.png)
=> 10.81.6.100 sent packets to many hosts on 192.168.6.200

- When filtered with `ip.src == 10.81.6.100`
    ![](IMG/2023-03-16-23-30-49.png)
  => We can see that don't have any packet with flag ACK from it
=> nmap scan

=======
>>>>>>> parent of 8c34b3f (update)
## Analyze PHP CGI Argument Injection

Using `Metasploit`, choose `exploit/multi/http/php_cgi_injection` with payload `php/meterpreter/reverse_tcp` to attack, check the `pcap` file [here](/Network/Labs/Material/Basic/php.pcap)

## Analyze UnrealIRCD 3.2.8.1 Backdoor Command Execution

Using `Metasploit`, choose `exploit/unix/irc/unreal/_ircd_3281_backdoor` with payload `cmd/unix/reverse_perl` to attack, check the `pcap` file [here](/Network/Labs/Material/Basic/backdoor.pcap)