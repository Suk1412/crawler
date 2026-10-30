import argparse

from core.processmanager import ProcessManager
from core.logging_config import setup_logging


def main(argv=None):
    parser = argparse.ArgumentParser(description="根据站点配置抓取指定 URL 的内容")
    urls = parser.add_mutually_exclusive_group()
    urls.add_argument("url", nargs="?", help="要抓取的列表、目录或文章 URL")
    urls.add_argument("--url", dest="option_url", help="要抓取的 URL（与位置参数二选一）")
    args = parser.parse_args(argv)
    url = args.option_url or args.url or "https://www.book18.me/category/18"

    setup_logging()
    manager = ProcessManager(url)
    manager.run()


if __name__ == "__main__":
    main()
