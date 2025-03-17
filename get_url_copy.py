import os
import requests
from bs4 import BeautifulSoup
import asyncio
from colorama import Fore



class Spider_20xs_note(object):
    def __init__(self, dir_url):
        """
            dir_url: 文章目录URL
        """
        self.dir_url = dir_url
        self.book_name = ""
        self.book_path = ""
        self.chapter_name = ""
        self.chapter_content = ""
    
    def install_file(self, total_name_list={"book_name_path":{"type": "div","class_":"detail","title":"h1"},
                                            # "book_name_path":{"type": "div","class_":"header","title":"h1"},
                                            "book_url_list":{"type": ["div","ul"],"class_":"main", "ul":"read"}}):
        """
            得到文件下载链接
        """
        # 发送HTTP请求
        response = requests.get(self.dir_url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            self.book_name = soup.find_all("div", class_="detail")[0].find_all("p", class_="name")[0].get_text()
            self.book_path = f"note/{self.book_name}.txt"
            all_file_url = soup.find_all("div", class_="main")[0].find_all("ul", class_="read")[0].find_all("li")
            first_url = all_file_url[0].find('a').get('href')
            chapter_number_start = first_url.split('/')[-1].split('.')[0]

            i = 1
            while i<=1770:
                self.chapter_file_url = f"{self.dir_url}/{str(chapter_number_start)}.html"
                response = requests.get(self.dir_url)
                if response.status_code == 200:
                    chapter_number_start = int(chapter_number_start) + 1
                self.get_file_content(self.chapter_file_url)
                i += 1



    def get_file_content(self, url):
        # 发送HTTP请求
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')


            self.chapter_name = soup.find('h1', class_='headline').get_text()
            self.chapter_content = ""
            self.chapter_content += self.chapter_name + '\n'
            article_content = soup.find('div', class_='content')
            if article_content:
                paragraphs = article_content.find_all('p')
                for paragraph in paragraphs:
                    value = paragraph.get_text()
                    value = self.exclusion("穿书院更新速度全网最快", value)
                    self.chapter_content += value + '\n'
                self.file_save()
            else:
                print(Fore.RED + "未找到文章内容", Fore.RESET)
        else:
            print(Fore.RED + f"{self.chapter_name}----下载失败", Fore.RESET)
        
    def file_save(self):
        with open(self.book_path, 'a+', encoding='utf-8') as file:
            file.write(self.chapter_content)
            print(Fore.GREEN + f"{self.chapter_name}----已下载", Fore.RESET)
    
    def exclusion(self,exclusion_value, value):
        if exclusion_value in value:
            return ""
        else:
            return value



total_url = "https://m.chuanshuyuan.com/50947"
xs_spider = Spider_20xs_note(dir_url=total_url)
xs_spider.install_file()


# 'https://m.chuanshuyuan.com/50947/2237641.html'