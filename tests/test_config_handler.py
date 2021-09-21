import unittest
import app.modules.config_handler as config_handler
import os
import shutil


class Tests(unittest.TestCase):
    def test_folder_actions(self):
        self.assertFalse(config_handler.config_folder_exists("./config"))

        self.assertEqual(config_handler.create_config_folder("./config"), (os.path.join(os.getcwd(), "config"), 0))
        self.assertEqual(config_handler.create_config_folder("./config"), (os.path.join(os.getcwd(), "config"), 1))

        self.assertEqual(config_handler.config_folder_exists("./config"), os.path.join(os.getcwd(), "config"))

        with self.assertRaises(PermissionError):
            config_handler.create_config_folder("A:\\config")

    def tearDown(self) -> None:
        shutil.rmtree(os.path.join(os.getcwd(), "config"))

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
            self.assertEqual(f.read(), """<?xml version="1.0" ?><root><data type="str">a</data><numbers """+
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


if __name__ == '__main__':
    unittest.main()
