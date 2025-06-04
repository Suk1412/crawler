from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self):
        super().__init__()
        self.request_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    @abstractmethod
    def extract_novel_info(self, html: str) -> str:
        """ 提取小说基本信息 """
        pass


    @abstractmethod
    def extract_chapter_list(self, html: str) -> list[tuple[str, str]]:
        """ 提取章节标题与链接列表 """
        pass


    @abstractmethod
    def extract_chapter_content(self, html: str) -> str:
        """ 提取章节正文 """
        pass