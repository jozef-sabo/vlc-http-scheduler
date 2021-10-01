import unittest
import app.modules.url_processor as url_processor


class Tests(unittest.TestCase):
    def test_validate_path(self):
        path = url_processor.parse_path("Folder1/Folder2/File.mp4")

        self.assertEqual(path.full, "Folder1/Folder2/File.mp4")
        self.assertEqual(path.path, "Folder1/Folder2")
        self.assertEqual(path.file_extension, ".mp4")
        self.assertEqual(path.file_name, "File")
        self.assertEqual(path.full_filename, "File.mp4")

        path = url_processor.parse_path("File.mp4")

        self.assertEqual(path.full, "File.mp4")
        self.assertEqual(path.path, "")
        self.assertEqual(path.file_extension, ".mp4")
        self.assertEqual(path.file_name, "File")
        self.assertEqual(path.full_filename, "File.mp4")

        path = url_processor.parse_path("Folder1/Folder2/File")

        self.assertEqual(path.full, "Folder1/Folder2/File")
        self.assertEqual(path.path, "Folder1/Folder2")
        self.assertEqual(path.file_extension, "")
        self.assertEqual(path.file_name, "File")
        self.assertEqual(path.full_filename, "File")

        path = url_processor.parse_path("Folder1/Folder2/.mp4")

        self.assertEqual(path.full, "Folder1/Folder2/.mp4")
        self.assertEqual(path.path, "Folder1/Folder2")
        self.assertEqual(path.file_extension, "")
        self.assertEqual(path.file_name, ".mp4")
        self.assertEqual(path.full_filename, ".mp4")

    def test_validate_path_leading_slash(self):
        path = url_processor.parse_path("/Folder1/Folder2/File.mp4")

        self.assertEqual(path.full, "/Folder1/Folder2/File.mp4")
        self.assertEqual(path.path, "/Folder1/Folder2")
        self.assertEqual(path.file_extension, ".mp4")
        self.assertEqual(path.file_name, "File")
        self.assertEqual(path.full_filename, "File.mp4")

        path = url_processor.parse_path("/File.mp4")

        self.assertEqual(path.full, "/File.mp4")
        self.assertEqual(path.path, "/")
        self.assertEqual(path.file_extension, ".mp4")
        self.assertEqual(path.file_name, "File")
        self.assertEqual(path.full_filename, "File.mp4")

        path = url_processor.parse_path("/Folder1/Folder2/File")

        self.assertEqual(path.full, "/Folder1/Folder2/File")
        self.assertEqual(path.path, "/Folder1/Folder2")
        self.assertEqual(path.file_extension, "")
        self.assertEqual(path.file_name, "File")
        self.assertEqual(path.full_filename, "File")

        path = url_processor.parse_path("/Folder1/Folder2/.mp4")

        self.assertEqual(path.full, "/Folder1/Folder2/.mp4")
        self.assertEqual(path.path, "/Folder1/Folder2")
        self.assertEqual(path.file_extension, "")
        self.assertEqual(path.file_name, ".mp4")
        self.assertEqual(path.full_filename, ".mp4")
