import argparse
import grp
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from typing import Optional
from parser_factory import get_parser
import logging


def clean_chapter_title(title):
    # 去除各种形式的章节编号
    return re.sub(r"^(第[\d一二三四五六七八九零〇十百千万亿]+章|[\d一二三四五六七八九零〇十百千万亿]+)[ \t\u3000]+", "", title).strip()

def create_dir(path: Optional[str]=None, chmod_mode: Optional[int]=None,gid: Optional[int]=None, uid: Optional[int]=None) -> None:
    import pwd, grp
    if chmod_mode is None:
        chmod_mode = 0o775
    if gid is None:
        gid = grp.getgrnam(os.getlogin()).gr_gid
    if uid is None:
        uid = pwd.getpwnam(os.getlogin()).pw_uid
    if not os.path.exists(path):
        os.makedirs(path)
        os.chmod(path, chmod_mode)
        os.chown(path, gid, uid)

def create_file(path: Optional[str]=None, chmod_mode: Optional[int]=None,gid: Optional[int]=None, uid: Optional[int]=None) -> None:
    import pwd, grp
    if chmod_mode is None:
        chmod_mode = 0o775
    if gid is None:
        gid = grp.getgrnam(os.getlogin()).gr_gid
    if uid is None:
        uid = pwd.getpwnam(os.getlogin()).pw_uid
    if not os.path.exists(path):
        open(path, 'a').close()
        os.chmod(path, chmod_mode)
        os.chown(path, gid, uid)

def write_to_file(path: str, content: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

class Crawling_Process(object):
    def __init__(self, note_url: Optional[str]=None) -> None:
        """ 
            @type note_url:   String
            @param note_url: 文章目录URL 

            @type book_id:   String
            @param book_id: 文章ID 
        """
        self.note_url = note_url
        self.parser = get_parser(note_url)
        self.storage_path = ""
        self.book_name = ""
        self.book_path = ""
        self.file_name = ""
        self.book_chapter_list = {}
        logging.info(f"创建书籍文件夹")
        self.creat_book_dir()


    def creat_book_dir(self):
        self.book_name = self.parser.extract_novel_info(self.note_url)
        self.storage_path = os.path.dirname(__file__) + f"/../note/"
        self.book_path = self.storage_path + self.book_name
        create_dir(self.storage_path)
        create_dir(self.book_path)
    

    def create_chapter_file(self, chapter_name: Optional[str]=None, chapter_id: Optional[int]=None) -> None:
        title_name = clean_chapter_title(chapter_name)
        chapter_name = f"第{chapter_id}章 {title_name}"
        chapter_path = self.book_path + f"/{chapter_name}"
        create_file(chapter_path)
        return chapter_path
    

    def get_chapter_list(self):
        self.book_chapter_list = self.parser.extract_chapter_list(self.note_url)
        return self.book_chapter_list
    

    def get_chapter_content(self, chapter_url: Optional[str]=None):
        book_chapter_content = self.parser.extract_chapter_content(chapter_url)
        return book_chapter_content
    

    def download_file(self,start_chapter: Optional[int]=0, end_chapter: Optional[int]=10000) -> None:
        logging.info(f"开始获取 {self.book_name} 章节列表")
        self.get_chapter_list() 
        logging.info(f"开始下载 {self.book_name} 共{len(self.book_chapter_list)}章")
        for i in self.book_chapter_list.keys():
            if i >= start_chapter and i <= end_chapter:
                chapter_name = re.split("求月票", self.book_chapter_list[i][0])[0].replace("/", "|")
                chapter_url = self.book_chapter_list[i][1]
                chapter_path = self.create_chapter_file(chapter_name=chapter_name, chapter_id=i)
                chapter_content = self.get_chapter_content(chapter_url)
                write_to_file(chapter_path, chapter_content)
                logging.info(f"{chapter_name} 下载完成")
            else:
                chapter_name = re.split("求月票", self.book_chapter_list[i][0])[0].replace("/", "|")
                logging.info(f"{chapter_name} 跳过下载")
        
    def get_booksid_list(self):
        return [("第一本书","10001"),("第二本书","10002"),("第三本书","10003")]
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    # parser.add_argument("-l", "--list", action="store_true", help="列出所有书籍")
    parser.add_argument("-i", "--id", type=int, default=0, help="指定书籍ID")
    parser.add_argument("-u", "--url", type=str, default=0, help="需要爬取的文章目录URL")
    parser.add_argument("-s", "--start", type=int, default=0, help="开始章节")
    parser.add_argument("-e", "--end", type=int, default=10000, help="结束章节")
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

    # if args.list:
    #     A = Crawling_Process(args.url)
    #     books_id_list = A.get_booksid_list()
    #     from rich.table import Table
    #     from rich import print, box
    #     table = Table(show_header=True, header_style="bright_green", box=box.DOUBLE_EDGE)
    #     table.add_column("name", justify="center")
    #     table.add_column("id", justify="center")
    #     for book in books_id_list:
    #         name = book[0]
    #         id = book[1]
    #         table.add_row(*(name, id), style='bright_blue')
    #     print(table)
    # else:
    ants = Crawling_Process(args.url)
    ants.download_file(args.start, args.end)
    








