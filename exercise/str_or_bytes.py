#!/usr/bin/env python3
"""
python3 str and bytes
str = unicode
str -> encode -> bytes
bytes -> decode -> str
"""


def to_str(bytes_or_str):
	if isinstance(bytes_or_str, bytes):
		value = bytes_or_str.decode('utf-8')
	else:
		value = bytes_or_str
	return value


def to_bytes(bytes_or_str):
	if isinstance(bytes_or_str, str):
		value = bytes_or_str.encode('utf-8')
	else:
		value = bytes_or_str
	return value


test1 = '&2'
test2 = b'\x42'

print(type(test1))
print(type(to_bytes(test1)))
print([test1, to_bytes(test1)])
print(type(test2))
print(type(to_str(test2)))
print([test2, to_str(test2)])
