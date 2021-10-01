import unittest
import os
import shutil
import app.modules.vlc_connector.tools.system.prepare_folder as prepare_folder


class Tests(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        locale_folder = os.path.abspath(os.path.join(os.getcwd(), "../locale"))
        if os.path.isdir(locale_folder):
            shutil.rmtree(locale_folder)

    @classmethod
    def tearDown(cls) -> None:
        locale_folder = os.path.abspath(os.path.join(os.getcwd(), "../locale"))
        if os.path.isdir(locale_folder):
            shutil.rmtree(locale_folder)

    def test_prepare_locale_folder(self):
        locale_folder = os.path.abspath(os.path.join(os.getcwd(), "../locale"))
        out = prepare_folder.prepare_locale_folder()
        self.assertTrue(os.path.isdir(locale_folder))
        self.assertEqual(out[0], locale_folder)
        self.assertEqual(out[1], 1)

    def test_prepare_locale_folder_made(self):
        locale_folder = os.path.abspath(os.path.join(os.getcwd(), "../locale"))
        os.makedirs(locale_folder)
        out = prepare_folder.prepare_locale_folder()
        self.assertTrue(os.path.isdir(os.path.abspath(os.path.join(os.getcwd(), "../locale"))))
        self.assertEqual(out[0], locale_folder)
        self.assertEqual(out[1], 0)

    def test_prepare_language_folder(self):
        language_folder = os.path.abspath(os.path.join(os.getcwd(), "../locale/sk/LC_MESSAGES"))
        locale_folder = prepare_folder.prepare_locale_folder()
        language_folder_out = prepare_folder.prepare_language_folder(locale_folder[0], "sk")

        self.assertTrue(os.path.isdir(language_folder))
        self.assertEqual(language_folder_out[0], language_folder)
        self.assertEqual(language_folder_out[1], 1)

    def test_prepare_language_folder_made(self):
        language_folder = os.path.abspath(os.path.join(os.getcwd(), "../locale/sk/LC_MESSAGES"))
        locale_folder = prepare_folder.prepare_locale_folder()
        os.makedirs(language_folder)

        language_folder_out = prepare_folder.prepare_language_folder(locale_folder[0], "sk")

        self.assertTrue(os.path.isdir(language_folder))
        self.assertEqual(language_folder_out[0], language_folder)
        self.assertEqual(language_folder_out[1], 0)
