from bs4 import BeautifulSoup
from .base_parser import BaseParser



class QidianParser(BaseParser):
    def extract_chapter_list(self, html):
        soup = BeautifulSoup(html, "html.parser")
        chapters = []
        for a in soup.select("ul.cf li a"):
            title = a.text.strip()
            link = a["href"]
            chapters.append((title, link))
        return chapters

    def extract_chapter_content(self, html):
        soup = BeautifulSoup(html, "html.parser")
        content_div = soup.find("div", class_="read-content")
        paragraphs = content_div.find_all("p")
        return "\n".join(p.get_text(strip=True) for p in paragraphs)


if __name__ == "__main__":
    url = "https://www.qidian.com/book/1032795920"
    parser = QidianParser()
    parser.extract_chapter_list(url)