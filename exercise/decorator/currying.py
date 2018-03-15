#!/usr/bin/env python3
"""
柯里化：将add(4,5) -> add(4)(5)
"""


def add(x):
	def _add(y):
		return x + y
	return _add


print(add(4)(5))

