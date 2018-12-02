#!/usr/bin/env python3
"""
对实例的数据进行校验
"""


class Typed:
	def __init__(self, ttype):
		self.ttype = ttype

	def __get__(self, instance, owner):
		pass

	def __set__(self, instance, value):
		print('T_set', self, instance, value)
		if not isinstance(value, self.ttype):
			raise ValueError(value)


class Person:
	name = Typed(str)
	age = Typed(int)

	def __init__(self, name: str, age: int):
		self.name = name
		self.age = age


# p1 = Person('tom', '18')


