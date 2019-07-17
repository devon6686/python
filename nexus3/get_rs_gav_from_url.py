"""
从components的下载url中获取component的GAV信息，输出到csv文件中
"""

import re
import csv
import argparse
from pathlib import Path
from datetime import datetime


def get_gav_from_url(filename, split_word='http://nexus.example.com/repository/releases/'):
	pattern1 = re.compile('.+\.(jar|pom|aar)$')
	pattern2 = re.compile('.+(-sources.jar)$')

	with open(filename, encoding='UTF-8') as url_file:
		for url in url_file:
			if url.strip():
				if pattern1.findall(url) and not pattern2.findall(url):
					gav_path = url.split(split_word)[-1]
					groupId = '.'.join(gav_path.split('/')[:-3])
					version = gav_path.split('/')[-2]
					artifactId = gav_path.split('/')[-3]
					asset_filename = artifactId + version
					print(groupId, artifactId, version, asset_filename)
					with open('releases-gav-{}.csv'.format(datetime.now().strftime('%Y-%m-%d')), mode='a+',
					          encoding='UTF-8', newline='') as data_csv:
						csv_writer = csv.writer(data_csv)
						data_csv.write((groupId, artifactId, version, asset_filename))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='get_asset_gav', description='get asset gav from url')
	parser.add_argument('-f', '--file', metavar='url_file', dest='url_file', required=True, help="component's url file")

	args = parser.parse_args()
	if not Path(args.url_file).exists():
		raise FileNotFoundError
	get_gav_from_url(args.url_file)
