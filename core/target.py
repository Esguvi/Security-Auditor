import re

def sanitize_target(target: str) -> str:
    target = target.strip().lower()
    if not re.match(r"^[a-z0-9\.\-]+$", target):
        raise ValueError("Invalid target")
    return target
