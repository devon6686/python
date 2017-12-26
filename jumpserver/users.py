#!/usr/bin/env python3
"""
批量添加用户信息
"""
import uuid


users_csv = "/Users/devon/Downloads/users.csv"
users_txt = "/Users/devon/Downloads/users.txt"


def gen_user_record(user_id, name, username, email, role='User', active='True', group='developer'):
	user_info_1 = ','.join(str(i) for i in [user_id, name, username, email, role])
	# print(user_info_1)
	user_info_2 = active + ','*2 + group
	user_line = user_info_1 + ','*3 + user_info_2
	# print(user_record)
	return(user_line)


users_list = []
with open(users_txt) as users:
	for user in users.read().split('\n'):
		r_username, r_name = user.split()
		r_user_id = uuid.uuid4()
		r_email = r_username + '@123.com'
		r_user_info = gen_user_record(r_user_id, r_name, r_username, r_email)
		users_list.append(r_user_info)
print(users_list)


with open(users_csv, mode='a+') as csv_users:
	for user_record in users_list:
		csv_users.write(user_record + '\n')
		csv_users.flush()



