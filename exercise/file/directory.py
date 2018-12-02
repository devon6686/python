#!/usr/bin/env python3
"""
遍历并判断文件类型，如果是目录是否可以判断其是否为空？
"""

from pathlib import Path


file = '/tmp/test/1.txt'
p = Path(file)

for x in p.parents[len(p.parents)-2].iterdir():
	print(x, end='\t')

	if x.is_dir():
		flag = False
		for _ in x.iterdir():
			flag = True
			break
		print('dir', 'Not Empty' if flag else 'Empty', sep='\t')
	elif x.is_file():
		print('file')
	else:
		print('other file')