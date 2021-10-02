from .validate_ip import validate_ip
from . import path as path
from . import mrl


def parse_path(filepath: str) -> path.Path:
    return path.Path(filepath)
