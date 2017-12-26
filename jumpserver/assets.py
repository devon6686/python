#!/usr/bin/env python3
"""
批量添加资产信息
"""

import uuid


assets_file = "/Users/devon/Downloads/assets.csv"
hosts_file = "/Users/devon/Downloads/hosts.txt"


def gen_record(host_id, ip, host_name, port=22):
	cluster = "Default"
	active = "True"
	os_type = "VM"
	env = "Test"
	status = "In use"
	user = "admin_user"
	assets_group = "Default"
	property_list = [host_id, ip, host_name, port, cluster, active, os_type, env, status, user]

	property_part1 = ','.join(str(j) for j in property_list)
	property_part2 = ','*22
	row = property_part1 + property_part2 + assets_group
	return row


record_list = []
with open(hosts_file) as hosts_list:
	hosts = hosts_list.read().split('\n')
	for host in hosts:
		ip = host
		hostname = ip
		hostId = uuid.uuid4()
		record_list.append(gen_record(hostId, ip, hostname))
print(record_list)


with open(assets_file, mode='a+') as assets:
	for record in record_list:
		record = record + '\n'
		assets.write(record)
		assets.flush()
