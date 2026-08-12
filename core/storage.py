import os
from typing import Optional
import re

def clean_chapter_title(title: str) -> str:
      """去掉章节编号，保留用于文件名的章节标题。"""
      return re.sub(
          r"^(第[\d一二三四五六七八九零〇十百千万亿]+章|"
          r"[\d一二三四五六七八九零〇十百千万亿]+)[ \t\u3000]+",
          "",
          title,
      ).strip()

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

class Storage():
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def save(self, book_name: str, chapter_no: int, chapter_title: str, content: str, entry_type: str):
        # 创建书籍目录
        book_dir = os.path.join(self.output_dir, book_name)
        os.makedirs(book_dir, exist_ok=True)

        title_name = clean_chapter_title(chapter_title)
        filename = f"第{chapter_no:03d}章 {title_name}.txt"
        file_path = os.path.join(book_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    

if __name__ == "__main__":
    storage = Storage(output_dir="output")
    storage.save(
        book_name="Example Book",
        chapter_no=1,
        chapter_title="Chapter 1",
        content="This is the content of Chapter 1.",
        entry_type="catalog"
    )