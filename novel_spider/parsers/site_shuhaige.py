from bs4 import BeautifulSoup
from .base_parser import BaseParser
import requests



class ShuhaigeParser(BaseParser):
    def extract_novel_info(self, html):
        response = requests.get(html, headers=self.request_headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_name = soup.select("p.name")[0].text.strip()
        return book_name


    def extract_chapter_list(self, html):
        urls = self.extract_chapter_page(html)
        chapter_num = 1
        chapters = {}
        for url in urls:
            response = requests.get(url, headers=self.request_headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for a in soup.select("ul.read li a"):
                    title = a.text.strip()
                    link = f"https://m.shuhaige.net{a['href']}"
                    chapters[chapter_num] = [title, link]
                    chapter_num += 1
        return chapters
            
    
    def extract_chapter_content(self, html):
        response = requests.get(html, headers=self.request_headers)
        paragraphs = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.find('h1', class_='headline').text
            paragraphs.append(title)
            paragraphs = soup.select("div.content p")
        return title + "\n" + "\n".join(p.get_text(strip=True) for p in paragraphs)


    def extract_chapter_page(self, html):
        response = requests.get(html, headers=self.request_headers)
        pages = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            options = soup.select('select option')
            pages = [opt['value'] for opt in options]
            full_urls = [f"https://m.shuhaige.net{path}" for path in pages]
        return full_urls



if __name__ == "__main__":
    parser = ShuhaigeParser()
    # parser.extract_chapter_list(url)
    url = 'https://m.shuhaige.net/382358/'
    parser.extract_novel_info(url)

