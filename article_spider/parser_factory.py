from urllib.parse import urlparse
from article_spider.parsers.site_book18 import Book18Parser
from parsers.site_cnblogs import CnblogsParser
from parsers.site_cnsec import CnsecParser
from parsers.general import GeneralWebParser

def get_parser(url: str):
    domain = urlparse(url).netloc
    if "cn-sec" in domain:
        return CnsecParser()
    if "cnblogs" in domain:
        return CnblogsParser()
    if "book18" in domain:
        return Book18Parser()
    else:
        raise ValueError(f"不支持的网站: {domain}")

# def get_parser(url: str):
#     return GeneralWebParser()

if __name__ == "__main__":
    url = "https://cn-sec.com/archives/5040402.html"
    url = "https://www.cnblogs.com/HarmonyOSSDK/p/19642889"
    # url = "https://www.book18.me/article/9284"
    domain = urlparse(url).netloc
    print(domain)