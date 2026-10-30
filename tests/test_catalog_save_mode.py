import tempfile
import unittest
from pathlib import Path

from core.processmanager import ProcessManager
from core.storage import Storage


class FakeParser:
    def __init__(self, save_mode=None):
        catalog = {} if save_mode is None else {"save_mode": save_mode}
        self.config = {"catalog": catalog}

    def get_book_name(self, _):
        return "测试书"

    def get_chapter_list(self, _):
        return {
            1: ["第一章", "https://example.test/1"],
            2: ["第二章", "https://example.test/2"],
        }

    def get_chapter_content(self, url):
        chapter = "第一章" if url.endswith("/1") else "第二章"
        return chapter, f"{chapter}\n{chapter}正文"


class CatalogSaveModeTest(unittest.TestCase):
    def make_manager(self, output_dir, save_mode=None):
        manager = ProcessManager.__new__(ProcessManager)
        manager.entry_url = "https://example.test/book"
        manager.parser = FakeParser(save_mode)
        manager.storage = Storage(output_dir=output_dir)
        return manager

    def test_default_mode_keeps_one_file_per_chapter(self):
        with tempfile.TemporaryDirectory() as output_dir:
            self.make_manager(output_dir).catalog("catalog")
            files = list((Path(output_dir) / "测试书").glob("*.txt"))
            self.assertEqual(len(files), 2)

    def test_single_file_mode_combines_chapters_in_order(self):
        with tempfile.TemporaryDirectory() as output_dir:
            self.make_manager(output_dir, "single_file").catalog("catalog")
            files = list((Path(output_dir) / "测试书").glob("*.txt"))
            self.assertEqual([file.name for file in files], ["测试书.txt"])
            self.assertEqual(
                files[0].read_text(encoding="utf-8"),
                "第一章\n第一章正文\n\n第二章\n第二章正文\n",
            )


if __name__ == "__main__":
    unittest.main()
