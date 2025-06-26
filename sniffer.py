from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime

recent_packets = []
blacklisted_ips = ["123.49.53.190", "45.67.23.11"]

def process_packet(packet):
    if IP in packet:
        proto = "TCP" if TCP in packet else "UDP" if UDP in packet else "Other"
        src = packet[IP].src
        dst = packet[IP].dst
        alert = "Blacklisted IP" if src in blacklisted_ips or dst in blacklisted_ips else ""
        recent_packets.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "protocol": proto,
            "src": src,
            "dst": dst,
            "alert": alert
        })
        if len(recent_packets) > 100:
            recent_packets.pop(0)

def start_sniffing():
    sniff(prn=process_packet, store=False)

def get_recent_packets():
    return list(recent_packets)
