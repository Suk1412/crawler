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

