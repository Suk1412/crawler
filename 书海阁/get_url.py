import grp
import os
import time
import requests
from bs4 import BeautifulSoup
import asyncio

class Crawling_Process(object):
    def __init__(self, book_url,book_id):
        """
            dir_url: 文章目录URL
        """
        self.dir_url = book_url + book_id
        self.book_url = book_url
        self.book_id = book_id
        # self.request_headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        #     "Accept-Language": "en-US,en;q=0.5",
        #     "Connection": "keep-alive",
        #     "Upgrade-Insecure-Requests": "1"
        # }

        self.request_headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://m.minixiaoshuow.com/detail/37168/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.chapter_info = {"name": "None","url": "None"}
        self.chapter_dict = {}
        self.book_name = "测试"
        self.blacklist = "None"

    def get_chapter_url(self):
        ...
    
    def request_main_url(self):
        ...
        # 发送HTTP请求
        chapter_num = 1

        response = requests.get(self.dir_url, headers=self.request_headers)
        # 检查请求是否成功
        if response.status_code == 200:
            print(response.text)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.book_name = soup.find('strong').text
            pages_list = [option['value'] for option in soup.find_all('option')]

        for page_num in pages_list:
            dir_url = self.book_url + page_num
            response = requests.get(dir_url, headers=self.request_headers)
            # 检查请求是否成功
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                box_cons = soup.find_all("ul", class_="read")
                if box_cons[0]:
                    url_names = box_cons[0].find_all('li')
                    for num in range(len(url_names)):
                        link = url_names[num]
                        href = link.find('a').get('href')
                        chapter_name = link.get_text()
                        url = f"{self.book_url}{href}"
                        self.chapter_info["name"] = chapter_name
                        self.chapter_info["url"] = url
                        self.chapter_dict[chapter_num] = self.chapter_info
                        chapter_num += 1
                    # print(chapter_name,url)
                    print("章节名字和路径 记录成功")
                else:
                    print("请求章节目录失败")
            else:
                print("请求章节目录失败，状态码:", response.status_code)

    def create_file(self):
        directory = os.path.dirname(__file__) + "/../note/"
        self.book_path = directory + self.book_name + ".txt"
        with open(self.book_path, 'w') as file:
            ...
        os.chmod(self.book_path, 0o777)
        gid = grp.getgrnam("wx").gr_gid
        os.chown(self.book_path, -1, gid)
        print(f"书名：{self.book_name}")
        self.blacklist = self.book_name

    def get_file_content(self):
        try:
            # 发送HTTP请求
            num = 1
            chapter_name = self.chapter_dict[num]["name"]
            print(chapter_name)
            url = self.chapter_dict[num]["url"]
            response = requests.get(url, headers=self.request_headers)
            # 检查请求是否成功
            if response.status_code == 200:
                # 使用BeautifulSoup解析HTML内容
                soup = BeautifulSoup(response.text, 'html.parser')
                article_content = soup.find('div', class_='content')
                if article_content:
                    paragraphs = article_content.find_all('p')

                    for paragraph in paragraphs:
                        # print(paragraph.get_text())
                        ...
                    # print(self.book_path)
                    with open(self.book_path, 'a', encoding='utf-8') as file:
                        file.write(chapter_name + '\n')
                        for paragraph in paragraphs:
                            if self.blacklist in paragraph.get_text():
                                break
                            file.write(paragraph.get_text() + '\n')
                        file.write('\n\n')
                else:
                    print("未找到文章内容")
            else:
                print("请求文章内容失败，状态码:", response.status_code)
            return 
        except requests.RequestException as e:
            print(f"请求发生错误: {e}")


    def install_file(self, total_name_list={"book_name_path":{"type": "div","class_":"header","title":"h1"},
                                            "book_url_list":{"type": ["div","ul"],"class_":"main", "ul":"read"}}):
        """
            得到文件下载链接
        """
        # 发送HTTP请求
        response = requests.get(self.dir_url, headers=self.request_headers)
        # 检查请求是否成功
        if response.status_code == 200:
            print("请求主网成功")
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            box_cons = soup.find_all(total_name_list["book_name_path"]["type"], class_=total_name_list["book_name_path"]["class_"])
            if box_cons[0]:
                book_name = box_cons[0].find(total_name_list["book_name_path"]["title"]).get_text()
                directory = os.path.dirname(__file__) + "/note/"
                self.book_path = directory + book_name + ".txt"
                with open(self.book_path, 'w') as file:
                    ...
                os.chmod(self.book_path, 0o777)
                gid = grp.getgrnam("wx").gr_gid
                os.chown(self.book_path, -1, gid)
                print(f"书名：{book_name}")

                self.book_directory_path = directory + book_name + "_目录.txt"
                with open(self.book_directory_path, 'w') as file:
                    ...
                os.chmod(self.book_directory_path, 0o777)
                gid = grp.getgrnam("wx").gr_gid
                os.chown(self.book_directory_path, -1, gid)

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
                    self.get_file_content(url,chapter_name)
                    print(chapter_name,"    爬取成功")
            else:
                print("章节和章节路径")
        else:
            print("请求章节目录失败，状态码:", response.status_code)
    

# 设置目标网页URL
book_id = "382358"
book_url = "https://m.shuhaige.net/"

url = book_url + book_id
crawler = Crawling_Process(book_url,book_id)
url = "https://m.shuhaige.net//382358/133263295.html"
crawler.request_main_url()
crawler.create_file()
crawler.get_file_content()
