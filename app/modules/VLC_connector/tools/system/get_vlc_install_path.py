import winreg
from . import find_system
from . import system_type


def get_vlc_install_path() -> str:
    """
    Returns an installation path of VLC.
    :return: Install path of VLC
    :rtype: str
    """
    system = find_system.get_os()

    if system == system_type.WINDOWS or system == system_type.WINDOWS_CYGWIN:
        return __get_path_win()

    #  TODO: implement more systems


def __get_path_win() -> str:
    """
        Returns an installation path of VLC in Windows like OSs.
        :return: Install path of VLC
        :rtype: str
        """
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\VideoLAN\\VLC") as key:
            installation_path = winreg.QueryValueEx(key, "InstallDir")
    except FileNotFoundError as e:
        raise FileNotFoundError("VLC is not installed. Please install VLC from 'https://www.videolan.org/vlc/'")

    if installation_path[1] != 1:
        raise ValueError("Init went wrong, please try again later")

    return installation_path[0]


print(get_vlc_install_path())
