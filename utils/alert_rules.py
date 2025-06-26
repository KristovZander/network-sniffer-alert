# utils/alert_rules.py

# Example suspicious IPs and ports (can be extended)
blacklisted_ips = {"192.168.1.10", "10.0.0.99","123.49.53.190", "181.214.153.62"}
suspicious_ports = {6667, 31337, 12345}  # Common for malware/trojans

def is_suspicious(packet):
    src = packet.get("src")
    dst = packet.get("dst")
    proto = packet.get("protocol")
    port = packet.get("sport") if "sport" in packet else None

    if src in blacklisted_ips or dst in blacklisted_ips:
        return "Blacklisted IP"
    if port in suspicious_ports:
        return f"Suspicious Port: {port}"
    return None
