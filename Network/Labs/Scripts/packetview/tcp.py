import dpkt
import datetime
from dpkt.utils import mac_to_str, inet_to_str

def print_tcp(pcap):
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

        # Check for TCP in the transport layer
        if isinstance(ip.data, dpkt.tcp.TCP):

            # Set the TCP data
            tcp = ip.data

            # Pull out flags information (flags are packed into the flags field, so use bitmasks)
            urg = bool(tcp.flags & dpkt.tcp.TH_URG)
            ack = bool(tcp.flags & dpkt.tcp.TH_ACK)
            psh = bool(tcp.flags & dpkt.tcp.TH_PUSH)
            rst = bool(tcp.flags & dpkt.tcp.TH_RST)
            syn = bool(tcp.flags & dpkt.tcp.TH_SYN)
            fin = bool(tcp.flags & dpkt.tcp.TH_FIN)

            # Pull out fragment information (offset is packed into the off field, so use bitmasks)
            frag_offset = tcp.off & dpkt.tcp.TCP_OPT_MAX

            # Print out the info
            print('Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp)))
            print('Ethernet Frame: ', mac_to_str(eth.src), mac_to_str(eth.dst), eth.type)
            print('IP: %s -> %s   (len=%d ttl=%d)' %
                    (inet_to_str(ip.src), inet_to_str(ip.dst), ip.len, ip.ttl))
            print('TCP: %d -> %d   (seq=%d ack=%d urg=%d ack=%d psh=%d rst=%d syn=%d fin=%d offset=%d)' %
                    (tcp.sport, tcp.dport, tcp.seq, tcp.ack, urg, ack, psh, rst, syn, fin, frag_offset))
            if tcp.data.hex() != '':
                print('TCP payload: ', tcp.data.hex())
            
            # Check for payload spanning acrossed TCP segments
            if not tcp.data.endswith(b'\r\n'):
                print('\nPAYLOAD TRUNCATED! Reassemble TCP segments!\n')