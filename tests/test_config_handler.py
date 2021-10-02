import unittest
import app.modules.config_handler as config_handler
import app.modules.misc.errors as errors
import os
import shutil
import sys


class Tests(unittest.TestCase):
    def test_folder_actions(self):
        self.assertFalse(config_handler.config_folder_exists("./config"))

        self.assertEqual(config_handler.create_config_folder("./config"), (os.path.join(os.getcwd(), "config"), 0))
        self.assertEqual(config_handler.create_config_folder("./config"), (os.path.join(os.getcwd(), "config"), 1))

        self.assertEqual(config_handler.config_folder_exists("./config"), os.path.join(os.getcwd(), "config"))

    @unittest.skipUnless(sys.platform in ["win32", "cygwin"],
                         "Tested path is not possible only on Windows-like machines")
    def test_permission_error_win(self):
        with self.assertRaises(PermissionError):
            config_handler.create_config_folder("A:\\config")

    @unittest.skipIf(sys.platform in ["win32", "cygwin"], "Tested path is not possible only on Unix-like machines")
    def test_permission_error_unix(self):
        with self.assertRaises(PermissionError):
            config_handler.create_config_folder("/root/config")

    def tearDown(self) -> None:
        dir_to_remove = os.path.join(os.getcwd(), "config")
        if os.path.isdir(dir_to_remove):
            shutil.rmtree(dir_to_remove)

    def test_export_config_json(self):
        config_handler.export_config({}, "./config", "conf", "j+")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "{}")

        config_handler.export_config([], "./config", "conf", "j")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "[]")

        config_handler.export_config({}, "./config", "conf", "jp")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "{}")

        config_handler.export_config([], "./config", "conf", "jp")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "[]")

        config_handler.export_config({}, "./config", "conf", "jo")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "e30=")

        config_handler.export_config([], "./config", "conf", "jo")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "W10=")

        config_handler.export_config({"data": "a"}, "./config", "conf", "j")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """{"data": "a"}""")

        config_handler.export_config(["a"], "./config", "conf", "j")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """["a"]""")

        config_handler.export_config({"data": "a"}, "./config", "conf", "jp")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """{\r\n    "data": "a"\r\n}""")

        config_handler.export_config(["a"], "./config", "conf", "jp")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """[\r\n    "a"\r\n]""")

        config_handler.export_config({"data": "a"}, "./config", "conf", "jpo")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "ewogICAgImRhdGEiOiAiYSIKfQ==")

        config_handler.export_config(["a"], "./config", "conf", "jpo")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "WwogICAgImEiCl0=")

        config_handler.export_config({"data": "a", "numbers": [1, 2]}, "./config", "conf", "j")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """{"data": "a", "numbers": [1, 2]}""")

        config_handler.export_config(["a", 1], "./config", "conf", "j")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """["a", 1]""")

        config_handler.export_config({"data": "a", "numbers": [1, 2]}, "./config", "conf", "jp")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), '{\r\n    "data": "a",\r\n    "numbers": [\r\n        1,\r\n        2\r\n    ]'
                                       '\r\n}')

        config_handler.export_config(["a", 1], "./config", "conf", "jp")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """[\r\n    "a",\r\n    1\r\n]""")

        config_handler.export_config({"data": "a", "numbers": [1, 2]}, "./config", "conf", "jpo")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(
                f.read(),
                "ewogICAgImRhdGEiOiAiYSIsCiAgICAibnVtYmVycyI6IFsKICAgICAgICAxLAogICAgICAgIDIKICAgIF0KfQ=="
            )

        config_handler.export_config(["a", 1], "./config", "conf", "jpo")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "WwogICAgImEiLAogICAgMQpd")

        config_handler.export_config(["a", 1], "./config", "conf")
        with open(os.path.join("./config", "conf.json"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """["a", 1]""")

        with self.assertRaises(ValueError):
            config_handler.export_config(["a", 1], "./config", "conf", "abc")

    def test_export_config_xml(self):
        config_handler.export_config({}, "./config", "conf", "x+")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), '<?xml version="1.0" ?><root/>')

        config_handler.export_config([], "./config", "conf", "x")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), '<?xml version="1.0" ?><root/>')

        config_handler.export_config({}, "./config", "conf", "xp")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), '<?xml version="1.0" ?>\r\n<root/>\r\n')

        config_handler.export_config([], "./config", "conf", "xp")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), '<?xml version="1.0" ?>\r\n<root/>\r\n')

        config_handler.export_config({}, "./config", "conf", "xo")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "PD94bWwgdmVyc2lvbj0iMS4wIiA/Pjxyb290Lz4=")

        config_handler.export_config([], "./config", "conf", "xo")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "PD94bWwgdmVyc2lvbj0iMS4wIiA/Pjxyb290Lz4=")

        config_handler.export_config({"data": "a"}, "./config", "conf", "x")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """<?xml version="1.0" ?><root><data type="str">a</data></root>""")

        config_handler.export_config(["a"], "./config", "conf", "x")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """<?xml version="1.0" ?><root><item type="str">a</item></root>""")

        config_handler.export_config({"data": "a"}, "./config", "conf", "xp")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """<?xml version="1.0" ?>\r\n<root>\r\n\t<data type="str">a</data>\r\n""" +
                             """</root>\r\n""")

        config_handler.export_config(["a"], "./config", "conf", "xp")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """<?xml version="1.0" ?>\r\n<root>\r\n\t<item type="str">a</item>\r\n""" +
                             """</root>\r\n""")

        config_handler.export_config({"data": "a"}, "./config", "conf", "xpo")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "PD94bWwgdmVyc2lvbj0iMS4wIiA/Pgo8cm9vdD4KCTxkYXRhIHR5cGU9InN0ciI+YTwvZGF0YT4"
                                       "KPC9yb290Pgo=")

        config_handler.export_config(["a"], "./config", "conf", "xpo")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "PD94bWwgdmVyc2lvbj0iMS4wIiA/Pgo8cm9vdD4KCTxpdGVtIHR5cGU9InN0ciI+YTwvaXRlbT4"
                                       "KPC9yb290Pgo=")

        config_handler.export_config({"data": "a", "numbers": [1, 2]}, "./config", "conf", "x")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """<?xml version="1.0" ?><root><data type="str">a</data><numbers """ +
                             """type="list"><item type="int">1</item><item type="int">2</item></numbers></root>""")

        config_handler.export_config(["a", 1], "./config", "conf", "x")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), """<?xml version="1.0" ?><root><item type="str">a</item><item""" +
                             """ type="int">1</item></root>""")

        config_handler.export_config({"data": "a", "numbers": [1, 2]}, "./config", "conf", "xp")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), '<?xml version="1.0" ?>\r\n<root>\r\n\t<data type="str">a</data>\r\n\t'
                                       '<numbers type="list">\r\n\t\t<item type="int">1</item>\r\n\t\t'
                                       '<item type="int">2</item>\r\n\t</numbers>\r\n</root>\r\n'
                             )

        config_handler.export_config(["a", 1], "./config", "conf", "xp")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), '<?xml version="1.0" ?>\r\n<root>\r\n\t<item type="str">a</item>\r\n\t'
                                       '<item type="int">1</item>\r\n</root>\r\n'
                             )

        config_handler.export_config({"data": "a", "numbers": [1, 2]}, "./config", "conf", "xpo")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(
                f.read(),
                "PD94bWwgdmVyc2lvbj0iMS4wIiA/Pgo8cm9vdD4KCTxkYXRhIHR5cGU9InN0ciI+YTwvZGF0YT4KCTxudW1iZXJzIHR5cGU9Imxpc"
                "3QiPgoJCTxpdGVtIHR5cGU9ImludCI+MTwvaXRlbT4KCQk8aXRlbSB0eXBlPSJpbnQiPjI8L2l0ZW0+Cgk8L251bWJlcnM+"
                "Cjwvcm9vdD4K"
            )

        config_handler.export_config(["a", 1], "./config", "conf", "xpo")
        with open(os.path.join("./config", "conf.xml"), "r", newline="\r\n") as f:
            self.assertEqual(f.read(), "PD94bWwgdmVyc2lvbj0iMS4wIiA/Pgo8cm9vdD4KCTxpdGVtIHR5cGU9InN0ciI+YTwvaXRlbT4K"
                                       "CTxpdGVtIHR5cGU9ImludCI+MTwvaXRlbT4KPC9yb290Pgo=")

    def test_import_config_json(self):
        config_handler.create_config_folder("./config")

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("{}")
        self.assertEqual(config_handler.import_config("./config", "conf.json", "j"), {})

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("[]")
        self.assertEqual(config_handler.import_config("./config", "conf.json", "j"), [])

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("e30=")
        self.assertEqual(config_handler.import_config("./config", "conf.json", "jo"), {})

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("W10=")
        self.assertEqual(config_handler.import_config("./config", "conf.json", "jo"), [])

    def test_import_config_xml(self):
        config_handler.create_config_folder("./config")

        with open(os.path.join("./config", "conf.xml"), "w+", newline="\r\n") as f:
            f.write("""<?xml version="1.0" ?><root/>""")
        self.assertEqual(config_handler.import_config("./config", "conf.xml", "x"), {})

        with open(os.path.join("./config", "conf.xml"), "w+", newline="\r\n") as f:
            f.write("PD94bWwgdmVyc2lvbj0iMS4wIiA/Pjxyb290Lz4=")
        self.assertEqual(config_handler.import_config("./config", "conf.xml", "xo"), {})

        with open(os.path.join("./config", "conf.xml"), "w+", newline="\r\n") as f:
            f.write("""<?xml version="1.0" ?>\r\n<root/>\r\n""")
        self.assertEqual(config_handler.import_config("./config", "conf.xml", "x"), {})

    def test_import_config_auto_recognise_json(self):
        config_handler.create_config_folder("./config")

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("{}")
        self.assertEqual(config_handler.import_config("./config", "conf.json"), {})

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("[]")
        self.assertEqual(config_handler.import_config("./config", "conf.json"), [])

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("e30=")
        self.assertEqual(config_handler.import_config("./config", "conf.json"), {})

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("W10=")
        self.assertEqual(config_handler.import_config("./config", "conf.json"), [])

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("{}")
        self.assertEqual(config_handler.import_config("./config", "conf"), {})

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("[]")
        self.assertEqual(config_handler.import_config("./config", "conf"), [])

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("e30=")
        self.assertEqual(config_handler.import_config("./config", "conf"), {})

        with open(os.path.join("./config", "conf.json"), "w+", newline="\r\n") as f:
            f.write("W10=")
        self.assertEqual(config_handler.import_config("./config", "conf"), [])

    def test_import_config_auto_recognise_xml(self):
        config_handler.create_config_folder("./config")

        with open(os.path.join("./config", "conf.xml"), "w+", newline="\r\n") as f:
            f.write("""<?xml version="1.0" ?><root/>""")
        self.assertEqual(config_handler.import_config("./config", "conf.xml"), {})

        with open(os.path.join("./config", "conf.xml"), "w+", newline="\r\n") as f:
            f.write("PD94bWwgdmVyc2lvbj0iMS4wIiA/Pjxyb290Lz4=")
        self.assertEqual(config_handler.import_config("./config", "conf.xml"), {})

        with open(os.path.join("./config", "conf.xml"), "w+", newline="\r\n") as f:
            f.write("""<?xml version="1.0" ?><root/>""")
        self.assertEqual(config_handler.import_config("./config", "conf"), {})

        with open(os.path.join("./config", "conf.xml"), "w+", newline="\r\n") as f:
            f.write("PD94bWwgdmVyc2lvbj0iMS4wIiA/Pjxyb290Lz4=")
        self.assertEqual(config_handler.import_config("./config", "conf"), {})

    # noinspection DuplicatedCode
    def test_from_to_json(self):
        args_path = ["./config", "conf"]

        test_data = {}
        conf_path = config_handler.export_config(test_data, *args_path, "j+")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)
        conf_path = config_handler.export_config(test_data, *args_path, "jo")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)

        test_data = {"data": "a"}
        conf_path = config_handler.export_config(test_data, *args_path, "j")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)
        conf_path = config_handler.export_config(test_data, *args_path, "jo")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)

        test_data = {"data": "a", "numbers": [1, 2], "recursive_dict": {"data": "a", "numbers": [1, 2]}}
        conf_path = config_handler.export_config(test_data, *args_path, "j")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)
        conf_path = config_handler.export_config(test_data, *args_path, "jo")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)

        test_data = []
        conf_path = config_handler.export_config(test_data, *args_path, "j+")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)
        conf_path = config_handler.export_config(test_data, *args_path, "jo")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)

        test_data = ["a"]
        conf_path = config_handler.export_config(test_data, *args_path, "j")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)
        conf_path = config_handler.export_config(test_data, *args_path, "jo")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)

        test_data = ["a", 1]
        conf_path = config_handler.export_config(test_data, *args_path, "j")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)
        conf_path = config_handler.export_config(test_data, *args_path, "jo")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)

    # noinspection DuplicatedCode
    def test_from_to_xml(self):
        args_path = ["./config", "conf"]

        test_data = {}
        conf_path = config_handler.export_config(test_data, *args_path, "x+")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)
        conf_path = config_handler.export_config(test_data, *args_path, "xo")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)

        test_data = {"data": "a"}
        conf_path = config_handler.export_config(test_data, *args_path, "x")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)
        conf_path = config_handler.export_config(test_data, *args_path, "xo")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)

        test_data = {"data": "a", "numbers": [1, 2], "recursive_dict": {"data": "a", "numbers": [1, 2]}}
        conf_path = config_handler.export_config(test_data, *args_path, "x")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)
        conf_path = config_handler.export_config(test_data, *args_path, "xo")[0]
        self.assertEqual(config_handler.import_config(conf_path, " "), test_data)

    def test_import_config_errors(self):
        with self.assertRaises(errors.ConfigFolderMissingError):
            config_handler.import_config("./config", "test")

        config_handler.create_config_folder("./config")
        with self.assertRaises(errors.ConfigFileMissingError):
            config_handler.import_config("./config", "test")

        config_handler.export_config({}, "./config", "test", "j")
        with self.assertRaises(ValueError):
            config_handler.import_config("./config", "test.json", "JPO")

        config_handler.export_config({}, "./config", "test", "j")
        with self.assertRaises(ValueError):
            config_handler.import_config("./config", "test.json", "po")

        with open(os.path.join("./config", "test"), "w+", newline="\r\n") as f:
            f.write("1, [2]")
        with self.assertRaises(ValueError):
            config_handler.import_config("./config", "test")

        with open(os.path.join("./config", "test"), "w+", newline="\r\n") as f:
            f.write("1, 2")
        with self.assertRaises(ValueError):
            config_handler.import_config("./config", "test")


if __name__ == '__main__':
    unittest.main()
