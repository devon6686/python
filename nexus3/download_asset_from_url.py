"""
根据url批量下载asset
"""
from pathlib import Path
import requests
import logging
import argparse
from datetime import datetime

FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nexus')
handler = logging.FileHandler("dl-().log".format(datetime.now().strftime("%Y-%m-%d")))
fmt = logging.Formatter(FORMAT)
handler.setFormatter(fmt)
logger.addHandler(handler)


def download_maven_asset(download_url, storage_path):
	package_path = str(Path(storage_path) / Path(download_url.strip().split('/')[-1]))
	try:
		with requests.get(download_url, stream=True) as response:
			with open(package_path, 'wb') as fd:
				for chunk in response.iter_content(chunk_size=1024):
					fd.write(chunk)
	except Exception as e:
		logger.error(e)
	else:
		logger.info("## succeed to download asset: {}".format(download_url.strip().split('/')[-1]))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='download_asset', description='download assets from url')
	parser.add_argument('-d', '--directory', metavar='storage_path', dest='storage_path', required=True,
	                    help="storage path for packages")
	parser.add_argument('-f', '--file', metavar='url_file', dest='url_file', required=True, help='url file')
	args = parser.parse_args()

	if not Path(args.url_file).exists() or not Path(args.storage_path).exists():
		raise FileNotFoundError

	with open(args.url_file, encoding='UTF-8') as f:
		for line in f:
			if line.strip():
				download_maven_asset(line.strip(), args.storage_path)

