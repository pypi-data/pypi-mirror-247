from unittest import TestCase


class Test(TestCase):
    def test_get_file_path(self):
        from utils.system import is_win, is_linux
        from utils.file import get_file_path
        if is_win():
            self.assertEqual(get_file_path("d:/Projects/test1/", "Proj\\remote\\test2\\", "1", "2"),
                             "d:\\Projects\\test1\\Proj\\remote\\test2\\1\\2")
            self.assertEqual(get_file_path("d:\\Projects/test1/", "Proj\\remote\\test2\\", "1", "2"),
                             "d:\\Projects\\test1\\Proj\\remote\\test2\\1\\2")
            self.assertEqual(get_file_path(1, "2", "3"), "1\\2\\3")
            self.assertEqual(
                get_file_path(
                    f"\\\\127.0.0.1\\Shared\\Remote\\2022Proj\\ServerTasks"),
                f"\\\\127.0.0.1\\Shared\\Remote\\2022Proj\\ServerTasks")
        elif is_linux():
            self.assertEqual(get_file_path("/d/Projects/test1/", "Proj\\remote\\test2\\", "1", "2"),
                             "/d/Projects/test1/Proj/remote/test2/1/2")
            self.assertEqual(get_file_path(1, "2", "3"), "1/2/3")

    def test_path_part(self):
        from utils.file import get_path_parent, get_path_back_second_part, get_path_last_part
        from utils.system import is_win
        if is_win():
            self.assertEqual(get_path_parent("d:/Projects/test1"), "d:\\Projects")
            self.assertEqual(get_path_parent("d:/Projects/test1.txt"), "d:\\Projects")
            self.assertEqual(get_path_back_second_part("d:/Projects/test1"), "Projects")
            self.assertEqual(get_path_back_second_part("d:/Projects/test1.txt"), "Projects")
            self.assertEqual(get_path_last_part("d:/Projects/test1"), "test1")
            self.assertEqual(get_path_last_part("d:/Projects/test1.txt"), "test1.txt")

            self.assertEqual(get_path_parent("d:\\Projects\\test1"), "d:\\Projects")
            self.assertEqual(get_path_parent("d:\\Projects\\test1.txt"), "d:\\Projects")
            self.assertEqual(get_path_back_second_part("d:\\Projects\\test1"), "Projects")
            self.assertEqual(get_path_back_second_part("d:\\Projects\\test1.txt"), "Projects")
            self.assertEqual(get_path_last_part("d:\\Projects\\test1"), "test1")
            self.assertEqual(get_path_last_part("d:\\Projects\\test1.txt"), "test1.txt")
        else:
            self.assertEqual(get_path_parent("/d/Projects/test1"), "/d/Projects")
            self.assertEqual(get_path_parent("/d/Projects/test1.txt"), "/d/Projects")
            self.assertEqual(get_path_back_second_part("/d/Projects/test1"), "Projects")
            self.assertEqual(get_path_back_second_part("/d/Projects/test1.txt"), "Projects")
            self.assertEqual(get_path_last_part("/d/Projects/test1"), "test1")
            self.assertEqual(get_path_last_part("/d/Projects/test1.txt"), "test1.txt")

    def test_norm_path(self):
        from utils.file import norm_case_insensitive_path, norm_spe
        from utils.system import is_win
        if is_win():
            self.assertEqual(norm_case_insensitive_path("d:/Projects/test1"), "d:\\projects\\test1")
            self.assertEqual(norm_spe("d:\\Projects/test1"), "d:/Projects/test1")

            self.assertEqual(norm_case_insensitive_path("d:\\Projects\\test1"), "d:\\projects\\test1")
        else:
            self.assertEqual(norm_case_insensitive_path("/d/Projects/test1"), "/d/projects/test1")
            self.assertEqual(norm_spe("/d\\Projects/test1"), "/d\Projects/test1")

    def test_path_to_url(self):
        from utils.file import path_to_url
        from utils.system import is_win
        if is_win():
            self.assertEqual(path_to_url("d:/requirements.txt"), "file:///d:/requirements.txt")
            self.assertEqual(path_to_url("d:\\requirements.txt"), "file:///d:/requirements.txt")
        else:
            self.assertEqual(path_to_url("/d/requirements.txt"), "file:///d/requirements.txt")

    def test_make_dirs_rm_dirs(self):
        from utils.file import copy_dir
        from utils.file import rm_dirs
        from utils.file import make_dirs
        from utils.file import get_file_path
        path = "./tmp_test/test_make_dirs_rm_dirs"
        err = make_dirs(path)
        self.assertTrue(err.ok)
        err = make_dirs(path)
        self.assertTrue(err.ok)

        with open(get_file_path(path, "test.txt"), "w") as f:
            f.write("test")
        count = copy_dir("./tmp_test", "./tmp_test2")
        self.assertEqual(count, 1)

        err = rm_dirs("./tmp_test")
        self.assertTrue(err.ok)
        err = rm_dirs("./tmp_test2")
        self.assertTrue(err.ok)
        err = rm_dirs("./tmp_test2")
        self.assertTrue(err.ok)
