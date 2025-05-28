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

class MinixiaoshuoParser(BaseParser):
    def extract_novel_info(self, html):
        response = requests.get(html, headers=self.request_headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_name = soup.select("h1")[0].text.strip()
        else:
            print(response.status_code)
            print("qidian novel info error")
        return book_name


    def extract_chapter_list(self, html):
        chapter_num = 1
        chapters = {}
        url = html
        response = requests.get(url, headers=self.request_headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for a in soup.select("div.bd ul li a"):
                title = a.text.strip()
                link = f"{url}{a['href']}"
                pattern = r"^\d+\.html$"
                if re.match(pattern, a['href']):
                    chapters[chapter_num] = [title, link]
                    chapter_num += 1
                else:
                    chapter_num += 1
        else:
            print("qidian chapter list error:",response.status_code)
        return chapters
            
    
    def extract_chapter_content(self, html):
        response = requests.get(html, headers=self.request_headers)
        content_div = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find('h1', class_='headline').text.strip()
            match = re.search(r'(第\d+章\s+[^\s_]+)', title)
            if match:
                title = match.group(1)
            else:
                pass
            content_div = soup.find("div", id="txt")
            cleaned_paragraphs = []
            for p in content_div.find_all("p"):
                text = p.get_text(strip=True)
                if "请关注米妮小说网" not in text:
                    cleaned_paragraphs.append(text)
            clean_text = "\n".join(cleaned_paragraphs)
        return title + "\n" + clean_text


    def extract_chapter_page(self, html):
        response = requests.get(html, headers=self.request_headers)
        pages = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            options = soup.select('div.book_more a')
            pages = [opt['href'] for opt in options]
            full_urls = [f"https://m.minixiaoshuow.com/detail{path}" for path in pages]
        return full_urls



if __name__ == "__main__":
    parser = MinixiaoshuoParser()
    url = f"https://m.minixiaoshuow.com/detail/37168/"
    url = f"https://m.minixiaoshuow.com/detail/37168/76913.html"
    chapters = parser.extract_chapter_content(url)
    print(chapters)
