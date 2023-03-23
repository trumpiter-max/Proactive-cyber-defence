import dpkt
import sys
import icmp, tcp, udp, http, dns

if len(sys.argv) < 2:
    print('Usage: python %s <path-of-file> <option> \n -general \n -icmp \n -tcp' % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

# Open the filename file in binary mode
with open(filename, 'rb') as f:
    if filename.endswith('.pcap'):
        filename = dpkt.filename.Reader(f)
    elif filename.endswith('.pcapng'):
        filename = dpkt.pcapng.Reader(f)

    for option in range (2, len(sys.argv)):
        if sys.argv[option] == '-icmp':
            icmp.print_icmp(filename)
        if sys.argv[option] == '-tcp':
            tcp.print_tcp(filename)
        if sys.argv[option] == '-udp':
            udp.print_udp(filename)
        if sys.argv[option] == '-http':
            http.print_http(filename)
        if sys.argv[option] == '-dns':
            dns.print_dns(filename)