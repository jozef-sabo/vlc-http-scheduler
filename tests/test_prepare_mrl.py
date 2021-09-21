import unittest
import app.modules.url_processor.mrl as mrl


class Tests(unittest.TestCase):
    def test_validate_parameters_file(self):
        self.assertEqual(
            mrl.create().from_parameters(
                mrl.uri.FILE,
                "C:/Users/admin/Downloads/film.mp4"
            ).stringify(),
            "file:///C:/Users/admin/Downloads/film.mp4"
        )
        self.assertEqual(
            mrl.create().from_parameters(mrl.uri.FILE, "film.mp4").stringify(),
            "file:///film.mp4"
        )
        self.assertEqual(
            mrl.create().from_parameters(mrl.uri.FILE, "/film.mp4").stringify(),
            "file:///film.mp4"
        )

    def test_validate_parameters_ftp(self):
        self.assertEqual(
            mrl.create().from_parameters(
                mrl.uri.FTP,
                "File.mp4",
                host="1.2.3.4"
            ).using_ip().stringify(),
            "ftp://1.2.3.4/File.mp4")
        self.assertEqual(
            mrl.create().from_parameters(
                mrl.uri.FTP,
                "File.mp4",
                host="ftp.com"
            ).stringify(),
            "ftp://ftp.com/File.mp4")
        self.assertEqual(
            mrl.create().from_parameters(
                mrl.uri.FTP,
                "File.mp4",
                host="1.2.3.4",
                port=5678
            ).using_ip().stringify(),
            "ftp://1.2.3.4:5678/File.mp4")
        self.assertEqual(
            mrl.create().from_parameters(
                mrl.uri.FTP,
                "File.mp4",
                host="ftp.com",
                port=5678
            ).stringify(),
            "ftp://ftp.com:5678/File.mp4")
        self.assertEqual(
            mrl.create().from_parameters(
                mrl.uri.FTP,
                "File.mp4",
                host="1.2.3.4",
                username="admin",
                password="administrator"
            ).using_ip().stringify(),
            "ftp://admin:administrator@1.2.3.4/File.mp4")
        self.assertEqual(
            mrl.create().from_parameters(
                mrl.uri.FTP,
                "File.mp4",
                host="ftp.com",
                username="admin",
                password="administrator"
            ).stringify(),
            "ftp://admin:administrator@ftp.com/File.mp4")
        self.assertEqual(
            mrl.create().from_parameters(
                mrl.uri.FTP,
                "File.mp4",
                host="1.2.3.4",
                port=5678,
                username="admin",
                password="administrator"
            ).using_ip().stringify(),
            "ftp://admin:administrator@1.2.3.4:5678/File.mp4")
        self.assertEqual(
            mrl.create().from_parameters(
                mrl.uri.FTP,
                "File.mp4",
                host="ftp.com",
                port=5678,
                username="admin",
                password="administrator"
            ).stringify(),
            "ftp://admin:administrator@ftp.com:5678/File.mp4")

    def test_validate_url_file(self):
        mrl_to_file = mrl.create().from_url("file:///C:/Users/admin/Downloads/film.mp4")
        self.assertEqual(
            mrl_to_file.stringify(),
            "file:///C:/Users/admin/Downloads/film.mp4"
        )
        self.assertEqual(
            [mrl.uri.FILE, "C:/Users/admin/Downloads/film.mp4"],
            [mrl_to_file.access, mrl_to_file.path.full]
        )

        mrl_to_file = mrl.create().from_url("file:///film.mp4")
        self.assertEqual(
            mrl_to_file.stringify(),
            "file:///film.mp4"
        )
        self.assertEqual(
            [mrl.uri.FILE, "/film.mp4"],
            [mrl_to_file.access, mrl_to_file.path.full]
        )
        mrl_to_file = mrl.create().from_url("C:/Users/admin/Downloads/film.mp4")
        self.assertEqual(
            mrl_to_file.stringify(),
            "file:///C:/Users/admin/Downloads/film.mp4"
        )
        self.assertEqual(
            [mrl.uri.FILE, "C:/Users/admin/Downloads/film.mp4"],
            [mrl_to_file.access, mrl_to_file.path.full]
        )
        mrl_to_file = mrl.create().from_url("film.mp4")
        self.assertEqual(
            mrl_to_file.stringify(),
            "file:///film.mp4"
        )
        self.assertEqual(
            [mrl.uri.FILE, "film.mp4"],
            [mrl_to_file.access, mrl_to_file.path.full]
        )
        mrl_to_file = mrl.create().from_url("/film.mp4")
        self.assertEqual(
            mrl_to_file.stringify(),
            "file:///film.mp4"
        )
        self.assertEqual(
            [mrl.uri.FILE, "/film.mp4"],
            [mrl_to_file.access, mrl_to_file.path.full]
        )

    def test_validate_url_ftp(self):
        mrl_to_ftp_file = mrl.create().from_url("ftp://1.2.3.4/File.mp4").using_ip()
        self.assertEqual(
            mrl_to_ftp_file.stringify(),
            "ftp://1.2.3.4/File.mp4")
        self.assertEqual(
            [mrl.uri.FTP, "1.2.3.4", "File.mp4"],
            [mrl_to_ftp_file.access, mrl_to_ftp_file.host, mrl_to_ftp_file.path.full]
        )

        mrl_to_ftp_file = mrl.create().from_url("ftp://ftp.com/File.mp4")
        self.assertEqual(
            mrl_to_ftp_file.stringify(),
            "ftp://ftp.com/File.mp4")
        self.assertEqual(
            [mrl.uri.FTP, "ftp.com", "File.mp4"],
            [mrl_to_ftp_file.access, mrl_to_ftp_file.host, mrl_to_ftp_file.path.full]
        )

        mrl_to_ftp_file = mrl.create().from_url("ftp://1.2.3.4:5678/File.mp4")
        self.assertEqual(
            mrl_to_ftp_file.stringify(),
            "ftp://1.2.3.4:5678/File.mp4")
        self.assertEqual(
            [mrl.uri.FTP, "1.2.3.4", 5678, "File.mp4"],
            [mrl_to_ftp_file.access, mrl_to_ftp_file.host, mrl_to_ftp_file.port, mrl_to_ftp_file.path.full]
        )

        mrl_to_ftp_file = mrl.create().from_url("ftp://ftp.com:5678/File.mp4")
        self.assertEqual(
            mrl_to_ftp_file.stringify(),
            "ftp://ftp.com:5678/File.mp4")
        self.assertEqual(
            [mrl.uri.FTP, "ftp.com", 5678, "File.mp4"],
            [mrl_to_ftp_file.access, mrl_to_ftp_file.host, mrl_to_ftp_file.port, mrl_to_ftp_file.path.full]
        )

        mrl_to_ftp_file = mrl.create().from_url("ftp://admin:administrator@1.2.3.4/File.mp4")
        self.assertEqual(
            mrl_to_ftp_file.stringify(),
            "ftp://admin:administrator@1.2.3.4/File.mp4")
        self.assertEqual(
            [mrl.uri.FTP, "admin", "administrator", "1.2.3.4", "File.mp4"],
            [
                mrl_to_ftp_file.access,
                mrl_to_ftp_file.username,
                mrl_to_ftp_file.password,
                mrl_to_ftp_file.host,
                mrl_to_ftp_file.path.full]
        )
        mrl_to_ftp_file = mrl.create().from_url("ftp://admin:administrator@ftp.com/File.mp4")
        self.assertEqual(
            mrl_to_ftp_file.stringify(),
            "ftp://admin:administrator@ftp.com/File.mp4")
        self.assertEqual(
            [mrl.uri.FTP, "admin", "administrator", "ftp.com", "File.mp4"],
            [
                mrl_to_ftp_file.access,
                mrl_to_ftp_file.username,
                mrl_to_ftp_file.password,
                mrl_to_ftp_file.host,
                mrl_to_ftp_file.path.full]
        )
        mrl_to_ftp_file = mrl.create().from_url("ftp://admin:administrator@1.2.3.4:5678/File.mp4").using_ip()
        self.assertEqual(
            mrl_to_ftp_file.stringify(),
            "ftp://admin:administrator@1.2.3.4:5678/File.mp4")
        self.assertEqual(
            [mrl.uri.FTP, "admin", "administrator", "1.2.3.4", 5678, "File.mp4"],
            [
                mrl_to_ftp_file.access,
                mrl_to_ftp_file.username,
                mrl_to_ftp_file.password,
                mrl_to_ftp_file.host,
                mrl_to_ftp_file.port,
                mrl_to_ftp_file.path.full]
        )
        mrl_to_ftp_file = mrl.create().from_url("ftp://admin:administrator@ftp.com:5678/File.mp4")
        self.assertEqual(
            mrl_to_ftp_file.stringify(),
            "ftp://admin:administrator@ftp.com:5678/File.mp4")
        self.assertEqual(
            [mrl.uri.FTP, "admin", "administrator", "ftp.com", 5678, "File.mp4"],
            [
                mrl_to_ftp_file.access,
                mrl_to_ftp_file.username,
                mrl_to_ftp_file.password,
                mrl_to_ftp_file.host,
                mrl_to_ftp_file.port,
                mrl_to_ftp_file.path.full]
        )

    def test_validate_path(self):
        mrl_to_ftp_file = mrl.create().from_url("ftp://admin:administrator@ftp.com:5678/Folder1/Folder2/File.mp4")

        self.assertEqual(mrl_to_ftp_file.path.full, "Folder1/Folder2/File.mp4")
        self.assertEqual(mrl_to_ftp_file.path.path, "Folder1/Folder2")
        self.assertEqual(mrl_to_ftp_file.path.file_extension, ".mp4")
        self.assertEqual(mrl_to_ftp_file.path.file_name, "File")
        self.assertEqual(mrl_to_ftp_file.path.full_filename, "File.mp4")

        mrl_to_ftp_file = mrl.create().from_url("ftp://admin:administrator@ftp.com:5678/File.mp4")

        self.assertEqual(mrl_to_ftp_file.path.full, "File.mp4")
        self.assertEqual(mrl_to_ftp_file.path.path, "")
        self.assertEqual(mrl_to_ftp_file.path.file_extension, ".mp4")
        self.assertEqual(mrl_to_ftp_file.path.file_name, "File")
        self.assertEqual(mrl_to_ftp_file.path.full_filename, "File.mp4")

        mrl_to_ftp_file = mrl.create().from_url("ftp://admin:administrator@ftp.com:5678/Folder1/Folder2/File")

        self.assertEqual(mrl_to_ftp_file.path.full, "Folder1/Folder2/File")
        self.assertEqual(mrl_to_ftp_file.path.path, "Folder1/Folder2")
        self.assertEqual(mrl_to_ftp_file.path.file_extension, "")
        self.assertEqual(mrl_to_ftp_file.path.file_name, "File")
        self.assertEqual(mrl_to_ftp_file.path.full_filename, "File")

        mrl_to_ftp_file = mrl.create().from_url("ftp://admin:administrator@ftp.com:5678/Folder1/Folder2/.mp4")

        self.assertEqual(mrl_to_ftp_file.path.full, "Folder1/Folder2/.mp4")
        self.assertEqual(mrl_to_ftp_file.path.path, "Folder1/Folder2")
        self.assertEqual(mrl_to_ftp_file.path.file_extension, "")
        self.assertEqual(mrl_to_ftp_file.path.file_name, ".mp4")
        self.assertEqual(mrl_to_ftp_file.path.full_filename, ".mp4")

    def test_validate_errors(self):
        with self.assertRaises(ResourceWarning):
            mrl.create().from_parameters(mrl.uri.FTP, "File.mp4")
        with self.assertRaises(ResourceWarning):
            mrl.create().from_parameters(mrl.uri.FTP, "File.mp4", username="admin")
        with self.assertRaises(ResourceWarning):
            mrl.create().from_parameters(mrl.uri.FTP, "File.mp4", username="admin", password="administrator")
        with self.assertRaises(ResourceWarning):
            mrl.create().from_parameters(mrl.uri.FTP, "File.mp4", password="administrator")
        with self.assertRaises(ResourceWarning):
            mrl.create().from_parameters(mrl.uri.FTP, "File.mp4", username="admin", port=5678)
        with self.assertRaises(ResourceWarning):
            mrl.create().from_parameters(mrl.uri.FTP, "File.mp4", username="admin", password="administrator", port=5678)
        with self.assertRaises(ResourceWarning):
            mrl.create().from_parameters(mrl.uri.FTP, "File.mp4", password="administrator", port=5678)
        with self.assertRaises(ResourceWarning):
            mrl.create().from_parameters(mrl.uri.FTP, "File.mp4", host="1.2.3.4", username="admin")
        with self.assertRaises(ResourceWarning):
            mrl.create().from_parameters(mrl.uri.FTP, "File.mp4", host="ftp.com", username="admin")

        with self.assertRaises(ValueError):
            mrl.create().from_parameters(
                mrl.uri.FTP,
                "File.mp4",
                host="ftp.com",
                port=5678,
                username="admin",
                password="administrator"
            ).using_ip()

        with self.assertRaises(ValueError):
            mrl.create().from_url("ftp://admin:administrator@ftp.com:5678/File.mp4").using_ip()


if __name__ == '__main__':
    unittest.main()
