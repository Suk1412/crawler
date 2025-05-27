from urllib.parse import urlparse
from parsers.site_shuhaige import ShuhaigeParser
from parsers.site_biquge import BiqugeParser

def get_parser(url: str):
    domain = urlparse(url).netloc
    if "shuhaige" in domain:
        return ShuhaigeParser()
    if "ca56c1c.fk6k.cc" in domain:
        return BiqugeParser()
    else:
        raise ValueError(f"不支持的网站: {domain}")
