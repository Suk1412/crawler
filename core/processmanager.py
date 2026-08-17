from sites.config_loader import load_config_for_url   
from sites.parser import Parser
from tools.text_utils import safe_filename
from core.storage import Storage
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

class ProcessManager(object):
    def __init__(self, entry_url: str):
        self.entry_url = entry_url
        config = load_config_for_url(entry_url)
        self.parser = Parser(config)
        self.storage = Storage(output_dir="output")

    def catalog(self,entry_type):
        """长篇小说下载器"""
        book_name = self.parser.get_book_name(self.entry_url)
        chapters = self.parser.get_chapter_list(self.entry_url)
        total_chapters = len(chapters)
        if not total_chapters:
            logger.warning("未找到可下载章节：%s", self.entry_url)
            return
        
        logger.info("开始下载《%s》，共 %s 章", book_name, total_chapters)
        saved_count = 0
        try:
            for completed, (chapter_no, (chapter_title, chapter_url)) in enumerate(
                chapters.items(), start=1
            ):
                _, content = self.parser.get_chapter_content(chapter_url)
                self.storage.save(
                    book_name=book_name,
                    chapter_no=chapter_no,
                    chapter_title=chapter_title,
                    content=content,
                    entry_type=entry_type,
                )
                logger.debug("已保存章节 %s/%s：%s", completed, total_chapters, chapter_title)
                saved_count = completed
                self._print_progress(completed, total_chapters, chapter_title)
            print()
        except KeyboardInterrupt:
            logger.warning("下载被用户中断：已完成 %s/%s 章", saved_count, total_chapters)
            return
        
        logger.info("《%s》下载完成", book_name)

    def single(self, entry_type):
        """单章小说下载器"""
        try:
            book_name = urlparse(self.entry_url).netloc
            chapter_title, content = self.parser.get_chapter_content(self.entry_url)
            save_title_name = safe_filename(chapter_title)
            self.parser.download_single_article(save_title_name,self.entry_url)
            self.storage.save(
                book_name=book_name,
                chapter_no=None,
                chapter_title=chapter_title,
                content=content,
                entry_type=entry_type,
            )
            logger.info("单篇文章已保存：%s", chapter_title)
        except KeyboardInterrupt:
            logger.warning("单篇文章下载被用户中断：%s", self.entry_url)
            return
        

    
    def article_list(self, entry_type):
        """多篇单章小说下载器"""
        book_name = self.parser.get_book_name(self.entry_url)
        chapters = self.parser.get_chapter_list(self.entry_url)
        total_chapters = len(chapters)
        if not total_chapters:
            logger.warning("未找到列表文章：%s", self.entry_url)
            return
        
        logger.info("开始下载文章列表《%s》，共 %s 篇", book_name, total_chapters)
        saved_count = 0
        try:
            for completed, (chapter_no, (chapter_title, chapter_url)) in enumerate(
                chapters.items(), start=1
            ):
                _, content = self.parser.get_chapter_content(chapter_url)
                self.storage.save(
                    book_name=book_name,
                    chapter_no=chapter_no,
                    chapter_title=chapter_title,
                    content=content,
                    entry_type=entry_type,
                )
                logger.debug("已保存文章 %s/%s：%s", completed, total_chapters, chapter_title)
                saved_count = completed
                self._print_progress(completed, total_chapters, chapter_title)
            print()
        except KeyboardInterrupt:
            logger.warning("文章列表下载被用户中断：已完成 %s/%s 篇", saved_count, total_chapters)
            return
    
        logger.info("文章列表《%s》下载完成", book_name)
        

    def run(self):
        entry_type = self.parser.config["entry_type"]
        logger.info("任务类型：%s", entry_type)
        if entry_type == "catalog":
            self.catalog(entry_type)
        if entry_type == "single_article":
            self.single(entry_type)
        if entry_type == "article_list":
            self.article_list(entry_type)
    

    @staticmethod
    def _print_progress(completed: int, total: int, chapter_title: str) -> None:
        """在同一行显示章节下载进度，不依赖第三方库。"""
        bar_width = 30
        filled = int(bar_width * completed / total)
        bar = "#" * filled + "-" * (bar_width - filled)
        percent = completed * 100 / total
        title = chapter_title.replace("\n", " ")[:30]
        print(
            f"\r\033[K[{bar}] {completed}/{total} {percent:6.2f}%  {title}",
            end="",
            flush=True,
        )
        
