"""
由于snapshots库太大，list接口超时会返回500，只能根据release-gav.txt信息获取
"""

import re
import requests
import csv
import argparse
from pathlib import Path
from datetime import datetime
import logging


FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nexus')
handler = logging.FileHandler("dl-().log".format(datetime.now().strftime("%Y-%m-%d")))
fmt = logging.Formatter(FORMAT)
handler.setFormatter(fmt)
logger.addHandler(handler)

headers = {'Accept': 'application/json'}
auth_info = ('admin', 'admin123')
BASE_URL = "http://nexus.example.com"


def get_ss_url_from_release_gav(asset_group, asset_name, asset_version, repo='snapshots'):
	api = "/service/rest/v1/search/assets"
	url = BASE_URL + api
	pattern1 = re.compile('.+\.(jar|pom|aar)$')
	pattern2 = re.compile('.+(-sources.jar)$')
	params = ['repository', 'format', 'maven.groupId', 'maven.artifactId', 'maven.baseVersion']
	values = [repo, 'maven2', asset_group, asset_name, asset_version + '-SNAPSHOT']
	data = dict(zip(params, values))
	asset_info = '/'.join(values)

	try:
		with requests.get(url, headers=headers, params=data) as response:
			print(response.status_code)
			result = response.json()
			if result['items']:
				first_urls = [item.get('downloadUrl') for item in result.get('items')]
				for url in first_urls:
					if pattern1.findall(url) and not pattern2.findall(url):
						logger.info(url)
			else:
				logger.error("### Not find maven asset: {}!".format(asset_info))
	except requests.exceptions.HTTPError as e:
		logger.error(e)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='get_asset_gav', description='get asset gav info from snapshots')
	parser.add_argument('-f', '--file', metavar='release_gav_file', dest='gav_file', required=True)
	args = parser.parse_args()

	if not Path(args.gav_file).exists():
		raise FileNotFoundError
	with open(args.gav_file, encoding='UTF-8') as f:
		for line in f:
			if line.strip():
				group, name, version, _ = line.strip().split(',')
				get_ss_url_from_release_gav(group, name, version)
