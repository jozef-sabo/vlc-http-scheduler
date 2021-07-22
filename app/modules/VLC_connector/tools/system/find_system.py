import sys
from . import system_type


def get_os() -> int:
    """
    Gets an Operating System and codes it into predefined constants
    :return: Returns int corresponding to constant name from system_type module
    :rtype: int
    """
    system = system_type.systems.get(sys.platform)
    if not system:
        raise NotImplementedError("Not supported OS is used")
    return system
