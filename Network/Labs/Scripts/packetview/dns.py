import dpkt
import datetime
from dpkt.utils import mac_to_str, inet_to_str

def print_dns(pcap):
    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)

        # Make sure the Ethernet data contains an IP packet
        if not isinstance(eth.data, dpkt.ip.IP):
            print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
            continue

        # Now grab the data within the Ethernet frame (the IP packet)
        ip = eth.data

        # Check for UDP in the transport layer
        if isinstance(ip.data, dpkt.udp.UDP) and ip.data.dport == 53:

            # Set the UDP data
            udp = ip.data

            # Parse the DNS packet
            try:
                dns = dpkt.dns.DNS(udp.data)
            except dpkt.dpkt.UnpackError:
                continue

            # Print out the info
            print('Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
            print('Ethernet Frame: ', mac_to_str(eth.src), mac_to_str(eth.dst), eth.type)
            print('IP: %s -> %s   (len=%d ttl=%d)' %
                    (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl))
            print('UDP: %d -> %d   (len=%d)' %
                    (udp.sport, udp.dport, udp.ulen))
            print('DNS transaction ID: %d' % dns.id)
            print('DNS questions: %d' % len(dns.qd))
            print('DNS answers: %d' % len(dns.an))
            print('DNS authorities: %d' % len(dns.ns))
            print('DNS additional: %d' % len(dns.ar))

            # Print out the DNS queries
            for query in dns.qd:
                print('DNS query: %s' % query.name)

            # Check for payload spanning acrossed UDP packets
            if len(udp.data) != udp.ulen - dpkt.udp.UDP_HDR_LEN:
                print('\nPAYLOAD TRUNCATED! Reassemble UDP packets!\n')