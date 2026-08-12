
from sites.config_loader import load_config_for_url   
from sites.parser import Parser
from storage import Storage

class ProcessManager(object):
    def __init__(self, entry_url: str):
          self.entry_url = entry_url

          # 1. URL → YAML dict
          config = load_config_for_url(entry_url)

          # 2. YAML dict → 通用 Parser
          self.parser = Parser(config)

          # 3. 负责保存，不关心站点结构
          self.storage = Storage(output_dir="output")

    def run(self):
        entry_type = self.parser.config["entry_type"]
        book_name = self.parser.get_book_name(self.entry_url)
        if entry_type == "catalog":
            chapters = self.parser.get_chapter_list(self.entry_url)
        else:
            chapters = {
                1: [book_name, self.entry_url]
            }
        for chapter_no, (chapter_title, chapter_url) in chapters.items():
            content_page_urls = self.parser.extract_content_pages(chapter_url)

            content = "\n".join(
                self.parser.extract_chapter_content(page_url)
                for page_url in content_page_urls
            )
            self.storage.save(
                book_name=book_name,
                chapter_no=chapter_no,
                chapter_title=chapter_title,
                content=content,
                entry_type=entry_type,
            )





