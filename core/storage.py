import os
import logging
from tools.text_utils import safe_filename, clean_chapter_title

logger = logging.getLogger(__name__)

class Storage():
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def save(self, book_name: str, chapter_no: int, chapter_title: str, content: str, entry_type: str):
        # 创建书籍目录
        save_book_name = safe_filename(book_name)
        book_dir = os.path.join(self.output_dir, save_book_name)
        os.makedirs(book_dir, exist_ok=True)

        title_name = clean_chapter_title(chapter_title)
        save_title_name = safe_filename(title_name)
        if entry_type == "single_article":
            filename = f"{save_title_name}.txt"
        if entry_type == "article_list":
            filename = f"{save_title_name}.txt"
        else:
            filename = f"第{chapter_no:03d}章 {save_title_name}.txt"
        file_path = os.path.join(book_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.debug("文件已写入：%s", file_path)
    

if __name__ == "__main__":
    from urllib.parse import urlparse
    url = "https://www.cnblogs.com/HarmonyOSSDK/p/21237380"
    url = "https://cn-sec.com/archives/5000944.html"
    domains = urlparse(url).netloc
    print(f"Domain: {domains}")
    storage = Storage(output_dir="output")
    storage.save(
        book_name=domains,
        chapter_no=1,
        chapter_title="Chapter 1",
        content="This is the content of Chapter 1.",
        entry_type="single_article"
    )
