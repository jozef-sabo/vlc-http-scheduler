# import find_system
from . import find_system
# from app.modules.VLC_connector.constants import system_type
# from app.modules.VLC_connector.constants import language
from ...constants import system_type
from ...constants import language


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
            lang = winreg.QueryValueEx(key, "Lang")
            if lang[1] != 1:
                raise ValueError("Init went wrong, please try again later")
            return lang[0]
    except FileNotFoundError as e:
        lang = __get_auto_lang_win()

    return lang


def get_vlc_auto_lang() -> str:
    system = find_system.get_os()

    if system == system_type.WINDOWS or system == system_type.WINDOWS_CYGWIN:
        return __get_auto_lang_win()

    #  TODO: implement more systems


def __get_auto_lang_win() -> str:
    import winreg
    import locale
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\VideoLAN\\VLC") as key:
            auto_lang = winreg.QueryValueEx(key, "Language")
    except FileNotFoundError:
        raise FileNotFoundError("VLC is not installed. Please install VLC from 'https://www.videolan.org/vlc/'")

    if auto_lang[1] != 1:
        raise ValueError("Init went wrong, please try again later")

    try:
        lang = int(auto_lang[0])
    except Exception:
        raise ValueError("Init went wrong, please try again later")

    # lang = lang ^ 0x400 if lang > 0x400 else lang

    try:
        lang = locale.windows_locale[lang]
    except KeyError:
        raise ValueError("Init went wrong, please try again later")

    if lang not in language.languages_with_region:
        lang = lang.split("_")[0]

    return lang


if __name__ == "__main__":
    print(__get_auto_lang_win())
