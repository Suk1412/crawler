from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urljoin


class Parser():
    def __init__(self, config: dict):
        self.config = config
        self.request_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
         # 创建一个可复用连接、Cookie 和默认请求头的会话
        self.session = requests.Session()
        self.session.headers.update(self.request_headers)

        # 请求失败时的自动重试策略
        retry = Retry(
            total=3,                         # 最多额外重试 3 次
            connect=3,                       # 连接失败最多重试 3 次
            read=3,                          # 读取超时最多重试 3 次
            backoff_factor=1,                # 第 1/2/3 次重试前等待约 1/2/4 秒
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET"}),
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)


        catalog_config = self.config.get("catalog", {})
        self.book_title_selector = self.config['book']['title_selector']
        self.chapter_title_selector = self.config['catalog']['title_selector']
        self.chapter_page_selector = self.config['catalog']['page_selector']
        self.chapter_page_url_attr = self.config['catalog']['page_url_attr']
        self.chapter_chapter_selector = self.config['catalog']['chapter_selector']
        self.chapter_chapter_title = self.config['catalog']['chapter_title']
        self.chapter_chapter_url_attr = catalog_config.get('chapter_url_attr')
        self.content_title_selector = self.config['content']['title_selector']
        self.content_paragraph_selector = self.config['content']['paragraph_selector']


    def get_book_name(self, html):
        """返回书名"""
        response = self.session.get(html, timeout=(5, 15))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_name = soup.select(self.book_title_selector)[0].text.strip()
        return book_name


    def get_chapter_list(self, html):
        """返回章节标题和链接列表"""
        urls = self.extract_chapter_page(html)
        chapter_num = 1
        chapters = {}
        for url in urls:
            response = self.session.get(url, timeout=(5, 15))
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for a in soup.select(self.chapter_chapter_selector):
                    title = a.text.strip()
                    href_attr = self.chapter_chapter_url_attr
                    href = a.get(href_attr)
                    if not href:
                        continue
                    chapter_url = urljoin(url, href)
                    chapters[chapter_num] = [title, chapter_url]
                    chapter_num += 1
        return chapters
            
    
    def get_chapter_content(self, html):
        """解析单个正文页"""
        response = self.session.get(html, timeout=(5, 15))
        paragraphs = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            title_node = soup.select_one(self.content_title_selector)
            if title_node is None:
                raise ValueError(f"找不到正文标题：{self.content_title_selector}")
            title = title_node.get_text(strip=True)
            paragraphs = soup.select(self.content_paragraph_selector)
        return title + "\n" + "\n".join(p.get_text(strip=True) for p in paragraphs)


    def extract_chapter_page(self, html):
        response = self.session.get(html, timeout=(5, 15))
        pages = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            options = soup.select(self.chapter_page_selector)
            pages = [opt['value'] for opt in options]
            full_urls = [urljoin(html, path) for path in pages]
        return full_urls

