import re

__regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[1-9])$"


def validate_ip(ip: str) -> str:
    if ip.strip() == "":
        return ""
    if ip.startswith("https://"):
        ip = ip[8:]

    if ip.startswith("http://"):
        ip = ip[7:]

    ip = ip.strip("/")

    if ip == "localhost":
        return "localhost"

    if not re.search(__regex, ip):
        raise ValueError("IP address is not correct")

    return ip
