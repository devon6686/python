#!/usr/bin/env python3
# coding=utf-8

"""
提供一个函数，被封装函数属性---copy-->包装函数属性，改造成带参装饰器
"""


def copy_properties(src):
	def _copy(dst):
		dst.__name__ = src.__name__
		dst.__doc__ = src.__doc__
		return dst
	return _copy


def logger(fn):
	@copy_properties(fn)    # wrapper = wrapper(fn)(wrapper)
	def wrapper(*args, **kwargs):
		"""I am wrapper"""
		print('begin')
		x = fn(*args, **kwargs)
		print('end')
		return x
	return wrapper


@logger     # add = logger(add)
def add(x, y):
	"""This is a function for add"""
	return x + y


print("name={}, doc={}".format(add.__name__, add.__doc__))