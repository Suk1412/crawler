from urllib.parse import urlparse
from parsers.site_cnblogs import CnblogsParser
from parsers.site_cnsec import CnsecParser

def get_parser(url: str):
    domain = urlparse(url).netloc
    if "cn-sec" in domain:
        return CnsecParser()
    if "cnblogs" in domain:
        return CnblogsParser()
    else:
        raise ValueError(f"不支持的网站: {domain}")

if __name__ == "__main__":
    url = "https://cn-sec.com/archives/5000944.html"
    domain = urlparse(url).netloc
    print(domain)