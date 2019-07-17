"""
Nexus API
"""

import requests
import logging
import re
import csv
from datetime import datetime

FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nexus')
handler = logging.FileHandler("repo-().log".format(datetime.now().strftime("%Y-%m-%d")))
fmt = logging.Formatter(FORMAT)
handler.setFormatter(fmt)
logger.addHandler(handler)

hys_repos = {'release': 'releases', 'snapshot': 'snapshots'}
hys_headers = {'Accept': 'application/json', 'Content-Type': 'multipart/form-data'}
BASE_URL = "http://nexus.example.com"
headers = {'Accept': 'application/json'}
auth_info = ('admin', 'admin123')


def get_assets_from_repo(params):
	api = '/service/rest/v1/assets'
	url = BASE_URL + api

	pattern1 = re.compile('.+\.(jar|pom|aar)$')
	pattern2 = re.compile('.+(-sources.jar)$')

	with requests.get(url, headers=headers, auth=auth_info, params=params) as response:
		if response.status_code == 200:
			rest = response.json().get('items')
			for item in rest:
				down_url = item.get('downloadUrl')
				if pattern1.findall(down_url) and not pattern2.findall(down_url):
					logger.info("#URL: {}".format(down_url))
					groupId = '.'.join(item.get('path').split('/')[:-3])
					version = item.get('path').split('/')[-2]
					artifactId = item.get('path').split('/')[-3]
					print(groupId, version, artifactId)
					with open('{}.csv'.format(params.get('repository')), mode='a+', encoding='UTF-8', newline='') as data_csv:
						csv_writer = csv.writer(data_csv)
						csv_writer.writerow((groupId, artifactId, version))
			return response.json().get('continuationToken')
		else:
			return False


repo = 'snapshots'
params = {'repository': repo}
n = 1
rt = get_assets_from_repo(params)
if rt:
	while True:
		if rt is None:
			break
		else:
			params['continuationToken'] = rt
			print('##第 {} 次 ####'.format(str(n)))
			n += 1
			print(params)
			rt = get_assets_from_repo(params)

