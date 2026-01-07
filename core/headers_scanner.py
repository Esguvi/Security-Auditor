import requests

def scan_headers(target):
    headers_risks = []
    try:
        r = requests.get(f"http://{target}", timeout=5)
        headers = r.headers

        if "X-Frame-Options" not in headers:
            headers_risks.append("Missing X-Frame-Options")

        if "Content-Security-Policy" not in headers:
            headers_risks.append("Missing CSP")

    except:
        pass

    return headers_risks
