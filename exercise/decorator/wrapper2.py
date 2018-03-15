#!/usr/bin/env python3
# coding=utf-8

"""
此装饰器的缺点：
	原函数对象的属性都被修改了，而使用装饰器，需求是为了查看原函数的属性，与需求冲突

解决方法：@copy_properties(fn)
"""


def logger(fn):
	def wrapper(*args, **kwargs):
		'I am wrapper'
		print('begin')
		x = fn(*args, **kwargs)
		print('end')
		return x
	return wrapper


@logger     # add = logger(add)
def add(x, y):
	"""
	This is a function for add
	"""
	return x + y


print("name={}, doc={}".format(add.__name__, add.__doc__))