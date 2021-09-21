
class InitError(Exception):
    """Error raised during first app initialization"""
    pass


class ConfigFolderMissingError(RuntimeError):
    """Config folder was not found"""
    pass


class ConfigFileMissingError(RuntimeError):
    """Config file was not found"""
    pass
