#!/usr/bin/env python3
"""
将字典扁平化(FLATMAP)
源字典{'a':{'b':1, 'c':2},'d':{'e':3,'f':{'g':4}}} ---> {'a.b':1, 'a.c':2, 'd.e':3, 'd.f.g':4}
"""

# recursion
# source = {'a': {'b': 1, 'c': 2}, 'd': {'e': 3, 'f': {'g': 4}}}
source = {'d': {'e': 3, 'f': {'g': 4}}, 'a': {'b': 1, 'c': 2}}

target = {}


def flatmap(src, prefix=''):
	for k, v in src.items():
		if isinstance(v, (dict, list, set, tuple)):
			return flatmap(v, prefix=prefix + k + '.')
		else:
			target[prefix+k] = v


flatmap(source)
print(target)

