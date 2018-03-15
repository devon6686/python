#!/usr/bin/env python3
"""
将一个列表转换成二叉树
方法1：居中对齐
"""


import math


def print_tree(array, unit_width=2):
	length = len(array)
	depth = math.ceil(math.log2(length + 1))
	width = 2**depth - 1
	index = 0

	for i in range(depth):
		for j in range(2**i):
			print('{:^{}}'.format(array[index], width * unit_width), end=' ' * unit_width)
			index += 1

			if index >= length:
				break
		width = width//2
		print()


lst = [10, 30, 40, 50, 90, 60, 80, 20, 70, 10, 20, 30, 40, 50, 60]
print_tree(lst)
