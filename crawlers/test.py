import requests
from bs4 import BeautifulSoup
import re

test_url = "https://npm.taobao.org/mirrors/node-sass/2331/win32-ia32-11_binding.node"
test_uri = "mirrors/node-sass/2331/win32-ia32-11_binding.node"
uri1 = "mirrors/node-sass/"
url1 = "https://npm.taobao.org/mirrors/node-sass/"
ua = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"
headers = {'User-Agent': ua}
r = requests.get(test_url, headers=headers).text
soup = BeautifulSoup(r, features="html.parser")
print(soup.find_all(href=re.compile(test_uri)))
# for element in soup.find_all(href=re.compile(test_uri)):
# 	for i in element.descendants:
# 		print(i)
# # print(soup.find_all(href=re.compile('https:.+/$')))

# base_url = "https://npm.taobao.org/"
# print(test_url.split(base_url))
#
# from pathlib import Path
# filepath = '/ttt/ssss/ssddd'
# print(Path(filepath).parent, type(Path(filepath).parent))
