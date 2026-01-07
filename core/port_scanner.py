import socket

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}

def scan_ports(target: str, timeout=0.5):
    open_ports = []

    for port, service in COMMON_PORTS.items():
        try:
            s = socket.socket()
            s.settimeout(timeout)
            if s.connect_ex((target, port)) == 0:
                open_ports.append({
                    "port": port,
                    "service": service,
                    "risk": "LOW" if port in [80, 443] else "MEDIUM",
                    "recommendation": f"Review {service} exposure"
                })
            s.close()
        except:
            pass

    return open_ports
