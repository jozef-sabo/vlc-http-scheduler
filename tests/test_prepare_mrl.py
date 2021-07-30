import unittest
import app.modules.VLC_connector.tools.request_processing.prepare_mrl as prepare_mrl


class Tests(unittest.TestCase):
    def test_validate_file(self):
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FILE, "C:/Users/admin/Downloads/film.mp4"),
                         "file:///C:/Users/admin/Downloads/film.mp4")
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FILE, "film.mp4"),
                         "file:///film.mp4")

    def test_validate_ftp(self):
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="1.2.3.4"),
                         "ftp://1.2.3.4/File.mp4")
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="ftp.com"),
                         "ftp://ftp.com/File.mp4")
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="1.2.3.4", port=5678),
                         "ftp://1.2.3.4:5678/File.mp4")
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="ftp.com", port=5678),
                         "ftp://ftp.com:5678/File.mp4")
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="1.2.3.4", username="admin",
                                                 password="administrator"),
                         "ftp://admin:administrator@1.2.3.4/File.mp4")
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="ftp.com", username="admin",
                                                 password="administrator"),
                         "ftp://admin:administrator@ftp.com/File.mp4")
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="1.2.3.4", port=5678,
                                                 username="admin", password="administrator"),
                         "ftp://admin:administrator@1.2.3.4:5678/File.mp4")
        self.assertEqual(prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="ftp.com", port=5678,
                                                 username="admin", password="administrator"),
                         "ftp://admin:administrator@ftp.com:5678/File.mp4")

        with self.assertRaises(ResourceWarning):
            prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4")
        with self.assertRaises(ResourceWarning):
            prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", username="admin")
        with self.assertRaises(ResourceWarning):
            prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", username="admin", password="administrator")
        with self.assertRaises(ResourceWarning):
            prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", password="administrator")
        with self.assertRaises(ResourceWarning):
            prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", username="admin", port=5678)
        with self.assertRaises(ResourceWarning):
            prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", username="admin", password="administrator",
                                    port=5678)
        with self.assertRaises(ResourceWarning):
            prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", password="administrator", port=5678)
        with self.assertRaises(ResourceWarning):
            prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="1.2.3.4", username="admin")
        with self.assertRaises(ResourceWarning):
            prepare_mrl.mrl_prepare(prepare_mrl.uri.FTP, "File.mp4", ip="ftp.com", username="admin")


if __name__ == '__main__':
    unittest.main()
