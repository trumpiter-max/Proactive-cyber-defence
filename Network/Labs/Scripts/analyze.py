import dpkt
import sys
import socket

filename = sys.argv[1]

# Open the pcap file in binary mode
with open(filename, 'rb') as f:
    pcap = dpkt.pcap.Reader(f)
    TCPcount = 0
    UDPcount = 0

    # Initialize empty sets for outcoming and incoming IP addresses
    outcoming_ips = set()
    incoming_ips = set()

    # Iterate over each packet in the pcap file
    for ts, buf in pcap:
        # Parse the packet using dpkt
        eth = dpkt.ethernet.Ethernet(buf)
        if eth.type == dpkt.ethernet.ETH_TYPE_IP:
            ip = eth.data
            transport_layer = ip.data

        # Check if the packet is TCP or UDP
        if isinstance(transport_layer, dpkt.tcp.TCP):
            TCPcount += 1
        if isinstance(transport_layer, dpkt.udp.UDP):
            UDPcount += 1

        # Check if the packet is TCP or UDP
        if isinstance(ip.data, dpkt.tcp.TCP) or isinstance(ip.data, dpkt.udp.UDP):
            # Get the source and destination IP addresses
            src_ip = socket.inet_ntoa(ip.src)
            dst_ip = socket.inet_ntoa(ip.dst)
            outcoming_ips.add(src_ip)
            incoming_ips.add(dst_ip)

    print("Outcoming IPs: ", outcoming_ips)
    print("Incoming IPs: ", incoming_ips)

    # Print the number of packets counted
    print("Number of TCP packets: ", TCPcount)
    print("Number of UDP packets: ", UDPcount)