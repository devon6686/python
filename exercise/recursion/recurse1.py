#!/usr/bin/env python3
"""
递归方法处理：1234 -> 4321
处理方法：
	1. 将1234视作数字处理
	2. 将1234视作字符串进行处理
"""


def fn(num):
	if num < 10:
		# print(num)
		return num
	num, b = divmod(num, 10)
	print(b, end='')
	return fn(num)


print(fn(12345))