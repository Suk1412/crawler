import grp
import os
import time
import requests
from bs4 import BeautifulSoup
from typing import Optional
from parser_factory import get_parser

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
    def __init__(self, note_url: Optional[str]=None ,book_id: Optional[str]=None) -> None:
        """ 
            @type note_url:   String
            @param note_url: 文章目录URL 

            @type book_id:   String
            @param book_id: 文章ID 
        """
        self.note_url = note_url
        self.book_id = book_id
        self.parser = get_parser(note_url)
        self.dir_url = note_url + book_id
        self.note_url = note_url
        self.book_id = book_id
        self.storage_path = ""
        self.book_path = ""
        self.file_name = ""
        self.book_chapter_list = {}
        self.creat_book_dir()
        self.get_chapter_list()


    def creat_book_dir(self):
        book_name = self.parser.extract_novel_info(self.dir_url)
        self.storage_path = os.path.dirname(__file__) + f"/../note/"
        self.book_path = self.storage_path + book_name
        create_dir(self.storage_path)
        create_dir(self.book_path)
    

    def create_chapter_file(self, chapter_name: Optional[str]=None, chapter_id: Optional[int]=None) -> None:
        import re
        pattern = r"^第\d+章\s+.+"
        match = re.match(pattern, chapter_name)
        if match:
            chapter_path = self.book_path + f"/{chapter_name}"
            create_file(chapter_path)
        else:
            chapter_name = f"第{chapter_id}章 {chapter_name}"
            chapter_path = self.book_path + f"/{chapter_name}"
            create_file(chapter_path)
        return chapter_path
    

    def get_chapter_list(self):
        self.book_chapter_list = self.parser.extract_chapter_list(self.dir_url)
        return self.book_chapter_list
    

    def get_chapter_content(self, chapter_url: Optional[str]=None):
        book_chapter_content = self.parser.extract_chapter_content(chapter_url)
        return book_chapter_content
    

    def download_file(self,start_chapter: Optional[int]=0, end_chapter: Optional[int]=10000) -> None:
        for i in self.book_chapter_list.keys():
            if i >= start_chapter and i <= end_chapter:
                chapter_name = self.book_chapter_list[i][0]
                chapter_url = self.book_chapter_list[i][1]
                chapter_path = self.create_chapter_file(chapter_name=chapter_name)
                chapter_content = self.get_chapter_content(chapter_url)
                write_to_file(chapter_path, chapter_content)
                print(f"第{i}章 {chapter_name} 下载完成")
            else:
                print(f"第{i}章 跳过下载")

if __name__ == '__main__':
    # 设置目标网页URL
    # book_id = "382358"
    # note_url = "https://m.shuhaige.net/"
    # A = Crawling_Process(note_url, book_id)
    # A.download_file()


    book_id = "108632"
    note_url = "https://ca56c1c.fk6k.cc/index/"
    A = Crawling_Process(note_url, book_id)
    A.download_file(start_chapter=250, end_chapter=255)











