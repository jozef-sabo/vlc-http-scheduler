import unittest
import os
import shutil
import app.modules.worker.MediaHolder as MediaHolder
import app.modules.VLC_connector.tools.request_processing.mrl as mrl

folder = os.path.abspath(os.path.join(os.getcwd(), "test"))
file1 = os.path.abspath(os.path.join(os.getcwd(), "test/file1.txt"))
file2 = os.path.abspath(os.path.join(os.getcwd(), "test/file2.txt"))


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.mkdir(folder)
        with open(file1, "w+", encoding="UTF-8", newline="\r\n") as opened_file_1:
            for i in range(1000):
                opened_file_1.write("abcdef\n")

        with open(file2, "w+", encoding="UTF-8", newline="\r\n") as opened_file_2:
            for i in range(10000):
                opened_file_2.write("1000101")

    def setUp(self) -> None:
        self.media1 = MediaHolder.add(mrl.create().from_url(file1))
        self.media2 = MediaHolder.add(mrl.create().from_url(file2))

    def tearDown(self) -> None:
        MediaHolder.remove_media()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(folder)

    def test_default(self):
        self.assertEqual(self.media1, MediaHolder.get_media()[0])
        self.assertEqual(self.media2, MediaHolder.get_media()[1])

        self.assertEqual(self.media1.display_name, "file1")
        self.assertEqual(self.media2.display_name, "file2")

        MediaHolder.remove_media()
        self.assertFalse(MediaHolder.get_media())

        self.assertEqual(MediaHolder.default_media_holder, MediaHolder.MediaHolder())

    def test_create_SHA(self):
        self.assertEqual(self.media1.SHA_256, "dfcddcb1c8fc0faa98d463cc4aaaee24f85c750305087986eabeea2ce77cfdec")
        self.assertEqual(self.media2.SHA_256, "f5602f308299a4c739a871b0474095036e77133180999a9723c802448b7ce536")

    def test_get_rename_media(self):
        self.assertEqual(MediaHolder.get_media("file1"), self.media1)
        self.assertEqual(MediaHolder.get_media("file2"), self.media2)

        MediaHolder.rename_media(MediaHolder.get_media("file1"), "video1")

        self.assertEqual(self.media1, MediaHolder.get_media("video1"))
        self.assertEqual(self.media1.latest_display_name, "file1")
        self.assertEqual(self.media1.display_name, "video1")

        with self.assertRaises(ValueError):
            MediaHolder.rename_media(MediaHolder.get_media("video1"), "file2")

    def test_add_media(self):
        media3 = MediaHolder.add_using_name(mrl.create().from_url(mrl.uri.FILE + file2), "file3")
        self.assertEqual(MediaHolder.get_media(), [self.media1, self.media2, media3])

        with self.assertRaises(ValueError):
            MediaHolder.add(mrl.create().from_url(mrl.uri.FILE + file2))

        with self.assertRaises(ValueError):
            MediaHolder.add_using_name(mrl.create().from_url(mrl.uri.FILE + file2), "file3")

    def test_integrity(self):
        self.assertEqual(MediaHolder.check_integrity(), [])

    def test_media_type(self):
        media3 = MediaHolder.add_using_name(mrl.create().from_url(mrl.uri.FILE + file2), "file3")
        self.assertEqual(media3.type, MediaHolder.types.FEATURE)

        media3.media_of_type("Test")
        self.assertEqual(media3.type, MediaHolder.types.TEST)

        media3.media_of_type("TLR")
        self.assertEqual(media3.type, MediaHolder.types.TRAILER)

        media4 = MediaHolder.add_using_name(mrl.create().from_url(mrl.uri.FILE + file2), "file4").psa
        self.assertEqual(media4.type, MediaHolder.types.PSA)

        with self.assertRaises(ValueError):
            media3.media_of_type("Fairy-tale")
