import gitlab
import logging

gitlab_url = "http://127.0.0.1"
user = "root"
private_token = "WZ3x9_W3wAqpzrB5Z4xs"
gl = gitlab.Gitlab(gitlab_url, private_token)

log = logging.basicConfig(level=logging.INFO)
# def create_branch(project_id: int, branch_name, gl):
# 	project = gl.projects.get(project_id)
#
branch_name_master = "master-i18n"
branch_name_develop = "develop-i18n"
# project = gl.projects.get(5)
master_i18n_info = {'branch': branch_name_master, 'ref': 'master'}
develop_i18n_info = {'branch': branch_name_develop, 'ref': branch_name_master}


def set_protected_branch(project, branch_name):
	try:
		project.branches.get(branch_name)
	except gitlab.exceptions.GitlabGetError:
		logging.error("{} not exists!".format(branch_name))
	else:
		try:
			project.protectedbranches.get(branch_name)
		except gitlab.exceptions.GitlabGetError:
			logging.info("{} will be set protected".format(branch_name))
			project.protectedbranches.create({
				'name': 'master-i18n',
				'merge_access_level': gitlab.MASTER_ACCESS,
				'push_access_level': gitlab.MASTER_ACCESS
			})
		else:
			logging.info("{} already is a protected branch".format(branch_name))


def create_branch(project, branch_name_master, branch_name_develop):
	try:
		project.branches.get(branch_name_master)
	except gitlab.exceptions.GitlabGetError:
		# logging.error("Branch: {} not found".format(branch_name_master))
		logging.info("###Project: {} Branch: {} and {} will be created!".format(project.attributes["name"], branch_name_master, branch_name_develop))
		project.branches.create(master_i18n_info)
		set_protected_branch(project, branch_name_master)
		project.branches.create(develop_i18n_info)
	else:
		logging.info("----Project: {} already have branch: {}".format(project.attributes["name"], branch_name_master))
		set_protected_branch(project, branch_name_master)
		try:
			project.branches.get(branch_name_develop)
		except gitlab.exceptions.GitlabGetError:
			logging.info("###Project: {} Branch: {} will be created!".format(project.attributes["name"], branch_name_develop))
			project.branches.create(develop_i18n_info)
		else:
			logging.info("****Project: {} already have branches: {} and {}".format(project.attributes["name"], branch_name_master, branch_name_develop))


project_name = "360/p361"
project = gl.projects.get(project_name)
create_branch(project, branch_name_master, branch_name_develop)
