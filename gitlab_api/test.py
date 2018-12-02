import gitlab
import requests


gitlab_url = "http://127.0.0.1"
user = "root"
private_token = "WZ3x9_W3wAqpzrB5Z4xs"
gl = gitlab.Gitlab(gitlab_url, private_token, api_version='4')

# print(len(gl.projects.list(all=True)))
#
project_name = "360/p361"
# p = gl.projects.get(project_name)
# print(p)
# print(p.protectedbranches.list())
# print(p.protectedbranches.get('master'))

payload = {'private_token': private_token}
uri = '/api/v3/projects/5/repository/branches/master'
url = gitlab_url + uri
r = requests.get(url, params=payload)
print(r.text)

