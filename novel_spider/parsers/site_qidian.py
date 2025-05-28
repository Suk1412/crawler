from bs4 import BeautifulSoup
# from .base_parser import BaseParser
import requests
import re
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

class BiqugeParser(BaseParser):
    def extract_novel_info(self, html):
        response = requests.get(html, headers=self.request_headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_name = soup.select("h1.bookName")[0].text.strip()
        else:
            print(response.status_code)
            print("qidian novel info error")
        return book_name


    def extract_chapter_list(self, html):
        urls = self.extract_chapter_page(html)
        chapter_num = 1
        chapters = {}
        for url in urls:
            response = requests.get(url, headers=self.request_headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for a in soup.select("div.book_last a"):
                    title = a.text.strip()
                    link = f"https://ca56c1c.fk6k.cc{a['href']}"
                    pattern = r"^/index/108632/\d+\.html$"
                    if re.match(pattern, a['href']):
                        chapters[chapter_num] = [title, link]
                        chapter_num += 1
                    else:
                        chapter_num += 1
        return chapters
            
    
    def extract_chapter_content(self, html):
        response = requests.get(html, headers=self.request_headers)
        content_div = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find('span', class_='title').text.strip()
            match = re.search(r'(第\d+章\s+[^\s_]+)', title)
            if match:
                title = match.group(1)
            else:
                pass
            content_div = soup.find("div", id="chaptercontent")
            raw_text = content_div.get_text(separator="\n", strip=True)
            clean_text = raw_text.split("请收藏：")[0].strip()
        return title + "\n" + clean_text


    def extract_chapter_page(self, html):
        response = requests.get(html, headers=self.request_headers)
        pages = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            options = soup.select('div.book_more a')
            pages = [opt['href'] for opt in options]
            full_urls = [f"https://ca56c1c.fk6k.cc{path}" for path in pages]
        return full_urls



if __name__ == "__main__":
    parser = BiqugeParser()
    # parser.extract_chapter_list(url)
    id = "37168"
    url = f"https://m.minixiaoshuow.com/detail/{id}/"
    chapters = parser.extract_novel_info(url)
    print(chapters)
