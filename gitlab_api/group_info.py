import gitlab

gitlab_url = "http://127.0.0.1"
user = "root"
private_token = "WZ3x9_W3wAqpzrB5Z4xs"
gl = gitlab.Gitlab(gitlab_url, private_token, api_version='4')

# gitlab.GUEST_ACCESS = 10
# gitlab.REPORTER_ACCESS = 20
# gitlab.DEVELOPER_ACCESS = 30
# gitlab.MASTER_ACCESS = 40
# gitlab.OWNER_ACCESS = 50

# 遍历组的成员信息 username是登陆账号
# groups = gl.groups.list()
# for g in groups:
# 	print(g.attributes["name"], g.attributes["id"], g.attributes["web_url"])

# group = gl.groups.get(5)
# print(type(group))
# projects = group.projects.list()
# print(type(projects)
#
# projects_info = []
# for project in projects:
# 	# print(project, project.__dict__)
# 	projects_info.append(project.attributes["id"])
#
# print(projects_info)
#
# members_username = []
# members = group.members.list()
# for m in members:
# 	print(m.attributes["id"], m.attributes["username"])


def grant_privileges(username: str, groupname: str, glu: gitlab.Gitlab):
	def _get_groups():
		groups_info = {}
		for g in gl.groups.list():
			groups_info[g.attributes["name"]] = g.get_id()
		return groups_info

	def _get_members(group_id: int):
		group = gl.groups.get(group_id)
		members_info = {}
		for m in group.members.list():
			members_info[m.attributes["username"]] = m.get_id()
		return members_info

	# def _get_projects(group_id: int):
	# 	group = gl.groups.get(group_id)
	# 	projects_info = {}
	# 	for p in group.projects.list(visibility='private'):
	# 		projects_info[p.attributes["name"]] = p.get_id()
	# 	return projects_info

	def _get_projects():
		projects_info = {}
		for p in gl.projects.list():
			projects_info[p.attributes["namespace"]["name"]] = p.get_id()
		return projects_info

	groups = _get_groups()
	group_id = groups[groupname]
	members_info = _get_members(group_id)
	projects_info = _get_projects()
	project_id = projects_info[groupname]

	# 判断用户是否属于这个组
	if username in members_info.keys():
		raise("Error, {} already exists in {}".format(username, groupname))


# grant_privileges("devon123", "admin", gl)
# print(gl.projects.list()[0].attributes["namespace"]["name"])
# for p in gl.projects.list():
# 	print(p)

project = gl.projects.get(5)
branch = project.branches.get("master")
branch.protect()
print(branch)





