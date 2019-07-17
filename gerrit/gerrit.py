"""
gerrit api
"""
import requests
import json
import logging
from urllib.parse import quote
import re
from datetime import datetime


pattern = re.compile('.+/.+')
# time_flag = datetime.strftime(datetime.now(), '%Y-%m-%d-since-%H-%M')
time_flag = datetime.now().__format__('%Y-%m-%d-since-%H-%M')
FORMAT = '%(levelname)s %(asctime)s  %(message)s'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('gerrit')
fmt = logging.Formatter('%(levelname)s %(asctime)s  %(message)s')
handler = logging.FileHandler('./gerrit-{}.log'.format(time_flag))
handler.setFormatter(fmt)
logger.addHandler(handler)

headers = {"accept": "application/json", "content-type": "application/json"}
auth_info = {"gerrit_auth_user", "gerrit_auth_password"}

gerrit_server = "http://gerrit.example.com"


# 调用gerrit的api公共方法
def gerrit_api(request_type, request_arg, params=None, success_status_code=200):
	request_url = gerrit_server + request_arg

	logger.info("GerritAPI: {} {} {}".format(request_type, request_url, params))
	ret_result = None

	try:
		result = requests.request(request_type, request_url, data=json.dumps(params), headers=headers, auth=auth_info)
		logger.debug("GerritResult: {} {}".format(result.status_code, result.text))
		if result.status_code == success_status_code:
			# 去除gerrit返回结果中包含的魔术前缀
			ret_result = json.loads(result.text.lstrip(")]]'").strip("\n"))
	except requests.exceptions.RequestException as e:
		logger.critical(e)
	return ret_result


def get_user_info_from_name(username):
	request_arg = "/accounts/?suggest&q=" + username
	result = gerrit_api("get", request_arg)
	if result:
		for user_info in result:
			if user_info.get("username").lower() == username.lower():
				return user_info
	return False


def get_group_info_from_name(group_name):
	request_arg = "/a/groups?query2=" + group_name
	result = gerrit_api("get", request_arg)
	if result:
		for group_info in result:
			if group_info.get("name").lower() == group_name.lower():
				return group_info
	return False


def get_group_list():
	request_arg = "/a/groups/"
	result = gerrit_api("get", request_arg)
	return result


# 创建应用
def create_project(app_name, desc=""):
	request_arg = "/a/projects/" + app_name
	params = {"description": desc}
	result = gerrit_api("put", request_arg, params=params, success_status_code=201)
	return result


# 初始化应用权限
def init_project_access_right(app_name, group_id):
	request_arg = "/a/projects/" + app_name + "/access"
	params = {"add": {"refs/*": {"permissions":{"read": {"rules": {group_id: {"action": "ALLOW"}}}}}}}
	result = gerrit_api("post", request_arg, params=params)
	return result


# 重载插件
def reload_plugin(plugin_name):
	request_arg = "/a/plugins/" + plugin_name + "/gerrit~reload"
	result = gerrit_api("post", request_arg)
	return result


def get_branch(app_name, branch_name):
	request_arg = "/a/projects/" + app_name + "/branches/" + branch_name
	result = gerrit_api("get", request_arg)
	return result


def create_branch(app_name, source_branch, target_branch):
	request_arg = "/a/projects/" + app_name + "/branches/" + target_branch
	params = {"revision": source_branch}
	result = gerrit_api("put", request_arg, params=params, success_status_code=201)
	return result


# 获取分支最新commitId
def get_branch_lstest_commit_id(app_name, branch_name):
	branch_info = get_branch(app_name, branch_name)
	if branch_info:
		return branch_info.get('revision')
	else:
		return False


def gerrit_get_api(api):
	url = gerrit_server + api
	try:
		with requests.get(url, headers=headers, auth=auth_info) as res:
			if res.status_code == 200 and res.text:
				ret_result = json.loads(res.text.lstrip(")]]'").strip("\n"))
				return ret_result
			else:
				logger.error("### url:{} status_code:{} result_text:{}".format(url, res.status_code, res.text))
				return False
	except requests.exceptions.HTTPError as e:
		logger.critical(e)
		return False


# get all projects info -> dict
def get_projects():
	api = '/a/projects/'
	return gerrit_get_api(api)


# get single project info -> tuple(id, state)
def get_project_from_name(app_name):
	api = '/a/projects/' + app_name
	ret = gerrit_get_api(api)
	if ret:
		return ret.get('id'), ret.get('state')
	else:
		return False


def get_project_user_access(app_name):
	api = '/a/projects/' + app_name + '/access'
	return gerrit_get_api(api)


def get_all_groups():
	api = '/a/groups/'
	rest = gerrit_get_api(api)
	groups_info = {}
	if rest:
		for group_name, group_items in rest.items():
			groups_info[group_name] = (group_items.get('id'), group_items.get('group_id'))
	return groups_info


def create_group(group_name: str):
	params = {'name': group_name, 'owner': group_name}
	if pattern.findall(group_name):
		group_name = quote(group_name, 'utf-8')
		api = '/a/groups/' + group_name
		url = gerrit_server + api
		try:
			with requests.put(url, headers=headers, auth=auth_info, data=json.dumps(params)) as res:
				if res.status_code == 201:
					logger.info("##succeed to create new gerirt group:{}".format(group_name))
					group_info = json.loads(res.text.lstrip(")]]").strip("\n"))
					return group_info.get('id')
				else:
					logger.info("##failed to create new gerrir group:{}".format(group_name))
					return False
		except requests.exceptions.HTTPError as e:
			logger.error(e)
			return False


def get_group_id_from_name(group_name):
	group_info = get_all_groups()
	if group_name in group_info.keys():
		group_id = group_info.get(group_name)[-1]
		return group_id
	else:
		logger.error("## group:{} not exists!".format(group_name))
		return False


def judge_project_user(app_name, username):
	project_info = get_project_from_name(app_name)
	user_rule_name = 'user:' + username
	if project_info[1] == 'ACTIVE':
		project_name = project_info[0]
		result = get_project_user_access(project_name)
		try:
			refs_rules = result.get('local').get('refs/*').get('permission').get('read').get('rules')
			user_rule = refs_rules.get(user_rule_name, False)
		except KeyError as e:
			logger.critical(e)
		else:
			return user_rule
	else:
		logger.warning("## project:{} is not ACTIVE".format(app_name))
		return False


def add_project_user_access_right(app_name, username):
	user_rule_name = 'user:' + username
	project_info = get_project_from_name(app_name)
	params = {"add": {"refs/*": {"permissions":{"read": {"rules": {user_rule_name: {"action": "ALLOW"}}}}}}}
	if project_info[1] == 'ACTIVE':
		project_name = project_info[0]
		api = '/a/projects/' + project_name + '/access'
		url = gerrit_server + api
		try:
			with requests.post(url, headers=headers, auth=auth_info, data=json.dumps(params)) as res:
				return True if res.status_code == 200 else False
		except requests.exceptions.HTTPError as e:
			logger.critical(e)
			return False
	else:
		logger.warning("### project:{} is not ACTIVE".format(app_name))
		return False


# grant project access rights for single group
def add_project_group_access_right(app_name, group_name):
	group_id = get_group_id_from_name(group_name)
	if group_id:
		params = {"add": {"refs/*": {"permissions": {"read": {"rules": {group_id: {"action": "ALLOW"}}}}}}}
		api = '/a/projects/' + app_name + '/access'
		url = gerrit_server + api
		try:
			with requests.post(url, headers=headers, auth=auth_info, data=json.dumps(params)) as res:
				if res.status_code == 200:
					logger.info("##succeed to add group:{} into project:{}".format(group_name, app_name))
					return True
				else:
					logger.error("##failed to add group:{} into project:{}".format(group_name, app_name))
					return False
		except requests.exceptions.HTTPError as e:
			logger.critical(e)
			return False
	else:
		logger.warning("## not find group:{}".format(group_name))
		return False


# multi add member list into a group
def add_group_members(group_name, user_name_list):
	group_id = get_group_id_from_name(group_name)
	accounts_id = []
	if group_id:
		api = '/a/groups/{}/members'.format(group_id)
		url = gerrit_server + api
		for user in user_name_list:
			user_info = get_user_info_from_name(user)
			if user_info:
				accounts_id.append(user_info.get('_account_id'))
		data = json.dumps({'member': accounts_id})

		with requests.post(url, headers=headers, auth=auth_info, data=data) as res:
			if res.status_code == 200:
				logger.info("##succeed to add member into group:{}".format(group_name))
				return True
			else:
				logger.critical("##failed to add member into group:{}".format(group_name))
				return False
	else:
		logger.error("## group_name:{} error".format(group_name))
		return False



