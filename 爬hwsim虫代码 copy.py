import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup

base_path = __file__.split("/")[:-1]
base_path.append("crawler")
crawler_path = "/".join(base_path,)


def URL_Completion(url):
    # 实现URL完整性处理的逻辑
    if not url.startswith("http"):
        url = "https://w1.fi" + url
    return url


def crawl_website_with_structure2(url):
    crawler_list = {}
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        target_class_list = ['ls-blob','ls-dir']
        for target_class in target_class_list:
            directory = soup.find_all('a', class_=target_class)
            for element in directory:
                href = URL_Completion(element['href'])
                text = element.text
                crawler_list[text] = href
            for key, value in crawler_list.items(): 
                if target_class == 'ls-blob':             
                    download_file(value, key)
                    print(key, value)
            
                elif target_class == 'ls-dir':
                    make_dirs(key)
                    base_path.append(key)
                    crawl_website_with_structure(URL_Completion(value))
                    print(key, value) 
                

def crawl_website_with_structure(url, base_path=crawler_path):
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        dir_elements = soup.find_all('a', class_='ls-dir')
        file_elements = soup.find_all('a', class_='ls-blob')

        for element in file_elements:
            file_name = element.text
            file_url = URL_Completion(element['href'])
            file_path = os.path.join(base_path, file_name)
            print(file_path)
            # download_file(file_url, file_path)

        for element in dir_elements: 
            dir_name = element.text
            dir_url = URL_Completion(element['href'])
            dir_path = os.path.join(base_path, dir_name)
            make_dirs(dir_path)
            # crawl_website_with_structure(dir_url,base_path=dir_path)



def make_dirs(dir_path):
    # 实现文件下载的逻辑
    try:
        os.makedirs(dir_path)
    except FileExistsError:
        pass

def download_file(url, file_path):
    # 实现文件下载的逻辑
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        directory = soup.find("div", class_="highlight")
        if directory:
            with open(file_path, 'w') as f:
                f.write(directory.text)
        else:
            print("未找到目录结构")

    


crawl_website_with_structure('https://www.69shuba.com/book/85967.htm')

