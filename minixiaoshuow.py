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
    
    def install_file(self, total_name_list={"book_name_path":{"type": "div","class_":"header","title":"h1"},
                                            "book_url_list":{"type": ["div","ul"],"class_":"main", "ul":"read"}}):
        """
            得到文件下载链接
        """
        # 发送HTTP请求

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

        response = requests.get(self.dir_url, headers=headers)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            box_cons = soup.find_all(total_name_list["book_name_path"]["type"], class_=total_name_list["book_name_path"]["class_"])
            if box_cons[0]:
                url_names = box_cons[0].find(total_name_list["book_name_path"]["title"]).get_text()
                directory = os.path.dirname(__file__) + "/note/"
                note_book_name = directory + url_names
                with open(note_book_name + '.txt', 'w') as file:
                    ...
                print(f"书名：{url_names}")

            
            


            soup = BeautifulSoup(response.text, 'html.parser')
            box_cons = soup.find_all("ul", class_="list")
            print(box_cons)
            if box_cons[0]:
                url_names = box_cons[0].find_all('li')
                print(url_names)
                for link in url_names:
                    href = link.find('a').get('href')
                    chapter_name = link.get_text()
                    url = f"https://m.chuanshuyuan.com{href}"
                    file_path = directory + chapter_name + ".txt"
                    print("---"*30,directory,chapter_name)
                    self.get_file_content(url,file_path)
                    print(href, chapter_name, "-----success")



            # soup = BeautifulSoup(response.text, 'html.parser')
            # box_cons = soup.find_all(total_name_list["book_url_list"]["type"][1], class_=total_name_list["book_url_list"]["ul"])
            # if box_cons[0]:
            #     url_names = box_cons[0].find_all('li')
            #     # print(url_names)
            #     for link in url_names:
            #         href = link.find('a').get('href')
            #         chapter_name = link.get_text()
            #         url = f"https://m.chuanshuyuan.com{href}"
            #         file_path = directory + chapter_name + ".txt"
            #         print("---"*30,directory,chapter_name)
            #         self.get_file_content(url,file_path)
            #         print(href, chapter_name, "-----success")

            else:
                print("未找到文章内容")
        else:
            print("请求失败，状态码:", response.status_code)
    

    def get_file_content(self, url, file_path):
        # 发送HTTP请求
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string
            article_content = soup.find('div', class_='content')
            if article_content:
                paragraphs = article_content.find_all('p')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write("-" * 20 + title + "-" * 20 + '\n')
                    for paragraph in paragraphs:
                        file.write(paragraph.get_text() + '\n')
            else:
                print("未找到文章内容")
        else:
            print("请求失败，状态码:", response.status_code)

    # def get_all_chapters():



# 设置目标网页URL
url = "https://m.minixiaoshuow.com/detail/37168/"  # 替换为你想爬取的网页地址
crawler = Crawling_Process(url)
crawler.install_file()
