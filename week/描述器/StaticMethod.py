#!/usr/bin/env python3
from functools import partial


class StaticMethod:
	def __init__(self, fn):
		# print(fn)
		self.fn = fn

	def __get__(self, instance, owner):
		print(self, instance, owner)
		return self.fn


class ClassMethod:
	def __init__(self, fn):
		# print(fn)
		self.fn = fn

	def __get__(self, instance, cls):
		print(self, instance, cls)
		# return self.fn(owner)
		return partial(self.fn, cls)


class A:

	@StaticMethod
	def foo():
		print('static')

	@ClassMethod
	def bar(cls):
		print(cls.__name__)


# f = A.foo
# print(f)
# f()

f = A.bar
print(f)
f()