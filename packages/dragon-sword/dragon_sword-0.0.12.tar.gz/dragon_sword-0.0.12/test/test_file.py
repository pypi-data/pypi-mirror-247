from unittest import TestCase


class Test(TestCase):
    def setUp(self) -> None:
        self.sha2_file = "sha2.test.txt"
        self.sha2_str = "abcdefg".encode("utf-8")
        self.sha2_str_sum = "7d1a54127b222502f5b79b5fb0803061152a44f92b37e23c6527baf665d4da9a"
        with open(self.sha2_file, "wb") as f:
            f.write(self.sha2_str)

    def tearDown(self) -> None:
        import os
        os.remove(self.sha2_file)

    def test_sha2_io(self):
        from io import BytesIO
        f = BytesIO()
        ss = self.sha2_str
        f.write(ss)
        # print(f.getvalue())
        from utils.file import sha2_io
        s = sha2_io(f)
        self.assertTrue(s == self.sha2_str_sum)

    def test_sha2_file(self):
        from utils.file import sha2_file
        s = sha2_file(self.sha2_file)
        self.assertTrue(s == self.sha2_str_sum)

    def test_read_lock(self):
        from utils.file import Lock
        with Lock("./").read_lock():
            pass
        with Lock("./").write_lock():
            pass

    def test_extract_compressed(self):
        from utils.file import check_file_exist
        from utils.file import compress
        from utils.file import extract_compressed
        from utils.file import rm_dirs
        from utils.file import make_dirs
        from utils.file import get_file_path
        path = "./tmp_test3/test_extract_compressed"
        name = "test_extract_compressed.txt"
        make_dirs(path)
        filepath = get_file_path(path, name)
        with open(filepath, "w") as f:
            f.write("123abc")

        target, err = compress(path)
        self.assertTrue(check_file_exist(target))

        path2 = "./tmp_test3/test_extract_compressed/extract"
        make_dirs(path2)
        extract_compressed(target, path2)
        self.assertTrue(check_file_exist(get_file_path(path2, name)))

        rm_dirs("./tmp_test3")

    def test_buff_size(self):
        from utils.file import buff_size
        self.assertTrue(buff_size(), 65535)

    def test_is_compress_file(self):
        from utils.file import is_compress_file
        self.assertTrue(is_compress_file("./1.gz"))
        self.assertTrue(is_compress_file("./1.tar"))
        self.assertTrue(is_compress_file("./1.zip"))
        self.assertTrue(is_compress_file("./1.rar"))
        self.assertFalse(is_compress_file("./1.txt"))
        self.assertFalse(is_compress_file("./1"))
        self.assertFalse(is_compress_file("."))

    def test_check_zip_file(self):
        from utils.file import check_zip_file
