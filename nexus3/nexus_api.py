"""
nexus3 API
__author__ = "wanglinxiang"
"""

import logging
import requests
import re
from pathlib import Path
from datetime import datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder


FORMAT = "%(levelname)s %(asctime)s %(message)s"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('nexus')
handler = logging.FileHandler("repo-().log".format(datetime.now().strftime("%Y-%m-%d")))
fmt = logging.Formatter(FORMAT)
handler.setFormatter(fmt)
logger.addHandler(handler)

repos = {'release': 'releases', 'snapshot': 'snapshots'}
BASE_URL = "http://nexus.example.com"
headers = {'Accept': 'application/json'}
auth_info = ('admin', 'admin123')

regex_version = re.compile('snapshot')


def upload_maven_asset(asset_group: str, asset_name: str, asset_version: str, repo: str,
                       asset_ext='jar', storage='/data/packages'):
	api = '/service/rest/v1/components'
	nexus_api_address = BASE_URL + api
	asset_full_location = "{}/{}-{}.{}".format(storage, asset_name, asset_version, asset_ext)
	if not Path(asset_full_location).exists():
		raise FileNotFoundError
	if regex_version.findall(asset_version.lower()):
		raise ValueError("## snapshots repository is not supported to upload components with api, "
		                 "please use mvn client command!")
	params = (('repository', repo),)
	asset_fullname = asset_full_location.split('/')[-1]
	files = MultipartEncoder(
		{
			'maven2.groupId': asset_group,
			'maven2.artifactId': asset_name,
			'maven2.version': asset_version,
			'maven2.asset1.extension': asset_ext,
			'maven2.asset1': (asset_fullname, open(asset_full_location, 'rb'), 'text/plain')
		}
	)
	try:
		with requests.post(nexus_api_address, headers={'Content-Type': files.content_type},
		                   params=params, data=files, auth=auth_info) as response:
			logger.info("### http status code:{}".format(response.status_code))
			if response.status_code == 204:
				logger.info("## succeed to upload asset({}) to repository({})".format(asset_fullname, repo))
				return True
			else:
				logger.error("## failed to upload asset({}) to repository({})".format(asset_fullname, repo))
				return False
	except requests.exceptions.HTTPError as e:
		logger.error(e)
		return False


def check_maven_asset(asset_group, asset_name, asset_version, asset_ext='jar'):
	api = '/service/rest/v1/search/assets'
	nexus_api_address = BASE_URL + api
	params = ['repository', 'format', 'maven.groupId', 'maven.artifactId', 'maven.baseVersion', 'maven.extension']
	if regex_version.findall(asset_version.lower()):
		repo_name = repos.get('snapshot')
	else:
		repo_name = repos.get('release')

	values = [repo_name, 'maven2', asset_group, asset_name, asset_version, asset_ext]
	data = dict(zip(params, values))
	asset_info = '/'.join(values)
	try:
		with requests.get(nexus_api_address, headers=headers, params=data) as response:
			result = response.json()
			if result['items']:
				logger.info("## maven asset:{} exists!".format(result.get('items')[0].get('downloadUrl')))
				return True
			else:
				logger.error("## maven asset:{} not find!".format(asset_info))
				return False
	except requests.exceptions.HTTPError as e:
		logger.error(e)
		return False


# dev: npm-local, version-snapshot
# test: npm-pajk, version
def search_npm_asset(asset_name, asset_version, env_type):
	api = '/service/rest/v1/search/assets'
	nexus_api_address = BASE_URL + api
	params = {'name': asset_name}

	if env_type == 'dev':
		params['version'] = asset_version + '-snapshot'
		params['repository'] = 'npm-local'
	elif env_type == 'test':
		params['version'] = asset_version
		params['repository'] = 'npm-pajk'
	print(params)

	try:
		with requests.get(nexus_api_address, headers=headers, params=params) as response:
			result = response.json()
			if result.get('items'):
				if len(result.get('items')) == 1:
					asset_id = result.get('items')[0].get('id')
					logger.info("## find asset:{} in repo:{}".format(params.get('name') + '-' + asset_version + '.tgz', params.get('repository')))
					return asset_id
				else:
					logger.error("## not find asset:{} in repo:{}!".format(params.get('name') + '-' + asset_version, params.get('repository')))
				return False
	except requests.exceptions.HTTPError as e:
		logger.error(e)
		return False


def check_npm_asset(asset_name, asset_version, env_type):
	api = '/service/rest/v1/search/assets'
	nexus_api_address = BASE_URL + api
	params = {'name': asset_name}
	if env_type == 'dev':
		params['version'] = asset_version + '-snapshot'
		params['repository'] = 'npm-local'
	elif env_type == 'test':
		params['version'] = asset_version
		params['repository'] = 'npm-pajk'
	print(params)

	try:
		with requests.get(nexus_api_address, headers=headers, params=params) as response:
			result = response.json()
			return True if result['items'] else False
	except requests.exceptions.HTTPError as e:
		logger.error(e)
		return False


def delete_npm_asset(asset_name, asset_version, env_type):
	asset_id = search_npm_asset(asset_name, asset_version, env_type)
	if asset_id:
		api = '/service/rest/v1/assets' + str(asset_id)
		nexus_api_address = BASE_URL + api

		try:
			with requests.delete(nexus_api_address, headers=headers, auth=auth_info) as response:
				logger.info("## http status-code:{}".format(response.status_code))
				if response.status_code == 204:
					logger.info("## succeed to delete npm asset:{}".format(asset_name + "-" + asset_version))
					return True
				else:
					logger.error("## failed to delete asset:{} version:{} env:{}".format(asset_name, asset_version, env_type))
					return False
		except requests.exceptions.HTTPError as e:
			logger.error(e)
			return False


def upload_npm_asset(asset_name, asset_version, env_type, storage='packages/'):
	api = '/service/rest/v1/components'
	nexus_api_address = BASE_URL + api
	define = {
		'dev': {'flag': 'snapshot', 'repo': 'npm-local'},
		'test': {'flag': '-', 'repo': 'npm-pajk'}
	}

	if env_type not in define.keys():
		raise ValueError
	asset_fullname = asset_name + define.get(env_type).get('flag') + asset_version + '.tgz'
	asset_file = Path(storage) / Path(asset_fullname)
	params = ('repository', define.get(env_type).get('repo'))
	if not asset_file.exists():
		raise FileNotFoundError
	asset_content = open(str(asset_file), 'rb')
	try:
		with requests.post(nexus_api_address, params=params, files={'npm.asset': (asset_fullname, asset_content)}) as response:
			logger.info("## http status_code:{}".format(response.status_code))
			if response.status_code == 204:
				logger.info("## succeed to upload npm asset:{} to repo:{}".format(asset_fullname, define.get(env_type).get('repo')))
				return True
			else:
				logger.error("## failed to upload npm asset:{} to repo:{}".format(asset_fullname, define.get(env_type).get('repo')))
				return False
	except requests.exceptions.HTTPError as e:
			logger.error(e)
			return False






