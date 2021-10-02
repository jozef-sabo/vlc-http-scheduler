import os
from typing import *
import base64
from . import url_processor
from .misc import errors


def create_config_folder(path: str) -> tuple:
    """
    Creates config folder at provided path.
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
    """
    Checks if config folder exists. If yes, returns an absolute path.
    :param path: Relative or absolute path of config folder
    :return: Absolute path of config folder in case folder exists, otherwise False
    """
    path = os.path.abspath(path)
    if os.path.isdir(path):
        return path

    return False


modes = ["+", "j", "x", "p", "o"]


def export_config(data: Union[dict, list], path: str, filename: str, mode: str = None) -> list:
    """
    Exports provided list or dictionary to file. Export can be customized by modes. If mode not provided, export is
    performed in JSON format without prettying nor obfuscating.
    Modes:
        - "+" creates config folder if not existing
        - "j" export in JSON
        - "x" export in XML
        - "p" prettify config
        - "o" obfuscates config with base64
    :param data: List or dictionary to export
    :param path: Path of config folder.
    :param filename: Name of the file. Extension is always added.
    :param mode: [Optional] Modes can customize the config file look. More modes can be used simultaneously.

    :return: List of path(s) of exported file(s)
    """
    path = os.path.abspath(path)

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


def import_config(filepath: str, filename: str, mode: str = None) -> Union[dict, list]:
    """
    Imports config from a file. Modes can be provided to help the system with importing. If using auto-recognition
    approach, JSON mode is preferred.
    Modes:
        - "j" import from JSON
        - "x" import from XML
        - "o" obfuscated config with base64
    :param filepath: Folder where the config file is stored.
    :param filename: Filename of the config file. Can be provided with or without an extension.
    :param mode: [Optional] Providing a mode speeds up the config file conversion.
    More modes can be used simultaneously. If none provided, system tries to find mode used for export. If none found,
    exception is raised.

    :return: (List or d)/Dictionary imported from file.
    """

    full_path = os.path.join(os.path.abspath(filepath), filename) if filename.strip() else os.path.abspath(filepath)
    if not mode:  # recognition process 1/3 - intentionally raising an exception later, if a not existent file
        if not os.path.isfile(full_path):
            tested_path = full_path + ".xml"
            if os.path.isfile(tested_path):
                full_path = tested_path

            tested_path = full_path + ".json"
            if os.path.isfile(tested_path):
                full_path = tested_path

    path = url_processor.parse_path(full_path)
    obfuscated = False
    filetype = ""

    if not os.path.isdir(path.path):
        raise errors.ConfigFolderMissingError("Config folder ({}) for '{}' was not found.".format(filepath, filename))
    if not os.path.isfile(path.full):
        raise errors.ConfigFileMissingError(
            "Config file '{}' was not found. No information were extracted.".format(filename))

    if mode:
        for character in mode:
            if character not in modes:
                raise ValueError("Invalid characters in mode {}.".format(mode))

    if mode:
        if "x" in mode:
            filetype = "xml"
        if "j" in mode:
            filetype = "json"

        if not filetype:
            raise ValueError("Filetype not provided in mode {}. Valid filetypes are JSON (j) and XML (x)".format(mode))

    with open(path.full, "r", encoding="UTF-8", newline="\r\n") as config_import:
        config_text = config_import.read()

    if not mode:  # recognition process 2/3
        if len(config_text) % 4 == 0:  # if text in base64, its length must be divisible by 4
            obfuscated = True
            for character in config_text:
                if character in ["<", ":", "{", "["]:
                    obfuscated = False
                    break

    if mode and "o" in mode:
        obfuscated = True

    if obfuscated:
        config_text = base64.b64decode(bytes(config_text, "UTF-8")).decode("UTF-8")

    config_text.strip()

    if not mode:  # recognition process 3/3
        if config_text[0] in ["{", "["]:
            filetype = "json"
        if config_text[:14] == "<?xml version=":
            filetype = "xml"

        if not filetype:
            raise ValueError("Cannot automatically recognize type of the config file '{}'".format(filename))

    if filetype == "json":
        import json
        return json.loads(config_text)

    if filetype == "xml":
        from app.modules.misc import xmltodict
        return xmltodict.xmltodict(config_text)
