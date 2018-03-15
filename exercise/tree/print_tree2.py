#!/usr/bin/env python3
"""
列表转换二叉树
方法2：投影栅格实现
lst = [10, 30, 40, 50, 90, 60, 80, 20, 70, 10, 20, 30, 40, 50, 60]
"""


import math


def print_tree2(array):
	"""
		前空格     元素间隔
	1     7         0
	2     3         7
	3     1         3
	4     0         1
	"""
	index = 1
	depth = math.ceil(math.log2(len(array)))
	sep = " "

	for i in range(depth):
		offset = 2 ** i
		print(sep * (2**(depth - i - 1) - 1), end='')
		line = array[index: index + offset]
		for j, x in enumerate(line):
			print('{:>{}}'.format(x, len(sep)), end='')
			interval = 0 if i == 0 else 2 ** (depth - i) - 1

			if j < len(line) - 1:
				print(sep * interval, end='')
		index += offset
		print()


print_tree2([0, 10, 20, 30, 40, 50, 70, 90, 60, 80])