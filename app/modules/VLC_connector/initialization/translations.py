from app.modules.VLC_connector.tools import system as system
import os
import gettext


def get_translations(operating_system=int):  # only for Windows, OS not yet used
    path = system.get_vlc_install_path()
    locale_path = os.path.join(path, "locale")
    lang_folders = os.listdir(locale_path)
    # lang_folders = ["sk"]

    for language in lang_folders:
        export_important_strings(locale_path, language)


def export_important_strings(locale_path: str, folder: str):
    lang = gettext.translation('vlc', localedir=locale_path, languages=[folder])
    print(folder, lang.gettext("Decoded format"))


if __name__ == "__main__":
    get_translations()
