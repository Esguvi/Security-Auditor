from core.port_scanner import scan_ports
from core.headers_scanner import scan_headers
from core.tls_scanner import check_tls

def run_remote_audit(target):
    ports = scan_ports(target)
    headers = scan_headers(target)
    tls = check_tls(target)

    # Risk Score
    score = 100
    for p in ports:
        if p["risk"] == "MEDIUM":
            score -= 10
        elif p["risk"] == "HIGH":
            score -= 30
    if headers:
        score -= len(headers) * 5
    if tls is None:
        score -= 20
    score = max(score, 0)

    return {
        "target": target,
        "ports": ports,
        "headers": headers,
        "tls": tls,
        "score": score,
        "type": "REMOTE"
    }
