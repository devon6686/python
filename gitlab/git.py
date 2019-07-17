import gitlab
import logging
from datetime import datetime
import time
import csv
import re
from pathlib import Path


time_flag = datetime.strftime(datetime.now(), '%Y-%m-%d-since-%H-%M')
FORMAT = '%(levelname)s %(asctime)s  %(message)s'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('gitlab')
handler = logging.FileHandler('./git-{}.log'.format(time_flag))
fmt = logging.Formatter('%(levelname)s %(asctime)s  %(message)s')
handler.setFormatter(fmt)
logger.addHandler(handler)


gl = gitlab.Gitlab.from_config('local', ['./gl.cfg'])
gl_privileges = {'20': gitlab.REPORTER_ACCESS, '30': gitlab.DEVELOPER_ACCESS}


def cost_time(fn):
	def wrapper(*args, **kwargs):
		start_time = datetime.now()
		rt = fn(*args, **kwargs)
		delta = (datetime.now() - start_time).total_seconds()
		logger.info('### function:{} took {}s'.format(fn.__name__, delta))
		return rt


def manipulate_project_user(operate_type, user_id, project_id, **kwargs):
	try:
		project = gl.projects.get(project_id)
		if operate_type == 'juege':
			project.members.get(user_id)
		elif operate_type == 'add':
			privilege = gl_privileges[str(kwargs['access_level'])]
			user_info = {'user_id': user_id, 'access_level': privilege}
			project.members.create(user_info)
		elif operate_type == 'modify':
			privilege = gl_privileges[str(kwargs['access_level'])]
			member = project.members.get(user_id)
			member.access_level = privilege
			member.save()
		elif operate_type == 'remove':
			member = project.members.get(user_id)
			member.delete()
	except gitlab.exceptions.GitlabError as e:
		logger.critical("### failed to {} user_id:{} project_id:{}".format(operate_type, str(user_id), str(project_id)))
		logger.critical(e)
		return False
	else:
		logger.info("### succeed to {} user_id:{} project_id:{}".format(operate_type, str(user_id), str(project_id)))
		return True


def manipulate_group_user(operate_type, user_id, group_id, **kwargs):
	group = gl.groups.get(group_id)
	member = group.members.get(user_id)

	try:
		if operate_type == "judge":
			group.members.get(user_id)
		elif operate_type == "add":
			privilege = gl_privileges[str(kwargs['access_level'])]
			user_info = {'user_id': user_id, 'access_level': privilege}
			group.members.create(user_info)
		elif operate_type == "modify":
			privilege = gl_privileges[str(kwargs['access_level'])]
			member.access_level = privilege
			member.save()
	except gitlab.exceptions.GitlabError as e:
		logger.critical("### failed to {} group_id:{} user_id:{}".format(operate_type, str(group_id), str(user_id)))
		logger.critical(e)
		return False
	else:
		logger.info("### succeed to {} group_id:{} user_id:{}".format(operate_type, str(group_id), str(user_id)))
		return True


# 判断用户是否在project中
def get_project_member(user_id, project_id):
	result = manipulate_project_user('judge', user_id, project_id)
	return result


def add_project_member(user_id, project_id, access_level):
	result = manipulate_project_user('add', user_id, project_id, access_level=access_level)
	return  result


def edit_project_member(user_id, project_id, access_level):
	result = manipulate_project_user('modify', user_id, project_id, access_level=access_level)
	return  result


def remove_project_member(user_id, project_id, access_level):
	result = manipulate_project_user('remove', user_id, project_id, access_level=access_level)
	return  result


def get_group_member(user_id, group_id):
	rt = manipulate_group_user('judge', user_id, group_id)
	return rt


def add_group_member(user_id, group_id, access_level):
	rt = manipulate_group_user('add', user_id, group_id, access_level=access_level)
	return rt


def edit_group_member(user_id, group_id, access_level):
	rt = manipulate_group_user('modify', user_id, group_id, access_level=access_level)
	return rt


def remove_group_member(user_id, group_id, access_level):
	rt = manipulate_group_user('remove', user_id, group_id)
	return rt


def set_project_default_branch(project_id, branch_name='develop'):
	project = gl.projects.get(project_id)
	try:
		project.default_branch = branch_name
		project.save()
	except gitlab.exceptions.GitlabError as e:
		logger.critical("### failed to set default branch:{}".format(branch_name))
		logger.critical(e)
		return False
	else:
		logger.info("### succeed to set default branch:{}".format(branch_name))
		return True


# 新建库是通过从一个模版倒入，为了避免新建完成之后还要做一些初始化操作
@cost_time
def create_project(namespace_id, project_name, create_description, is_ut_jacoco):
	project_template_path = "lib/repo-template-1.tar.gz"
	if is_ut_jacoco == "true":
		project_template_path = "lib/repo-template-2.tar.gz"
	try:
		output = gl.projects.import_project(
			open(project_template_path, 'rb'),
			path=project_name,
			namespace=str(namespace_id),
			create_description=create_description
		)
	except gitlab.exceptions.GitlabError as e:
		logger.critical("### failed to create project:{}".format(project_name))
		logger.critical(e)
		return False
	else:
		project_import = gl.projects.get(output['id'], lazy=True).imports.get()
		while project_import.import_status != 'finished':
			time.sleep(1)
			project_import.refresh()
			logger.info("### succeed to create project:{} id:{}".format(project_name, str(output['id'])))
			project_id = output['id']
			set_project_default_branch(project_id)
			return project_id


def protect_branch(project_id, branch_name='master'):
	branch_info = {
		'name': branch_name,
		'merge_access_level': gitlab.MAINTAINER_ACCESS,
		'push_access_level': gitlab.MAINTAINER_ACCESS
	}
	try:
		project = gl.projects.get(project_id)
		p_branch = project.protectedbranches.create(branch_info)
	except gitlab.exceptions.GitlabError as e:
		logger.error("### failed to set project_id:{} branch:{}".format(str(project_id), branch_name))
		logger.error(e)
		return False
	else:
		logger.info("### succeed to set project_id:{} branch:{}".format(str(project_id), branch_name))
		return p_branch


def get_groups():
	groups = gl.groups.list()
	group_list = []
	if groups:
		for group in groups:
			group_list.append((group.attributes['full_path'], group.get_id()))
		group_list.sort()
	return group_list


def get_subgroups(namespace_id):
	group = gl.groups.get(namespace_id)
	subgroups = group.subgroups.list(all=True, as_list=False)
	subgroup_list = [sub.get_id() for sub in subgroups] if subgroups else []
	return subgroup_list


def get_project_subgroup(project_name):
	project_id = get_project_id_from_name(project_name)
	if project_id:
		project = gl.projects.get(project_id)
		return project.attributes.get('namespace').get('full_path') \
			if project.attributes.get('namespace').get('parent_id') else False
	else:
		logger.error("### not find project:{} in gtilab".format(project_name))
		return False


def get_uid_from_username(username):
	try:
		users = gl.users.list(username=username)
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return users[0].get_id() if users else False


def delete_user(user_id):
	try:
		user = gl.users.get(user_id)
		user.delete()
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return True


def get_project_from_name(project_name):
	project_id = get_project_id_from_name(project_name)
	project = gl.projects.get(project_id)
	project_info = {}
	if project_id:
		project_info['path_with_namespace'] = project.attributes['path_with_namespace']
		project_info['path'] = project.attributes['path']
		project_info['name'] = project.attributes['name']
		project_info['project_id'] = project.get_id()
		project_info['group_name'] = project.attributes['namespace']['full_path']
		project_info['group_id'] = project.attributes['namespace']['id']
	return project_info



def get_projects_from_group_id(namespace_id):
	group = gl.groups.get(namespace_id)
	projects_info = {}
	projects = group.projects.list(all=True, as_list=False)
	if projects:
		for project in projects:
			projects_info[project.attributes['name'].lower()] = project.get_id()
	return projects_info


def get_projects_full_path_from_group_id(group_id):
	projects_fullname_list = []
	projects_info = get_projects_from_group_id(group_id)
	for _, project_id in projects_info.items():
		project = gl.projects.get(project_id)
		if project:
			projects_fullname_list.append((project.attributes.get('path_with_namespace'), project.get_id()))
	return projects_fullname_list


@cost_time
def get_project_id_from_name(project_name):
	pass
	try:
		projects = gl.projects.list(all=True, as_list=False, search=project_name)
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		if projects:
			if len(projects) == 1:
				if projects[0].attributes['name'].lower() == project_name.lower() and \
						projects[0].attributes['namespace'].get('kind') == 'group':
					logger.info("### project info: name-{} id-{}".format(project_name, str(projects[0].get_id())))
					return projects[0].get_id()
				else:
					logger.error("### not find project:{} in gitlab".format(project_name))
					return False
			else:
				for project in projects:
					if project.attributes['name'].lower() == project_name.lower() and \
							project.attributes['namespace'].get('kind') == 'group':
						logger.info("### project info: name-{} id-{}".format(project_name, str(projects[0].get_id())))
						return project.get_id()
		else:
			return False


def get_group_from_name(group_name):
	group_info = {}
	groups = gl.groups.list(all=True, as_list=False)
	for group in groups:
		if group.attributes['full_path'].lower() == group_name.lower():
			group_info['id'] = group.attributes['id']
			group_info['path'] = group.attributes['path']
			group_info['full_path'] = group.attributes['full_path']
	return group_info


def get_project_branch_latest_commit(project_id, branch_name):
	project = gl.projects.get(project_id)
	try:
		commits = project.commits.list(all=False, page=1, per_page=10, query_parameters={'ref_name': branch_name})
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		if commits:
			latest_commit_id = commits[0].get_id()[:12]
			logger.info("### OK! branch:{} latest_commit:{}".format(branch_name, latest_commit_id))
			return latest_commit_id
		else:
			return False


def get_project_branches(project_id):
	project = gl.projects.get(project_id)
	branches_info = []
	branches = project.branches.list(all=True, as_list=False)
	if branches:
		for branch in branches:
			branches_info.append([branch.attributes['name'], branch.attributes['commit']['committed_date']])
	return branches_info


def get_project_path_name(project_name):
	flag = False
	projects = gl.projects.list(all=True, as_list=False)
	for project in projects:
		if project.attributes['name'].lower() == project_name.lower() and project.attributes['namespace'].get('kind') == 'group':
			flag = project.attributes['path']
			break
	return flag


def create_tag(project_id, tag_name, ref):
	tag_info = {'tag_name': tag_name, 'ref': ref}
	try:
		project = gl.projects.get(project_id)
		tag = project.tags.create(tag_info)
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return tag


def create_branch(project_id, source_branch, dest_branch):
	branch_info = {'branch': dest_branch, 'ref': source_branch}
	try:
		project = gl.projects.get(project_id)
		branch = project.branches.create(branch_info)
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return branch


def delete_branch(project_id, branch_name):
	try:
		project = gl.projects.get(project_id)
		project.branches.delete(branch_name)
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return True


def list_repository_tree(project_id, ref_name="develop", path=""):
	try:
		project = gl.projects.get(project_id)
		items = project.repository_tree(path=path, ref=ref_name)
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return items


def create_merge_requests(project_id, source_branch, target_branch, title, assignee_id=None):
	merge_msg = {
		'source_branch': source_branch,
		'target_branch': target_branch,
		'title': title
	}
	if assignee_id:
		merge_msg['assignee_id'] = assignee_id
	try:
		project = gl.projects.get(project_id)
		mr = project.mergerequests.create(merge_msg)
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return mr


def accept_merge_request(project_id, merge_request_id):
	try:
		project = gl.projects.get(project_id)
		mr = project.mergerequests.get(merge_request_id)
		mr.merge()
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return True


def update_merge_request(project_id, merge_request_id, state_event):
	try:
		project = gl.projects.get(project_id)
		mr = project.mergerequests.get(merge_request_id)
		mr.state_event = state_event
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return True

def get_merge_request_commits(project_id, merge_request_id):
	try:
		project = gl.projects.get(project_id)
		mr = project.mergerequests.get(merge_request_id)
		commits = mr.commits()
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return commits


def get_file(project_id, file_path, ref_name):
	try:
		project = gl.projects.get(project_id)
		f = project.files.get(file_path=file_path, ref=ref_name)
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return f


def transfer_to_group(project_id, group_id):
	try:
		group = gl.groups.get(group_id)
		group.transfer_project(to_project_id=int(project_id))
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return True


def add_project_hook(project_id, event_type='push_events'):
	url = "http://XXXX"
	hook_info = {"url": url, event_type: 1}
	try:
		project = gl.projects.get(project_id)
		hook = project.hooks.create(hook_info)
	except gitlab.exceptions.GitlabError as e:
		logger.critical(e)
		return False
	else:
		return hook


# 获取project下所有member信息，dict, {username: uid}
def get_project_all_members(project_name):
	pid = get_project_id_from_name(project_name)
	project = gl.project.get(pid)
	members = project.members.list(all=True, as_list=False)
	members_info = {}
	if members:
		for member in members:
			members_info[member.attributes.get('username')] = member.get_id()
	return members_info


# 批量添加用户到group下的项目中
def add_user_into_group_projects(group_name: str, group_members:list, access_level=gitlab.DEVELOPER_ACCESS):
	group_info = get_group_from_name(group_name)
	if group_info:
		gid = group_info.get('id')
		projects_in_group = get_projects_from_group_id(gid)
		if projects_in_group:
			for _, pid in projects_in_group.items():
				for username in group_members:
					uid = get_uid_from_username(username)
					if uid:
						if get_project_member(uid, gid):
							edit_project_member(uid, pid, access_level)
						else:
							add_project_member(uid, pid, access_level)


# 删除历史分支
def clean_branches(stand_date='2017-01-01'):
	groups_ex_list = ['group_ex_1', 'group_ex_2']
	branches_ex_list = ['develop', 'master']
	projects_ex_list = ['project1', 'project2']

	try:
		projects = gl.projects.list(archived=0, as_list=False)
	except gitlab.exceptions.GitlabError as e:
		logger.error(e)
	else:
		for project in projects:
			if project.attributes.get('path_with_namespace').split('/')[0].lower() not in groups_ex_list and \
				project.attributes.get('path').lower() not in projects_ex_list and \
				project.attributes['namespace'].get('kind') == 'group':
				logger.info("^^^ project:{}".format(project.attributes.get('path_with_namespace')))
				try:
					branches = project.branches.list(all=True, as_list=False)
				except gitlab.exceptions.GitlabError as e:
					logger.error("^^^ failed to get project:{} branches".format(project.attributes.get('path')))
					logger.error(e)
				else:
					for branch in branches:
						if not branch.attributes.get('default') and not branch.attributes.get('protected'):
							commit_date = branch.attributes['commit']['committed_date']
							commit_date_str = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%S.%f+08:00')
							if commit_date_str.strftime('%Y-%m-%d') < stand_date and \
								branch.attributes['name'] not in branches_ex_list:
								try:
									branch.delete()
								except gitlab.exceptions.GitlabError as e:
									logger.error("^^ failed to delete branch:{}".format(branch.attributes['name']))
									logger.error(e)
								else:
									logger.info("^^ succeed to delete branch:{} commit_date:{}".
									            format(branch.attributes['name'], commit_date))


# 删除gitlab上所有组内成员
def delete_all_group_members(groups_ex_list=None, members_ex_list=None):
	groups_info = get_groups()
	groups_with_no_member = []
	for item in groups_info:
		if item[0] not in groups_ex_list:
			group = gl.groups.get(item[1])
			members = group.members.all(all=True, as_list=False)
			count = 0
			if len(members):
				for member_dict in members:
					if member_dict.get('username').lower() not in members_ex_list:
						try:
							member = group.members.get(member_dict.get('id'))
							member.delete()
						except gitlab.exceptions.GitlabError as e:
							logger.critical("## failed to delete {} from group:{}".format(member_dict.get('username'), item[0]))
							logger.critical(e)
						else:
							logger.info("## failed to delete {} from group:{}".format(member_dict.get('username'), item[0]))
							count += 1
				if count == 0:
					logger.info("## group:{} has no member except members_ex_list".format(item[0]))
			else:
				groups_with_no_member.append(item[0])
				logger.info("## group:{} has no members!".format(item[0]))
	print(groups_with_no_member)


# 删除gitlab下所有组内特定的成员
def delete_member_from_all_groups(member_list, groups_ex_list=None):
	groups_info = get_groups()
	groups_with_no_member = []
	for item in groups_info:
		group_name, group_id = item
		if group_name not in groups_ex_list:
			group = gl.groups.get(item[1])
			members = group.members.all(all=True, as_list=False)
			count = 0
			if len(members):
				for member_dict in members:
					if member_dict.get('username').lower() in member_list:
						try:
							member = group.members.get(member_dict.get('id'))
							member.delete()
						except gitlab.exceptions.GitlabError as e:
							logger.critical(
								"## failed to delete {} from group:{}".format(member_dict.get('username'), item[0]))
							logger.critical(e)
						else:
							logger.info(
								"## failed to delete {} from group:{}".format(member_dict.get('username'), item[0]))
							count += 1
				if count == 0:
					logger.info("## group:{} has no member except members_ex_list".format(item[0]))
			else:
				groups_with_no_member.append(item[0])
				logger.info("## group:{} has no members!".format(item[0]))
	print(groups_with_no_member)


# 删除gitlab所有组内的用户access requests
def delete_user_access_request_in_group(groups_ex_list=None):
	groups_info = get_groups()

	def _delete_member(gid):
		group = gl.groups.get(gid)
		group_access_requests = group.accessrequests.list()
		if len(group_access_requests):
			for gar in group_access_requests:
				try:
					gar.delete()
				except gitlab.exceptions.GitlabError as e:
					logger.critical(e)
				else:
					logger.info("## succeed to delete group_id:{} user access requests".format(gid))

	for item in groups_info:
		if groups_ex_list is None:
			_delete_member(item[1])
		else:
			if item[0] not in groups_ex_list:
				_delete_member(item[1])


# 获取gitlab上所有project信息（project-full-path, pid）
@cost_time
def get_all_projects():
	project_file = './projects-{}.csv'.format(datetime.now().__format__("%Y-%m-%d"))
	if not Path(project_file):
		Path(project_file).touch()

	groups_id_list = get_groups()
	for group in groups_id_list:
		group_id = group[-1]
		single_group_projects_list = get_projects_full_path_from_group_id(group_id)
		subgroups = get_subgroups(group_id)
		if subgroups:
			for sg in subgroups:
				sg_projects_name_list = get_projects_full_path_from_group_id(sg)
				single_group_projects_list.extend(sg_projects_name_list)
		with open(project_file, 'a+', encoding='UTF-8', newline='') as data_csv:
			csv_writer = csv.writer(data_csv, dialect='excel')
			for item in single_group_projects_list:
				csv_writer.writerow(item)


# 列出projects时间段内的的commit次数
def count_project_commits(project_file: str, start_time='2019-01-01T00:00:00Z', until='2019-04-01T00:00:00Z'):
	app_pattern = re.compile('^offline_group')
	if not Path(project_file).exists():
		raise FileNotFoundError

	with open(project_file, encoding='UTF-8') as projects_info:
		for line in projects_info:
			if line.strip() and not app_pattern.findall(line):
				project_fullname, pid = line.split(',')
				app = gl.projects.get(pid)
				app_branches_info = get_project_branches(pid)
				count = 0
				for app_branch in app_branches_info:
					commits = app.commits.list(since=start_time, until=until, ref_name=app_branch[0])

				count += len(commits)
		content = (project_fullname, count, len(app_branches_info))
		with open("online-projects-{}.csv".format(datetime.now().__format__("%Y-%m-%d")), encoding='UTF-8', mode='a+', newline='') as data_csv:
			csv_writer = csv.writer(data_csv)
			csv_writer.writerow(content)

