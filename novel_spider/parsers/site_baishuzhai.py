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

class BaishuzhaiParser(BaseParser):
    def extract_novel_info(self, html):
        response = requests.get(html, headers=self.request_headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_name = soup.select("div.book h1")[0].text.strip()
        return book_name


    def extract_chapter_list(self, html):
        # urls = self.extract_chapter_page(html)
        chapter_num = 1
        start_state = 0 
        chapters = {}
        url = html
        response = requests.get(url, headers=self.request_headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.select("div.listmain dl dd a"):
                title = a.text.strip()
                link = f"https://www.baishuzhai.cc{a['href']}"

                numbers = re.findall(r'第(\d+)章', title)[0]
                if numbers == "1":
                    start_state = 1
                if start_state == 1:
                    chapters[chapter_num] = [title, link]
                    chapter_num += 1
                    start_state = 1
        return chapters
            
    
    def extract_chapter_content(self, html):
        response = requests.get(html, headers=self.request_headers)
        paragraphs = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find('h1').get_text(strip=True)
            paragraphs.append(title)
            paragraph = soup.select("div.showtxt")[0]
            lines = paragraph.get_text(separator='\n', strip=True).split('\n')
            lines.insert(0, title)
        return '\n'.join(lines)


    def extract_chapter_page(self, html):
        response = requests.get(html, headers=self.request_headers)
        pages = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            options = soup.select('select option')
            pages = [opt['value'] for opt in options]
            full_urls = [f"https://www.baishuzhai.cc{path}" for path in pages]
        return full_urls



if __name__ == "__main__":
    parser = BaishuzhaiParser()
    # url = 'https://www.baishuzhai.cc/ibook/83243/83243894/'
    url = 'https://www.baishuzhai.cc/ibook/83243/83243894/36065058.html'
    parser.extract_chapter_content(url)

