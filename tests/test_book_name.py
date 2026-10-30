import unittest
from unittest.mock import Mock

import requests

from sites.parser import Parser


class BookNameTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser.__new__(Parser)
        self.parser.book_title_selector = "title"
        self.parser.session = Mock()
        self.url = "https://example.test/category/18"

    def set_response(self, status, text):
        response = requests.Response()
        response.status_code = status
        response.url = self.url
        response.encoding = "utf-8"
        response._content = text.encode("utf-8")
        self.parser.session.get.return_value = response

    def test_success_returns_title(self):
        self.set_response(200, "<title> 分类标题 </title>")
        self.assertEqual(self.parser.get_book_name(self.url), "分类标题")

    def test_http_failure_reports_status_and_url(self):
        self.set_response(403, "<title>Forbidden</title>")
        with self.assertRaises(requests.HTTPError) as error:
            self.parser.get_book_name(self.url)
        self.assertIn("403", str(error.exception))
        self.assertIn(self.url, str(error.exception))

    def test_missing_or_empty_title_reports_selector_and_url(self):
        for html in ("<html></html>", "<title> </title>"):
            with self.subTest(html=html):
                self.set_response(200, html)
                with self.assertRaises(ValueError) as error:
                    self.parser.get_book_name(self.url)
                self.assertIn("title", str(error.exception))
                self.assertIn(self.url, str(error.exception))


if __name__ == "__main__":
    unittest.main()
