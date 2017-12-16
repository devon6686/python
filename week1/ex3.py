#!/usr/bin/env python3
"""
用户管理
如果输入delete，则让用户输入”用户名”格式字符串，根据用户名查找dict中数据，若存在数据则将该数据移除，若用户数据不存在，则提示不存在;

如果输入update，则让用户输入”用户名:年龄:联系方式”格式字符串，并使用:分隔用户数据，根据用户名查找dcit中数据，若存在数据则将改数据更新数据，若用户数据不存在，则提示不存在;

如果用户输入find，则让用户输入”用户名”格式字符串，根据用户名查找dict中数据包含输入字符串的用户信息，并打印;

如果用户输入list，则打印所有用户信息;

打印用户第一个行数据为用户信息描述，从第二行开始为用户数据;

如果用户输入exit，则打印退出程序，并退出 ;

"""
users = {
	'tom': [20, 15128373798],
	'jim': [30, 13873738383],
	'lily': [18, 16765373737],
	'alice': [22, 18736649233]
}
user_functions = {
	'delete': '用户名',
	'update': '用户名:年龄:联系方式',
	'find': '用户名',
	'list': '所有用户信息',
	'exit': '退出程序'
}

while True:
	choice = input("""User Management Functions:
			1. delete
			2. update
			3. find
			4. list
			5. exit
	Please input your choice: \n""")
	if choice == 'delete':
		username = input('请输入{}：'.format(user_functions['delete']))
		result = users.pop(username, '\t用户{}不存在'.format(username))
		print(result)
	elif choice == 'update':
		user_info = input('请输入{}：'.format(user_functions['update']))
		username, age, phone = user_info.split(':')
		if users.get(username):
			users.update({username: [age, phone]})
			print('用户{}信息已更新,信息如下：'.format(username))
			print('\t用户:{}\n\t更新内容:{}'.format(username, users[username]))
		else:
			print('\t用户{}不存在'.format(username))
	elif choice == 'find':
		username = input('请输入{}：'.format(user_functions['find']))
		result = users.get(username, '\t用户{}不存在'.format(username))
		print(result)
	elif choice == 'list':
		print('{}：\n'.format(user_functions['list']))
		for userinfo in users.items():
			print(userinfo)
	elif choice == 'exit':
		print('{}'.format(user_functions['exit']))
		break
	else:
		print("Please input right choice!")
