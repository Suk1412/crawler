from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=chrome_options)
url = "https://cn-sec.com/archives/5000944.html"
driver.get(url)
# 等待 JS 加载完成
driver.implicitly_wait(5)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# 获取正文示例
texts = [p.text for p in soup.find_all("p")]
print(texts)

driver.quit()