import os
import requests
from bs4 import BeautifulSoup
import asyncio


class Spider_20xs_note(object):
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
        response = requests.get(self.dir_url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            box_cons = soup.find_all(total_name_list["book_name_path"]["type"], class_=total_name_list["book_name_path"]["class_"])
            if box_cons[0]:
                url_names = box_cons[0].find(total_name_list["book_name_path"]["title"]).get_text()
                directory = f"note/{url_names}/"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                print(f"书名：{url_names}")


            soup = BeautifulSoup(response.text, 'html.parser')
            box_cons = soup.find_all(total_name_list["book_url_list"]["type"][1], class_=total_name_list["book_url_list"]["ul"])
            if box_cons[0]:
                url_names = box_cons[0].find_all('li')
                # print(url_names)
                for link in url_names:
                    href = link.find('a').get('href')
                    chapter_name = link.get_text()
                    url = f"https://m.chuanshuyuan.com{href}"
                    file_path = directory + chapter_name + ".txt"
                    print("---"*30,directory,chapter_name)
                    self.get_file_content(url,file_path)
                    print(href, chapter_name, "-----success")

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

total_url = "https://m.minixiaoshuow.com/detail/37168.html"
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# }
response = requests.get(total_url,proxies=proxies)
print(response.status_code)





# from requests_html import HTMLSession

# total_url = "https://m.minixiaoshuow.com/detail/37168.html"
# session = HTMLSession()
# response = session.get(total_url)
# print(response)
# response.html.render()  # 渲染 JS
# print(response.status_code)
# print(response.html.html)
