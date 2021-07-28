import os


def prepare_locale_folder() -> tuple:
    init_path = os.path.dirname(os.getcwd())
    out_folder = os.path.abspath(os.path.join(init_path, "./locale"))

    return __create_folder(out_folder)


def prepare_language_folder(locale_path: str, language: str) -> tuple:
    out_folder = os.path.abspath(os.path.join(locale_path, language, "LC_MESSAGES"))
    return __create_folder(out_folder)


def __create_folder(folder: str) -> tuple:
    if os.path.isdir(folder):
        return folder, 0  # 0 -> folder existed

    try:
        os.makedirs(folder)
        return folder, 1  # 1 -> folder didn't exist

    except Exception:  # TODO: Create another folder when this is not accessible
        raise PermissionError("The program isn't allowed to create a directory. Try to run it in admin mode.")
