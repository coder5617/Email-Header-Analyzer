import ipaddress
import re

def is_valid_ipv4(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except:
        return False

def is_private_ip(ip):
    try:
        obj = ipaddress.IPv4Address(ip)
        return obj.is_private or obj.is_loopback
    except:
        return False

def extract_ip_from_received(raw):
    for pat in [r'\[([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\]', r'from\s+([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)']:
        m = re.search(pat, raw)
        if m and is_valid_ipv4(m.group(1)):
            return m.group(1)
    return None

def extract_ips_from_headers(headers):
    rec = headers.get("Received", [])
    if isinstance(rec, str):
        rec = [rec]
    ips = []
    for r in rec:
        ip = extract_ip_from_received(r)
        if ip and ip not in ips:
            ips.append(ip)
    xo = headers.get("X-Originating-IP", "").strip("[]")
    if xo and is_valid_ipv4(xo) and xo not in ips:
        ips.append(xo)
    return ips
