from core.port_scanner import scan_ports

def run_local_audit(target):
    ports = scan_ports(target)

    # Calcular Risk Score simple
    score = 100
    for p in ports:
        if p["risk"] == "MEDIUM":
            score -= 10
        elif p["risk"] == "HIGH":
            score -= 30
    score = max(score, 0)

    return {
        "target": target,
        "ports": ports,
        "score": score,
        "type": "LOCAL"
    }
