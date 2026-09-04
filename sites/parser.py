from bs4 import BeautifulSoup
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urljoin
from pathlib import Path
import re

logger = logging.getLogger(__name__)
output_dir = Path(__file__).resolve().parents[1] / "output" / "html"
output_dir.mkdir(parents=True, exist_ok=True)

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
        self.chapter_page_mode = catalog_config.get('page_mode')
        self.chapter_max_pages = catalog_config.get('max_pages')
        self.chapter_page_selector = self.config['catalog']['page_selector']
        self.chapter_page_url_attr = self.config['catalog']['page_url_attr']
        self.chapter_next_page_selector = catalog_config.get('next_page_selector')
        self.chapter_next_page_url_attr = catalog_config.get('next_page_url_attr')
        self.chapter_chapter_selector = self.config['catalog']['chapter_selector']
        self.chapter_chapter_title = self.config['catalog']['chapter_title']
        self.chapter_chapter_url_attr = catalog_config.get('chapter_url_attr')
        content_config = self.config['content']
        self.content_title_selector = content_config['title_selector']
        self.content_paragraph_selector = content_config['paragraph_selector']
        # 正文分页是可选功能。未配置的旧站点仍按单页正文处理。
        self.content_page_mode = content_config.get('page_mode')
        self.content_next_page_selector = content_config.get('next_page_selector')
        self.content_next_page_text = content_config.get('next_page_text')
        self.content_next_page_url_attr = content_config.get('next_page_url_attr', 'href')
        self.content_max_pages = content_config.get('max_pages', 100)
        self.content_remove_text_patterns = [
            re.compile(pattern)
            for pattern in content_config.get('remove_text_patterns', [])
        ]


    def get_book_name(self, html):
        """返回书名"""
        logger.debug("请求书籍/文章页：%s", html)
        response = self.session.get(html, timeout=(5, 15))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_name = soup.select(self.book_title_selector)[0].text.strip()
            logger.debug("书籍/文章名：%s", book_name)
        return book_name


    def get_chapter_list(self, html):
        """返回章节标题和链接列表"""
        urls = self.extract_chapter_page(html)
        logger.info("开始解析章节列表：目录页数量=%s", len(urls))
        chapter_num = 1
        chapters = {}
        for url in urls:
            logger.debug("请求目录页：%s", url)
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
        logger.info("章节列表解析完成：共发现 %s 个章节", len(chapters))
        return chapters
            
    
    def get_chapter_content(self, html):
        """解析单个正文页，并按配置合并其分页内容。"""
        current_url = html
        visited = set()
        title = None
        paragraph_texts = []

        while current_url and current_url not in visited and len(visited) < self.content_max_pages:
            visited.add(current_url)
            logger.debug("请求正文页：%s", current_url)
            response = self.session.get(current_url, timeout=(5, 15))
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            if title is None:
                title_node = soup.select_one(self.content_title_selector)
                if title_node is None:
                    raise ValueError(f"找不到正文标题：{self.content_title_selector}")
                title = title_node.get_text(strip=True)

            for paragraph in soup.select(self.content_paragraph_selector):
                text = self._clean_content_text(paragraph.get_text(strip=True))
                if text:
                    paragraph_texts.append(text)

            if self.content_page_mode != 'next_link':
                break
            current_url = self._get_next_content_page_url(soup, current_url)

        if len(visited) == self.content_max_pages and current_url:
            logger.warning("正文页达到最大限制 %s，已停止继续翻页", self.content_max_pages)
        logger.debug("正文解析完成：页数=%s", len(visited))
        return title, title + "\n" + "\n".join(paragraph_texts)

    def _get_next_content_page_url(self, soup, current_url):
        """从正文翻页区域取下一页；可用链接文本避免误跟随“下一章”。"""
        if not self.content_next_page_selector:
            raise ValueError("正文分页缺少 next_page_selector 配置")

        for node in soup.select(self.content_next_page_selector):
            if self.content_next_page_text and node.get_text(strip=True) != self.content_next_page_text:
                continue
            href = node.get(self.content_next_page_url_attr)
            if href:
                return urljoin(current_url, href)
        return None

    def _clean_content_text(self, text):
        """按 YAML 中的多个正则规则移除正文里的非文章文字。"""
        for pattern in self.content_remove_text_patterns:
            text = pattern.sub('', text)
        return text.strip()

    def download_single_article(self,name,html):
        """单篇文章下载器"""
        try:
            response = self.session.get(html, timeout=(5, 15))
            response.raise_for_status()
            file_path = output_dir / f"{name}.html"
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            logger.info("HTML页面已下载：%s", name)
        except KeyboardInterrupt:
            logger.warning("单篇文章下载被用户中断：%s", html)
            return
    
    def extract_chapter_page(self, html):
        """提取章节页数"""
        page_mode = self.chapter_page_mode
        if page_mode == "all_links":
            logger.debug("目录分页模式：所以页链接")
            response = self.session.get(html, timeout=(5, 15))
            pages = []
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                options = soup.select(self.chapter_page_selector)
                pages = [opt['value'] for opt in options]
                page_urls = [urljoin(html, path) for path in pages]
                logger.info("发现 %s 个目录分页链接", len(page_urls))
            return page_urls

        if page_mode == "next_link":
            logger.info("目录分页模式：链接翻页")
            page_urls = []
            visited = set()
            current_url = html
            max_pages = self.chapter_max_pages
            while current_url and current_url not in visited and len(page_urls) < max_pages:
                visited.add(current_url)
                page_urls.append(current_url)
                response = self.session.get(current_url, timeout=(5, 15))
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                next_node = soup.select_one(self.chapter_next_page_selector)
                if not next_node:
                    break
                attr = self.chapter_next_page_url_attr
                href = next_node.get(attr)
                current_url = urljoin(current_url, href) if href else None
            if len(page_urls) == max_pages:
                logger.warning("目录页达到最大限制 %s，已停止继续翻页", max_pages)
            logger.info("发现 %s 个目录分页链接", len(page_urls))
            return page_urls



if __name__ == "__main__":
    from sites.config_loader import load_config_for_url
    test_url = "https://cn-sec.com/archives/category/安全文章"
    test_url = "https://cn-sec.com/archives/category/%e5%ae%89%e5%85%a8%e6%96%87%e7%ab%a0/%e4%ba%ba%e5%b7%a5%e6%99%ba%e8%83%bd%e5%ae%89%e5%85%a8"
    # test_url = "https://cn-sec.com/archives/category/安全文章/page/2"
    # test_url = "https://cn-sec.com/archives/5000944.html"
    test_url = "https://bbs.kanxue.com/thread-292523.htm"
    config = load_config_for_url(test_url)
    parser = Parser(config)
    # response = parser.session.get(test_url, timeout=(5, 15))
    # response.raise_for_status()
    # with open("/home/wx/work/dev-project/crawler/output/html/page.html", "w", encoding="utf-8") as file:
    #     file.write(response.text)
    chapter_title, content = parser.get_chapter_content(test_url)
    from tools.text_utils import safe_filename
    save_title_name = safe_filename(chapter_title)
    print(f"章节标题: {save_title_name}")
    parser.download_single_article(save_title_name,test_url)
