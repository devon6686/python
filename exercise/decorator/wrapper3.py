#!/usr/bin/env python3
# coding=utf-8

"""
装饰器缺点解决方法1：
	通过copy_properties函数将被包装函数的属性覆盖掉包装函数；
	凡是被装饰的函数都需要复制这些属性；
	可以将复制属性的函数构建成装饰器函数，带参装饰器；
"""


def copy_properties(src, dst):

	dst.__name__ = src.__name__
	dst.__doc__ = src.__doc__


def logger(fn):
	def wrapper(*args, **kwargs):
		"""I am wrapper"""
		print('begin')
		x = fn(*args, **kwargs)
		print('end')
		return x
	copy_properties(fn, wrapper)
	return wrapper


@logger  # add = logger(add)
def add(x, y):
	"""This is a function for add"""
	return x + y


print("name={}, doc={}".format(add.__name__, add.__doc__))