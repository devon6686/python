#!/usr/bin/env python3
# coding=utf-8

"""
带参装饰器
	需求： 获取函数的执行时长，对时长超过阈值的函数记录一下；
"""
import time
import datetime


def copy_properties(src):
	def _copy(dst):
		dst.__name__ = src.__name__
		dst.__doc__ = src.__doc__
		return dst
	return _copy


def logger(duration):
	def _logger(fn):
		@copy_properties(fn)  # wrapper = wrapper(fn)(wrapper)
		def wrapper(*args, **kwargs):
			start = datetime.datetime.now()
			ret = fn(*args, **kwargs)
			delta = (datetime.datetime.now() - start).total_seconds()
			print('so slow') if delta > duration else print('so fast')
			return ret
		return wrapper
	return _logger


@logger(3)  # add = logger(5)(add)
def add(x, y):
	time.sleep(3)
	return x + y


print(add(5, 6))