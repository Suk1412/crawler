from pathlib import Path
from urllib.parse import urlparse
import logging
import yaml
import re

CONFIG_DIR = Path(__file__).resolve().parents[1] / "site_configs"
logger = logging.getLogger(__name__)

# def load_config_for_url(url: str) -> dict:
#     domain = urlparse(url).netloc.lower()
#     print(f"Domain: {domain}")
#     for config_path in CONFIG_DIR.glob("*.yaml"):
#         with config_path.open(encoding="utf-8") as file:
#             config = yaml.safe_load(file)

#         domains = config.get("domains", [])
#         if domain in domains:
#             return config

#     raise ValueError(f"没有找到 {domain} 的站点配置")



def load_config_for_url(url: str) -> dict:
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    path = parsed_url.path

    logger.debug("开始匹配配置：domain=%s, path=%s", domain, path)
    matches = []

    for config_path in CONFIG_DIR.glob("*.yaml"):
        with config_path.open(encoding="utf-8") as file:
            config = yaml.safe_load(file)

        # 第一层：域名必须匹配
        if domain not in config.get("domains", []):
            continue

        # 第二层：路径规则必须匹配
        path_regex = config.get("match", {}).get("path_regex", ".*")
        if not re.match(path_regex, path):
            continue

        priority = config.get("match", {}).get("priority", 0)
        matches.append((priority, config, config_path))

    if not matches:
        raise ValueError(f"没有找到匹配配置：{url}")

    matches.sort(key=lambda item: item[0], reverse=True)
    priority, config, config_path = matches[0]
    logger.info(
        "已加载配置：%s（类型=%s，优先级=%s）",
        config_path.name,
        config.get("entry_type"),
        priority,
    )
    return config



if __name__ == "__main__":
    test_url = 'https://m.shuhaige.net/382360/'
    # test_url = "https://www.cnblogs.com/HarmonyOSSDK/p/21237380"
    # test_url = "https://cn-sec.com/archives/5000944.html"
    # test_url = "https://cn-sec.com/archives/category/安全文章"
    # test_url = 'https://bbs.kanxue.com/thread-292523.htm'
    config = load_config_for_url(test_url)
    import yaml
    print("已加载配置：\n"
      + yaml.safe_dump(
        config,
        allow_unicode=True,
        sort_keys=False,
    ))
