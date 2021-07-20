import sys
import system_type


def get_os() -> int:
    system = system_type.systems.get(sys.platform)
    if not system:
        raise NotImplementedError("Not supported OS is used")
    return system
