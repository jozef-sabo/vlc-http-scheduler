from . import find_system
from ...constants import system_type


def get_vlc_lang() -> str:
    """
    Returns a current set VLC language.
    :return: VLC language in iso-639 format
    :rtype: str
    """
    system = find_system.get_os()

    if system == system_type.WINDOWS or system == system_type.WINDOWS_CYGWIN:
        return __get_lang_win()

    #  TODO: implement more systems


def __get_lang_win() -> str:
    """
        Returns a current set VLC language in Windows like OSs.
        :return: VLC language in iso-639 format
        :rtype: str
        """
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\VideoLAN\\VLC") as key:
            installation_path = winreg.QueryValueEx(key, "Lang")
    except FileNotFoundError as e:
        return "auto"

    if installation_path[1] != 1:
        raise ValueError("Init went wrong, please try again later")

    return installation_path[0]
