import argparse
import os
from typing import Optional
from urllib.parse import urlparse
from article_spider.parsers.general import GeneralWebParser
import logging
from tools.creat_tools import create_dir, create_file
from tools.write_tools import write_to_file
from site_configs import site_configs

"""
读取博客文章类但章节内容
"""

class Crawling_Process(object):
    def __init__(self, file_url: Optional[str]=None) -> None:
        """ 
            @type file_url:   String
            @param file_url: 文章目录URL 

            @type book_id:   String
            @param book_id: 文章ID 
        """
        self.file_url = file_url
        self.parser = GeneralWebParser(file_url)
        self.storage_path = ""
        self.web_name = ""
        self.web_path = ""
        self.file_name = ""
        self.book_chapter_list = {}
        logging.info(f"创建来源文件夹")
        self.creat_file_dir()


    def creat_file_dir(self):
        self.web_name = urlparse(self.file_url).netloc
        self.storage_path = os.path.dirname(__file__) + f"/../file/"
        self.web_path = self.storage_path + self.web_name
        create_dir(self.storage_path)
        create_dir(self.web_path)

    
    def create_file(self, file_name: Optional[str]=None) -> None:
        file_path = self.web_path + f"/{file_name}"
        print(file_path)
        create_file(file_path)
        return file_path
    

    def get_file_name(self) -> str:
        self.file_name = self.parser.extract_file_info(self.file_url)
        return self.file_name
    

    def get_chapter_content(self, chapter_url: Optional[str]=None):
        book_chapter_content = self.parser.extract_chapter_content(chapter_url)
        return book_chapter_content
    
    
    def download_file(self) -> None:
        logging.info(f"开始获取 {self.file_name} 文章内容")
        file_name = self.get_file_name()
        file_path = self.create_file(file_name=file_name)
        file_content = self.get_chapter_content(self.file_url)
        write_to_file(file_path, file_content)
        logging.info(f"{file_name} 下载完成")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str, default=0, help="需要爬取的文章目录URL")
    parser.add_argument("-d", "--debug", type=int, default=0, help="启用调试模式，1为开启")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG,  # 设置为DEBUG，控制输出交由 disable 决定
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    if args.debug != 1:
        logging.disable(logging.CRITICAL)

    if not args.url:
        url = input("请输入文章 url：")
    else:
        url = args.url
    
    domain = urlparse(url).netloc

    def save_site_configs(file_path="site_configs.py"):
        """把 site_configs 字典写回 Python 文件"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("site_configs = {\n")
            for domain, cfg in site_configs.items():
                f.write(f"    {repr(domain)}: {repr(cfg)},\n")
            f.write("}\n")
        print(f"site_configs 已保存到 {os.path.abspath(file_path)}")


    if domain not in site_configs:
        print(f"{domain} 不在 site_configs 中，需要手动输入选择器。")
        title = input("请输入标题选择器 (title selector): ")
        content = input("请输入正文选择器 (content selector): ")
        site_configs[domain] = {
            "title": title,
            "content": content
        }
        print(f"{domain} 已添加到 site_configs：{site_configs[domain]}")
        save_site_configs()  # 写回文件
    else:
        print(f"{domain} 已存在 site_configs。")

    try:
        ants = Crawling_Process(url)
        ants.download_file()
    except KeyboardInterrupt:
        print("爬取中断，程序退出")
    








