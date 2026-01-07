import ssl
import socket

def check_tls(target):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=target) as s:
            s.connect((target, 443))
            return s.version()
    except:
        return None
