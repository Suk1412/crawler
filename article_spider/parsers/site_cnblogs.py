from bs4 import BeautifulSoup
import requests
from base.get import BaseParser

class CnblogsParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.title_xpath = "h1.postTitle"
        self.content_xpath = "div.postBody"

    def extract_file_info(self, html):
        response = requests.get(html, headers=self.request_headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            file_name = soup.select_one(self.title_xpath).text.strip()
        return file_name

    def extract_chapter_content(self, html):
        response = requests.get(html, headers=self.request_headers)
        paragraphs = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.select_one(self.title_xpath).get_text(strip=True)
            paragraphs.append(title)
            paragraph = soup.select_one(self.content_xpath)
            lines = paragraph.get_text(separator='\n', strip=True).split('\n')
            lines.insert(0, title)
        return '\n'.join(lines)

if __name__ == "__main__":
    url = "https://www.baishuzhai.cc/ibook/83243/83243894/36065058.html"
    url = "https://cn-sec.com/archives/5000944.html"
    C = CnblogsParser()
    print(C.extract_novel_info(url))