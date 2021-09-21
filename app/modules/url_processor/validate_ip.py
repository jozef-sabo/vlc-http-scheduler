import re

__regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[1-9])$"


def validate_ip(ip: str) -> str:
    ip = ip.strip()
    if ip == "":
        return ""

    split_ip = ip.split("//")
    ip = split_ip[-1]
    ip = ip.strip("/")

    if ip == "localhost":
        return "localhost"

    if not re.search(__regex, ip):
        raise ValueError("IP address is not correct")

    return ip
