from urllib.parse import urlparse
from parsers.site_shuhaige import ShuhaigeParser
from parsers.site_qidian import QidianParser

def get_parser(url: str):
    domain = urlparse(url).netloc
    if "qidian" in domain:
        return QidianParser()
    elif "shuhaige" in domain:
        return ShuhaigeParser()
    else:
        raise ValueError(f"不支持的网站: {domain}")
