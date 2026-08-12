from pathlib import Path
from urllib.parse import urlparse
import yaml

CONFIG_DIR = Path(__file__).resolve().parents[1] / "site_configs"

def load_config_for_url(url: str) -> dict:
    domain = urlparse(url).netloc.lower()

    for config_path in CONFIG_DIR.glob("*.yaml"):
        with config_path.open(encoding="utf-8") as file:
            config = yaml.safe_load(file)

        domains = config.get("domains", [])
        if domain in domains:
            return config

    raise ValueError(f"没有找到 {domain} 的站点配置")


if __name__ == "__main__":
    test_url = 'https://m.shuhaige.net/382358/'
    config = load_config_for_url(test_url)
    print(config)