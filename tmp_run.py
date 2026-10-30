"""读取 tmp.txt 中的字典，依次抓取并归档根目录文件。"""

import ast
import subprocess
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    urls = ast.literal_eval((root / "tmp.txt").read_text(encoding="utf-8"))
    source = root / "output" / "短篇小说 - 成人小说 - 色情小说"
    for name, url in urls.items():
        destination = root / name
        destination.mkdir(exist_ok=True)
        # 继承终端输入输出，保留 main.py 的全部打印。
        subprocess.run(["python3", "main.py", url], cwd=root, check=True)
        print(f"开始归档：{source} -> {destination}", flush=True)
        subprocess.run(
            [
                "find", ".", "-maxdepth", "1", "-type", "f",
                "-exec", "mv", "-v", "-t", str(destination), "--", "{}", "+",
            ],
            cwd=source,
            check=True,
        )
        print(f"归档完成：{name}", flush=True)


if __name__ == "__main__":
    main()
