url = 'https://www.lingdxsw.org/book/19621/19266738.html'

import os
from pathlib import Path
import requests
from bs4 import BeautifulSoup

hwsim_path = "/home/wx/work/小代码/爬虫/"

def crawl_website_with_structure(url, base_path=hwsim_path):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        print(soup)
        dir_elements = soup.find_all('div', class_='panel-body')


crawl_website_with_structure(url)