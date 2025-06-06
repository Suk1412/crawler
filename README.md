⚙️ 可用参数说明
================

| 参数                        | 说明                                 |
|-----------------------------|--------------------------------------|
| `-h`, `--help`              | 显示帮助信息并退出                    |
| `-l`, `--list`              | 列出所有书籍                          |
| `-i ID`, `--id ID`          | 指定书籍 ID                           |
| `-u URL`, `--url URL`       | 需要爬取的文章目录 URL                |
| `-s START`, `--start START` | 开始章节编号                          |
| `-e END`, `--end END`       | 结束章节编号                          |
| `-d DEBUG`, `--debug DEBUG` | 启用调试模式（设置为 1 开启）         |


🧪 使用示例
================
爬取书籍所有章节：
```
python main.py -u "https://example.com/index/12345/list.html"
```

爬取书籍指定的章节：
```
python main.py -u "https://example.com/index/12345/list.html" -s 1 -e 100
```

启用调试模式：
```
python main.py -u "https://example.com/index/12345/list.html" -d 1
```
