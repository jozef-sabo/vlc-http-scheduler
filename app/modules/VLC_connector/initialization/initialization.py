from app.modules.VLC_connector.tools import system as system
from app.modules.VLC_connector.initialization import get_translations
import configparser


def initialization():
    os = system.get_os()
    locale_folder = get_translations(os)


if __name__ == "__main__":
    initialization()
