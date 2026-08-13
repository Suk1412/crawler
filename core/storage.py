import os
from typing import Optional
import re

def safe_filename(name: str, fallback: str = "untitled") -> str:
      """把文本转换成单个安全的文件名或目录名。"""
      name = str(name).strip()
      # Windows、Linux 中会造成问题的字符；/ 尤其会变成路径。
      name = re.sub(r'[<>:"/\\\\|?*\\x00-\\x1f]', "_", name)
      # 避免连续空格/替换符，并清除文件名末尾的空格与点。
      name = re.sub(r"\s+", " ", name).strip(" ._")
      # 防止名称过长。
      return (name or fallback)[:150]

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
        save_title_name = safe_filename(title_name)
        if entry_type == "single_article":
            filename = f"{save_title_name}.txt"
        else:
            filename = f"第{chapter_no:03d}章 {save_title_name}.txt"
        file_path = os.path.join(book_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    

if __name__ == "__main__":
    from urllib.parse import urlparse
    url = "https://www.cnblogs.com/HarmonyOSSDK/p/21237380"
    url = "https://cn-sec.com/archives/5000944.html"
    domains = urlparse(url).netloc
    print(f"Domain: {domains}")
    storage = Storage(output_dir="output")
    storage.save(
        book_name=domains,
        chapter_no=1,
        chapter_title="Chapter 1",
        content="This is the content of Chapter 1.",
        entry_type="single_article"
    )