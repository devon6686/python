import gitlab
import logging
import time


FORMAT = '%(levelname)s %(asctime)s  %(message)s'
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('gitlab')
handler = logging.FileHandler('./git.log')
fmt = logging.Formatter('%(levelname)s %(asctime)s  %(message)s')
handler.setFormatter(fmt)
log.addHandler(handler)


gl = gitlab.Gitlab.from_config('local', ['./gitlab.cfg'])
privileges = {'20': gitlab.REPORTER_ACCESS, '30': gitlab.DEVELOPER_ACCESS}

# manipulate group


def get_groups():
	groups = gl.groups.list(all=True, as_list=False)
	if groups:
		groups_info = {}
		for group in groups:
			groups_info[group.attributes['name']] = group.get_id()
		return groups_info
	else:
		log.error("no group find in gitlab!")
		return False


def create_group(name, path, **kwargs):
	group_info = {'name': name, 'path': path}
	if kwargs:
		group_info.update(kwargs)
	try:
		group = gl.groups.create(group_info)
	except gitlab.exceptions.GitlabError as e:
		log.error('failed to create group:{}!'.format(name))
		log.error(e)
		return False
	else:
		log.info('succeed to create group:{}!'.format(name))
		return group


def delete_group_from_name(name):
	name = str(name)
	groups_info = get_groups()
	if name in groups_info.keys():
		try:
			gl.groups.delete(groups_info[name])
		except gitlab.exceptions.GitlabError as e:
			log.error('failed to delete group:{}!'.format(name))
			log.error(e)
			return False
		else:
			log.info('succeed to delete group:{}'.format(name))
			return True
	else:
		log.info('group:{} not exists in gitlab!'.format(name))
		return True


def get_group_id_from_name(name):
	try:
		group = gl.groups.get(name)
	except gitlab.exceptions.GitlabError as e:
		log.error("group:{} not find!".format(name))
		log.error(e)
		return False
	else:
		group_id = group.get_id()
		return group_id


# manipulate user
def get_users():
	users = gl.users.list(all=True, as_list=False)
	if users:
		users_info = {}
		for user in users:
			users_info[user.attributes['username']] = user.get_id()
		return users_info
	else:
		log.error("No user find in gitlab!")
		return False


def get_user_id_from_username(username):
	users = get_users()
	if str(username) in users.keys():
		return users[str(username)]
	else:
		log.error("user:{} not exists!".format(str(username)))
		return False


def create_user(username, name, email, **kwargs):
	# username is login name
	user_info = {'username': username, 'name': name, 'email': email}
	if kwargs:
		user_info.update(kwargs)
	try:
		user = gl.users.create(user_info)
	except gitlab.exceptions.GitlabError as e:
		log.error('failed to create user:{} !'.format(username))
		log.error(e)
		return False
	else:
		log.info('succeed to create user:{} !'.format(username))
		return user


def delete_user(username):
	users = get_users()
	if str(username) in users.keys():
		try:
			gl.users.delete(users[str(username)])
		except gitlab.exceptions.GitlabError as e:
			log.error("failed to delete user:{} !".format(str(username)))
			log.error(e)
			return False
		else:
			log.info("succeed to delete user:{} !".format(str(username)))
			return True
	else:
		log.info("user:{} not exists!".format(username))
		return True


# manipulate project
def get_projects():
	try:
		projects = gl.projects.list(all=True, as_list=False, order_by='name')
	except gitlab.exceptions.GitlabError as e:
		log.error(e)
		return False
	else:
		if projects:
			projects_info = {}
			for project in projects:
				projects_info[project.attributes['name']] = (project.get_id(), project.attributes['path'])
			return projects_info
		else:
			log.error("not find any project in gitlab")
			return False


def create_project_with_import(project_name, group_name):
	template_file = './scm_repo-template-3_export.tar.gz'
	group_id = get_group_id_from_name(group_name)
	try:
		output = gl.projects.import_project(open(template_file, 'rb'), path=project_name, namespace=group_id)
	except gitlab.exceptions.GitlabError as e:
		log.error(e)
		return False
	else:
		project_import = gl.projects.get(output['id'], lazy=True).imports.get()
		while project_import.import_status != 'finished':
			time.sleep(1)
			project_import.refresh()
		log.info("succeed to import project:{} to group:{}".format(project_name, group_name))
		return True


def create_project_in_group(name, group_msg, **kwargs):
	if type(group_msg) == int:
		namespace_id = group_msg
	elif type(group_msg) == str:
		namespace_id = get_group_id_from_name(group_msg)
	else:
		log.critical("second parameter type error!")
		return False

	project_info = {'name': str(name), 'namespace_id': namespace_id}
	if kwargs:
		project_info.update(kwargs)
	try:
		project = gl.projects.create(project_info)
	except gitlab.exceptions.GitlabError as e:
		log.error("failed to create project:{}".format(name))
		log.error(e)
		return False
	else:
		log.info('succeed to create project:{} in group:{}'.format(str(name), str(group_msg)))
		return project


def get_project_members(project_msg):
	if type(project_msg) == str:
		project_id = get_project_id_from_name(project_msg)
	elif type(project_msg) == int:
		project_id = project_msg
	else:
		log.critical('parameter type error!')
		return False

	try:
		project = gl.projects.get(project_id)
		members = project.members.all(all=True)
	except gitlab.exceptions.GitlabError as e:
		log.critical(e)
		return False
	else:
		members_info = {}
		if members:
			for member in members:
				members_info[member.attributes['username']] = member.get_id()
		return members_info


def get_project_id_from_name(project_name):
	projects = get_projects()
	if str(project_name) in projects.keys():
		project_id = projects[str(project_name)][0]
		return project_id
	else:
		return False


def judge_project_member(username, project_name):
	project_id = get_project_id_from_name(project_name)
	user_id = get_user_id_from_username(username)
	try:
		project = gl.projects.get(project_id)
		project.members.get(user_id)
	except gitlab.exceptions.GitlabError as e:
		log.critical(e)
		return False
	else:
		log.info("user:{} exists in project:{}!".format(username, project_name))
		return True


def manipulate_project_user(operate, username, project_name, **kwargs):
	user_id = get_user_id_from_username(username)
	project_id = get_project_id_from_name(project_name)
	project = gl.projects.get(project_id)

	try:
		if operate == 'add':
			privilege = privileges[str(kwargs['access_level'])]
			user_info = {'user_id': user_id, 'access_level': privilege}
			project.members.create(user_info)
		elif operate == 'edit':
			privilege = privileges[str(kwargs['access_level'])]
			member = project.members.get(user_id)
			member.access_level = privilege
			member.save()
		elif operate == 'remove':
			project.members.delete(user_id)
		else:
			return False
	except gitlab.exceptions.GitlabError as e:
		log.critical(e)
		return False
	else:
		log.info("succeed to {} user:{} in project:{}".format(operate, username, project_name))
		return True


def add_project_user(username, project_name, access_level=20):
	result = manipulate_project_user('add', username, project_name, access_level=access_level)
	return result


def edit_project_user(username, project_name, access_level=20):
	result = manipulate_project_user('edit', username, project_name, access_level=access_level)
	return result


def remove_project_user(username, project_name):
	result = manipulate_project_user('remove', username, project_name)
	return result


def transfer_project(project_name, group_name):
	group_id = get_group_id_from_name(group_name)
	group = gl.groups.get(group_id)
	project_id = get_project_id_from_name(project_name)
	try:
		group.transfer_project(project_id)
	except gitlab.exceptions.GitlabError as e:
		log.error("failed to transfer project:{} to group:{}".format(project_name, group_name))
		log.error(e)
		return False
	else:
		log.info("succeed to transfer project:{} to group:{}".format(project_name, group_name))
		return True


# manipulate project branch
def get_project_branches(project_name):
	project_id = get_project_id_from_name(project_name)
	project = gl.projects.get(project_id)
	try:
		branches = project.branches.list(all=True, as_list=False)
	except gitlab.exceptions.GitlabError as e:
		log.error(e)
		return False
	else:
		branches_list = []
		if branches:
			for branch in branches:
				# print(branch.attributes['name'], branch.attributes['commit']['id'])
				branches_list.append(branch.attributes['name'])
		return branches_list


def judge_branch_in_project(project_name, branch_name):
	branches = get_project_branches(project_name)
	if branches and branch_name in branches:
		log.info("branch:{} exists project:{}".format(branch_name, project_name))
		return True
	else:
		return False


def manipulate_project_branch(operate, project_name, branch_name, ref='master'):
	project_id = get_project_id_from_name(project_name)
	project = gl.projects.get(project_id)
	try:
		if operate == 'create':
			branch_info = {'branch': branch_name, 'ref': ref}
			project.branches.create(branch_info)
		elif operate == 'delete':
			project.branches.delete(branch_name)
		elif operate == 'protect':
			branch = project.branches.get(branch_name)
			branch.protect()
		elif operate == 'unprotect':
			branch = project.branches.get(branch_name)
			branch.unprotect()
		else:
			return False
	except gitlab.exceptions.GitlabError as e:
		log.error(e)
		return False
	else:
		log.info("succeed to {} branch:{}".format(operate, branch_name))
		return True


def create_project_branch(project_name, branch_name, ref='master'):
	result = manipulate_project_branch('create', project_name, branch_name, ref=ref)
	return result


def delete_project_branch(project_name, branch_name):
	result = manipulate_project_branch('delete', project_name, branch_name)
	return result


def set_branch_protect(project_name, branch_name):
	result = manipulate_project_branch('protect', project_name, branch_name)
	return result


def unset_branch_protect(project_name, branch_name):
	result = manipulate_project_branch('unprotect', project_name, branch_name)
	return result


create_project_with_import('repo-template-1', 'scm')


