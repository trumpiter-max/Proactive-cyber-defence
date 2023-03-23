import sys
from scapy.all import *
import requests
import hashlib

def write_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

def get_file_hash(file):
    with open(file, 'rb') as f:
        data = f.read()
        md5 = hashlib.md5(data).hexdigest()
        sha1 = hashlib.sha1(data).hexdigest()
        sha256 = hashlib.sha256(data).hexdigest()
    return {'md5': md5, 'sha1': sha1, 'sha256': sha256}

# Function to extract IP addresses and domains from packets
def get_ip(packet, ip_set_incoming, ip_set_outgoing, domain_set): 
    if IP in packet:
        ip_set_outgoing.append(packet[IP].src)
        ip_set_incoming.append(packet[IP].dst)
    if TCP in packet:
        if packet.haslayer(Raw):
            # Extract domains from HTTP requests
            raw = packet[TCP].payload.load.decode('utf-8', errors='ignore')
            domains = re.findall(r'Host: (.*?)\\r\\n', raw)
            domain_set += domains

def extract_ip(packets):
    ip_set_incoming = []
    ip_set_outgoing = []
    domain_set = []

    for packet in packets:
        get_ip(packet, ip_set_incoming, ip_set_outgoing, domain_set)

    # Remove duplicates
    ip_set_incoming = list(set(ip_set_incoming))
    ip_set_outgoing = list(set(ip_set_outgoing))
    domain_set = list(set(domain_set))

    result = "## IP addresses and domains from the pcap file \n"
    result += "### Incoming IP addresses from the pcap file: " 
    if len(ip_set_incoming) == 0:
        result += "\n\n No incoming IP addresses found \n\n"
    else:
        result += "\n\n"
        for ip in ip_set_incoming:
            result += str(ip) + "\n\n"

    result += "\n\n ### Outgoing IP addresses from the pcap file: " 
    if len(ip_set_outgoing) == 0:
        result += "\n\n No outgoing IP addresses found \n\n"
    else:
        result += "\n\n"
        for ip in ip_set_outgoing:
            result += str(ip) + "\n\n"

    result += "\n\n ### Relative domains from the pcap file: "
    if len(domain_set) == 0:
        result += "\n\n No domains found \n\n"
    else:
        result += "\n\n"
        for domain in domain_set:
            result += str(domain) + "\n\n"

    write_file("./ioc.md", result)

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <pcap file>")
        sys.exit(1)

    filename = sys.argv[1]
    packets = rdpcap(filename)  
    extract_ip(packets)

if __name__ == '__main__':
    main()