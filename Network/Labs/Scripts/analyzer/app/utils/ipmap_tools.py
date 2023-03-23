from scapy.all import *
import requests
import os

def getmyip():
    try:
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]
    except:
        return None

def get_geo(ip):
    try:
        ip_address = getmyip(ip)
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        location_data = {
            "ip": ip_address,
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name")
        }
        return location_data
    except:
        return None

def get_ipmap(PCAPS, host_ip):
    geo_dict = dict()
    ip_value_dict = dict()
    ip_value_list = list()
    for pcap in PCAPS:
        if pcap.haslayer(IP):
            src = pcap.getlayer(IP).src
            dst = pcap.getlayer(IP).dst
            pcap_len = len(corrupt_bytes(pcap))
            if src == host_ip:
                oip = dst
            else:
                oip = src
            if oip in ip_value_dict:
                ip_value_dict[oip] += pcap_len
            else:
                ip_value_dict[oip] = pcap_len
    for ip, value in ip_value_dict.items():
        geo_list = get_geo(ip)
        if geo_list:
            geo_dict[geo_list[0]] = [geo_list[1], geo_list[2]]
            Mvalue = str(float('%.2f'%(value/1024.0)))+':'+ip
            ip_value_list.append({geo_list[0]:Mvalue})
        else:
            pass
    return [geo_dict, ip_value_list]