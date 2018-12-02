"""
爬取如下站点所有文件：
https://npm.taobao.org/mirrors/node-sass/
https://npm.taobao.org/dist
https://npm.taobao.org/mirrors/phantomjs
https://npm.taobao.org/mirrors/electron
https://npm.taobao.org/mirrors/fsevents
"""
import re
import time
import requests
from bs4 import BeautifulSoup
import logging
import threading
from queue import Queue
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


FORMAT = "%(levelname)s %(asctime)s %(thread)s %(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)
log = logging.getLogger('crawler')
handler = logging.FileHandler('./crawler.log')
handler.setLevel(logging.INFO)
log.addHandler(handler)

BASE_URL = "https://npm.taobao.org/"
uri_list = ["mirrors/node-sass/2331/", ]
ua = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"
headers = {'User-Agent': ua}

urls = Queue()  # 存取待下载文件的url
outputs = Queue()

event = threading.Event()
store_dir = "./"


# 1. 获取url
def crawler_urls(uri: str):
	pattern = re.compile('.+/$')
	url = BASE_URL + uri
	if pattern.match(uri):
		try:
			result = requests.get(url, headers=headers).text
			soup = BeautifulSoup(result, features="html.parser")
			for element in soup.find_all(href=re.compile(uri)):
				for child in element.descendants:
					sub_uri = uri + child
					if pattern.match(child):
						crawler_urls(sub_uri)
					else:
						sub_url = url + child
						urls.put(sub_url)
		except Exception as e:
			log.error(e)
	else:
		urls.put(url)


# 2.下载文件
def download():
	while not event.is_set():
		try:
			url = urls.get(True, 1)
			with requests.get(url, headers=headers, stream=True) as response:
				uri_path = url.split(BASE_URL)[-1]
				full_path = Path(store_dir)/Path(uri_path)
				print(uri_path)
				if not full_path.parent.exists():
					full_path.parent.mkdir(parents=True)
				with open(str(full_path), 'wb') as fd:
					for chunk in response.iter_content(chunk_size=1024):
						fd.write(chunk)
		except Exception as e:
			log.error(e)
		else:
			log.info("ok: {}".format(url))


executor = ThreadPoolExecutor(max_workers=10)

for uri in uri_list:
	executor.submit(crawler_urls, uri)
for i in range(5):
	executor.submit(download)

while True:
	inp = input('>>>')
	if inp.strip() == 'q':
		event.set()
		print("Stop Crawler!")
		time.sleep(5)
		break
