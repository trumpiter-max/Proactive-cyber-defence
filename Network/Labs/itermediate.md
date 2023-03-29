# Intermediate cases

Some unknown cases

## Table of contents

- [Intermediate cases](#intermediate-cases)
  - [Table of contents](#table-of-contents)
  - [Attack trace](#attack-trace)

---

## Attack trace

Check at Statistics->Endpoints, and there are 2 hosts: 98.114.205.102 and 192.150.11.111 (attacker 98.114.205.102:445 (SMB) and victim 192.150.11.111:1821 (TCP/UDP)). Note: using [this tool](https://www.adminsub.net/tcp-udp-port-finder/) to check port

![](https://i.ibb.co/vwqNRx8/Screenshot-2023-03-24-131504.png)

Then, using [this tool](https://www.whatismyip.com/ip-address-lookup/) to find location of above addresses:

![](https://i.ibb.co/tqSV26v/Screenshot-2023-03-24-131815.png)

![](https://i.ibb.co/fHStvPs/Screenshot-2023-03-24-131923.png)

Check at Statistics->Capture file properties to find Timespan, Average Packages

![](https://i.ibb.co/9cxLXyg/Screenshot-2023-03-24-132536.png)

Using filter in wireshark `tcp.flags==0x02` to find tcp dump (The hexadecimal number 0x02 the TCP SYN flag is present in the TCP header)

![](https://i.ibb.co/6vhF3KC/Screenshot-2023-03-24-132059.png)





