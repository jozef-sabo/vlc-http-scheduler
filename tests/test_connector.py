import unittest
import app.modules.vlc_connector.connector as connector
import app.modules.vlc_connector.constants.status_codes as status_codes


class Tests(unittest.TestCase):
    def test_connector(self):
        # vlc1 = connector.connect("localhost", "administrator", 8080)  # WILL BE IMPLEMENTED
        vlc2 = connector.connect("localhost", "administrator", check_conn=False)
        # self.assertEqual(vlc1.status, status_codes.OK)  # WILL BE IMPLEMENTED
        self.assertEqual(vlc2.status, status_codes.OK_WITHOUT_TEST)

        # with self.assertRaises(ConnectionError):
        #    vlc2 = connector.connector("localhost", "administrator", 8081)

        # with self.assertRaises(ConnectionRefusedError):
        #    vlc3 = connector.connector("192.168.1.222", "admin", 8080)


if __name__ == '__main__':
    unittest.main()
