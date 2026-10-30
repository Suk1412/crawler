import unittest

from sites.parser import Parser


class FakeResponse:
    def __init__(self, text):
        self.text = text
        self.status_code = 200

    def raise_for_status(self):
        return None


class FakeSession:
    def __init__(self, pages):
        self.pages = pages
        self.urls = []

    def get(self, url, timeout):
        self.urls.append(url)
        return FakeResponse(self.pages[url])


def make_config(**content_options):
    content = {
        "title_selector": "h1",
        "paragraph_selector": ".body p",
    }
    content.update(content_options)
    return {
        "book": {"title_selector": "h1"},
        "catalog": {
            "title_selector": "h2",
            "page_selector": "option",
            "page_url_attr": "value",
            "chapter_selector": "a",
            "chapter_title": "text",
        },
        "content": content,
    }


class ContentPaginationTest(unittest.TestCase):
    def test_next_link_merges_only_content_pages(self):
        parser = Parser(make_config(
            page_mode="next_link",
            next_page_selector=".pager a",
            next_page_text="下一页",
            max_pages=10,
        ))
        parser.session = FakeSession({
            "https://example.test/chapter.html": """
                <h1>第一章</h1><div class='body'><p>上半页</p></div>
                <div class='pager'><a href='/next-chapter.html'>下一章</a><a href='/chapter_2.html'>下一页</a></div>
            """,
            "https://example.test/chapter_2.html": """
                <h1>第一章</h1><div class='body'><p>下半页</p></div>
                <div class='pager'><a href='/next-chapter.html'>下一章</a></div>
            """,
        })

        title, content = parser.get_chapter_content("https://example.test/chapter.html")

        self.assertEqual(title, "第一章")
        self.assertEqual(content, "第一章\n上半页\n下半页")
        self.assertEqual(
            parser.session.urls,
            ["https://example.test/chapter.html", "https://example.test/chapter_2.html"],
        )

    def test_no_pagination_config_keeps_single_page_behavior(self):
        parser = Parser(make_config())
        parser.session = FakeSession({
            "https://example.test/chapter.html": """
                <h1>第一章</h1><div class='body'><p>正文</p></div>
                <div class='pager'><a href='/chapter_2.html'>下一页</a></div>
            """,
        })

        _, content = parser.get_chapter_content("https://example.test/chapter.html")

        self.assertEqual(content, "第一章\n正文")
        self.assertEqual(parser.session.urls, ["https://example.test/chapter.html"])

    def test_multiple_text_removal_patterns_clean_extracted_paragraphs(self):
        parser = Parser(make_config(remove_text_patterns=[
            r"请收藏.*",
            r"手机用户请.*阅读",
        ]))
        parser.session = FakeSession({
            "https://example.test/chapter.html": """
                <h1>第一章</h1><div class='body'>
                    <p>正文第一段</p><p>请收藏本站获取更新</p>
                    <p>手机用户请使用浏览器阅读</p><p>正文第二段</p>
                </div>
            """,
        })

        _, content = parser.get_chapter_content("https://example.test/chapter.html")

        self.assertEqual(content, "第一章\n正文第一段\n正文第二段")


if __name__ == "__main__":
    unittest.main()
