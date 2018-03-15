#!/usr/bin/env python3
# coding=utf-8

"""
装饰器
"""

import datetime
import time


def logger(fn):
	def wrapper(*args, **kwargs):
		# before
		start = datetime.datetime.now()
		print('args={},kwargs={}'.format(args, kwargs))
		rt = fn(*args, **kwargs)
		# end
		delta = (datetime.datetime.now() - start).total_seconds()
		print('function {} took {}s'.format(fn.__name__, delta))
		return rt
	return wrapper


@logger
def add1(x, y):
	print("----call add1-----")
	time.sleep(2)
	return x + y


print(add1(4, 5))