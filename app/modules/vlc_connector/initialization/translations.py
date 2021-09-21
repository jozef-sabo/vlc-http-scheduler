from app.modules.vlc_connector.tools import system as system
import strings_to_translate
import os
import gettext
import polib


def get_translations(operating_system=int):  # only for Windows, OS not yet used
    path = system.get_vlc_install_path()
    locale_path = os.path.join(path, "locale")
    lang_folders = os.listdir(locale_path)
    # lang_folders = ["sk"]

    locale_folder = system.prepare_locale_folder()[0]

    for language in lang_folders:
        export_important_strings(locale_path, language, locale_folder)

    return locale_folder


def export_important_strings(locale_path: str, language: str, out_folder="./locale"):
    lang = gettext.translation('vlc', localedir=locale_path, languages=[language])
    str_to_trs = strings_to_translate.important_strings
    out_folder = os.path.abspath(out_folder)

    curr_lang_folder = system.prepare_language_folder(out_folder, language)[0]
    mo_lang_file = os.path.join(curr_lang_folder, "vlc_connector.mo")
    mo_lang_to_eng_file = os.path.join(curr_lang_folder, "vlc_connector_to_eng.mo")

    po_file_to_eng = polib.POFile()
    po_file = polib.POFile()

    for translatable in str_to_trs:
        translated_string = lang.gettext(translatable)
        po_file.append(polib.POEntry(
            msgid=translatable,
            msgstr=translated_string
        ))
        po_file_to_eng.append(polib.POEntry(
            msgid=translated_string,
            msgstr=translatable
        ))

    po_file.save_as_mofile(mo_lang_file)
    po_file_to_eng.save_as_mofile(mo_lang_to_eng_file)

    # curr_lang_file = os.path.join(curr_lang_folder, "vlc_connector.po")
    # curr_lang_to_eng_file = os.path.join(curr_lang_folder, "vlc_connector.po")
    # po_file.save(curr_lang_file) #  If anybody want also .PO file
    # po_file.save(curr_lang_to_eng_file)

    #  OLD, NOT EVERYTIME WORKING METHOD  # (start)
    # with open(curr_lang_file, "w+", encoding="UTF-8") as out_file:
    #     for translatable in str_to_trs:
    #         out_file.write('msgid "{}"\n'.format(translatable))
    #         out_file.write('msgstr "{}"\n\n'.format(lang.gettext(translatable)))

    # convert_po_to_mo(curr_lang_file, mo_lang_file)


# def convert_po_to_mo(po_file_path: str, mo_file_path: str):
#     po_file = polib.pofile(po_file_path)
#     po_file.save_as_mofile(mo_file_path)
#  OLD, NOT EVERYTIME WORKING METHOD  # (end)


if __name__ == "__main__":
    print(system.get_vlc_lang())
