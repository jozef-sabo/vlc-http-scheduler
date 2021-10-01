from .validate_ip import validate_ip
from . import mrl
from . import path


def parse_path(filepath: str) -> path.Path:
    return path.Path(filepath)
