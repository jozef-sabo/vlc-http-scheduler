import unittest
import app.modules.VLC_connector.tools as tools


class Tests(unittest.TestCase):
    def test_validate_ip(self):
        self.assertEqual(tools.validate_ip("http://10.0.0.1"), "10.0.0.1")
        self.assertEqual(tools.validate_ip("https://10.0.0.1/"), "10.0.0.1")

        self.assertEqual(tools.validate_ip("192.168.1.25"), "192.168.1.25")

        self.assertEqual(tools.validate_ip("http://localhost"), "localhost")
        self.assertEqual(tools.validate_ip("http://localhost/"), "localhost")

        with self.assertRaises(ValueError):
            self.assertEqual(tools.validate_ip("https://10.0.0/"), "")
        with self.assertRaises(ValueError):
            self.assertEqual(tools.validate_ip("2610.0.0.0"), "")
        with self.assertRaises(ValueError):
            self.assertEqual(tools.validate_ip("210.0.0.10.0"), "")


if __name__ == '__main__':
    unittest.main()
