import os
import requests
from bs4 import BeautifulSoup
import asyncio


class Crawling_Process(object):
    def __init__(self, dir_url):
        """
            dir_url: 文章目录URL
        """
        self.dir_url = dir_url
        self.request_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
    
    def install_file(self, total_name_list={"book_name_path":{"type": "div","class_":"header","title":"h1"},
                                            "book_url_list":{"type": ["div","ul"],"class_":"main", "ul":"read"}}):
        """
            得到文件下载链接
        """
        # 发送HTTP请求

        

        response = requests.get(self.dir_url, headers=self.request_headers)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            box_cons = soup.find_all(total_name_list["book_name_path"]["type"], class_=total_name_list["book_name_path"]["class_"])
            if box_cons[0]:
                book_name = box_cons[0].find(total_name_list["book_name_path"]["title"]).get_text()
                directory = os.path.dirname(__file__) + "/note/"
                self.book_path = directory + book_name + ".txt"
                with open(self.book_path, 'w') as file:
                    ...
                print(f"书名：{book_name}")

            
            
            chapter_info = {"name": "None",
                            "url": "None"}
            chapter_url_dict = {}
            soup = BeautifulSoup(response.text, 'html.parser')
            box_cons = soup.find_all("ul", class_="list")
            if box_cons[0]:
                url_names = box_cons[0].find_all('li')
                for num in range(len(url_names)):
                    link = url_names[num]
                    href = link.find('a').get('href')
                    chapter_name = link.get_text()
                    url = f"{self.dir_url}{href}"
                    chapter_info["name"] = chapter_name
                    chapter_info["url"] = url
                    chapter_url_dict[num] = chapter_info
                    if num > 3:
                        break
                    print(chapter_name)
                    print(url)
                    self.get_file_content(url,chapter_name)

            else:
                print("未找到文章内容")
        else:
            print("请求失败，状态码:", response.status_code)
    
    def get_file_content(self, url, chapter_name):
        # 发送HTTP请求
        response = requests.get(url, headers=self.request_headers)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string
            article_content = soup.find('div', class_='content')
            if article_content:
                paragraphs = article_content.find_all('p')
                with open(self.book_path, 'a', encoding='utf-8') as file:
                    file.write(chapter_name + '\n')
                    for paragraph in paragraphs:
                        if "柯南里的捡尸人" in paragraph.get_text():
                            break
                        file.write(paragraph.get_text() + '\n')
                    file.write('\n\n')
            else:
                print("未找到文章内容")
        else:
            print("请求失败，状态码:", response.status_code)

    # def get_all_chapters():



# 设置目标网页URL
url = "https://m.minixiaoshuow.com/detail/37168/"  # 替换为你想爬取的网页地址
crawler = Crawling_Process(url)
crawler.install_file()


