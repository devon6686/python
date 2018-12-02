#!/usr/bin/env python3
"""
对实例的数据进行校验
"""
import inspect


class Typed:
	def __init__(self, ttype):
		self.ttype = ttype

	def __get__(self, instance, owner):
		pass

	def __set__(self, instance, value):
		print('T_set', self, instance, value)
		if not isinstance(value, self.ttype):
			raise ValueError(value)


class TypeAssert:
	def __init__(self, cls):
		self.cls = cls
		params = inspect.signature(self.cls).parameters
		print(params)
		for name, param in params.items():
			print(name, param.annotation)
			if param.annotation != param.empty:
				setattr(self.cls, name, Typed(param.annotation))
		print(self.cls.__dict__)

	def __call__(self, name, age):
		p = self.cls(name, age)
		return p


@TypeAssert
class Person:
	# name = Typed(str)
	# age = Typed(int)

	def __init__(self, name: str, age: int):
		self.name = name
		self.age = age


# p1 = Person('tom', 18)
p2 = Person('tom', '18')


