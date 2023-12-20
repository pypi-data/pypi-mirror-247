from unittest import TestCase
from utils.storage import FileStorage, SubDir


class Test(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_FileStorage_1(self):
        storage = FileStorage(
            "test", "/media/dir_a",
            # version_subdir=[],
            auto_make=False
        )
        storage.init()

        def t(filename):
            self.assertEqual(storage.final_paths(filename), ["/media/dir_a/test"])
            self.assertEqual(storage.the_final_path(filename), "/media/dir_a/test")
            self.assertEqual(storage.download_path(filename), f"/media/dir_a/downloading_test")

        t("file_a")
        t("file_b")
        t("file_c")

        part, full = storage.get_change_dir()
        self.assertSetEqual(part, set())
        self.assertSetEqual(full, set())

    def test_FileStorage_2(self):
        storage = FileStorage(
            "test", "/media/dir_a",
            version_subdir_s=[
                [SubDir("/media/dir_a")],
                [SubDir("/media/dir_a", 10), SubDir("/media/dir_b", 20)]
            ],
            auto_make=False
        )
        storage.init()
        # print(storage.all_dirs)

        filename = "file_a"
        self.assertEqual(storage.final_paths(filename), ['/media/dir_b/test/sub_5', '/media/dir_a/test'])
        self.assertEqual(storage.the_final_path(filename), "/media/dir_b/test/sub_5")
        self.assertEqual(storage.download_path(filename), f"/media/dir_a/downloading_test")

        filename = "file_b"
        self.assertEqual(storage.final_paths(filename), ['/media/dir_b/test/sub_19', '/media/dir_a/test'])
        self.assertEqual(storage.the_final_path(filename), "/media/dir_b/test/sub_19")
        self.assertEqual(storage.download_path(filename), f"/media/dir_a/downloading_test")


        filename = "file_c"
        self.assertEqual(storage.final_paths(filename), ['/media/dir_a/test/sub_1', '/media/dir_a/test'])
        self.assertEqual(storage.the_final_path(filename), "/media/dir_a/test/sub_1")
        self.assertEqual(storage.download_path(filename), f"/media/dir_a/downloading_test")

        filename = "file_d"
        self.assertEqual(storage.final_paths(filename), ['/media/dir_a/test/sub_3', '/media/dir_a/test'])
        self.assertEqual(storage.the_final_path(filename), "/media/dir_a/test/sub_3")
        self.assertEqual(storage.download_path(filename), f"/media/dir_a/downloading_test")

        part, full = storage.get_change_dir()
        self.assertSetEqual(part, set())
        self.assertSetEqual(full, {"/media/dir_a/test"})

    def test_FileStorage_3(self):
        storage = FileStorage(
            "test", "/media/dir_a",
            version_subdir_s=[
                [SubDir("/media/dir_a", 3)],
                [SubDir("/media/dir_a", 5), SubDir("/media/dir_b", 5)],
            ],
            auto_make=False
        )
        storage.init()
        # print(storage.all_dirs)

        filename = "file_a"
        self.assertEqual(storage.final_paths(filename), ['/media/dir_b/test/sub_2', '/media/dir_a/test/sub_0'])
        self.assertEqual(storage.the_final_path(filename), "/media/dir_b/test/sub_2")
        self.assertEqual(storage.download_path(filename), f"/media/dir_a/downloading_test")

        filename = "file_b"
        self.assertEqual(storage.final_paths(filename), ['/media/dir_b/test/sub_1', '/media/dir_a/test/sub_2'])
        self.assertEqual(storage.the_final_path(filename), "/media/dir_b/test/sub_1")
        self.assertEqual(storage.download_path(filename), f"/media/dir_a/downloading_test")

        filename = "file_c"
        self.assertEqual(storage.final_paths(filename), ['/media/dir_a/test/sub_1'])
        self.assertEqual(storage.the_final_path(filename), "/media/dir_a/test/sub_1")
        self.assertEqual(storage.download_path(filename), f"/media/dir_a/downloading_test")

        filename = "file_d"
        self.assertEqual(storage.final_paths(filename), ['/media/dir_a/test/sub_3', '/media/dir_a/test/sub_1'])
        self.assertEqual(storage.the_final_path(filename), "/media/dir_a/test/sub_3")
        self.assertEqual(storage.download_path(filename), f"/media/dir_a/downloading_test")

        part, full = storage.get_change_dir()
        self.assertSetEqual(part, {"/media/dir_a/test/sub_0", "/media/dir_a/test/sub_1", "/media/dir_a/test/sub_2"})
        self.assertSetEqual(full, set())
