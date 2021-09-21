import os
from typing import *
import base64


def create_config_folder(path: str) -> tuple:
    """

    :param path: Relative or absolute path of config folder
    :return: Tuple containing final path and status
    """

    path = os.path.abspath(path)
    if config_folder_exists(path):
        return path, 1  # folder existed

    try:
        os.makedirs(path)
    except Exception:  # TODO: Create another folder when this is not accessible
        raise PermissionError("The program isn't allowed to create a directory. Try to run it in admin mode.")
    else:
        return path, 0  # 1 -> folder didn't exist


def config_folder_exists(path: str) -> Union[str, bool]:
    path = os.path.abspath(path)
    if os.path.isdir(path):
        return path

    return False


modes = ["+", "j", "x", "p", "o"]


def export_config(data: Union[dict, list], path: str, filename: str, mode: str = None) -> list:
    """
    Modes:
        - "+" creates config folder if not existing
        - "j" export in JSON
        - "x" export in XML
        - "p" prettify config
        - "o" obfuscates config with base64
    :param data:
    :param path:
    :param filename:
    :param mode: Modes can customize the config file look. More modes can be used simultaneously.

    :return:
    """

    prettify = False
    obfuscate = False
    config_files = []

    if mode is None:
        mode = "j"

    for character in mode:
        if character not in modes:
            raise ValueError("Invalid mode {}".format(mode))

    if "+" in mode:
        create_config_folder(path)

    if "p" in mode:
        prettify = True

    if "o" in mode:
        obfuscate = True

    if "j" in mode:
        import json
        config_text = json.dumps(data, indent=4) if prettify else json.dumps(data)

        if obfuscate:
            config_text = base64.b64encode(bytes(config_text, "UTF-8")).decode("UTF-8")
        path_with_filename = os.path.join(path, filename + ".json")
        config_files.append(path_with_filename)

        with open(path_with_filename, "w+", encoding="UTF-8", newline="\r\n") as file:
            file.write(config_text)

    if "x" in mode:
        import dicttoxml
        import xml.dom.minidom as xml

        config_text = dicttoxml.dicttoxml(data)
        config_text = xml.parseString(config_text).toprettyxml() if prettify else xml.parseString(config_text).toxml()

        if obfuscate:
            config_text = base64.b64encode(bytes(config_text, "UTF-8")).decode("UTF-8")

        path_with_filename = os.path.join(path, filename + ".xml")
        config_files.append(path_with_filename)

        with open(path_with_filename, "w+", encoding="UTF-8", newline="\r\n") as file:
            file.write(config_text)

    return config_files
