#!/usr/bin/env python3
"""
堆排序：
	为了和树编码对应，增加一个无用的0在首位。
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


origin = [0, 30, 50, 10, 70, 80, 20, 90, 40, 60]

total = len(origin) - 1
print(origin)
print_tree2(origin)


def heap_adjust(n, i, array:list):
	"""
	调整当前结点（核心算法）
	调整的结点的起点在n//2，保证所有调整的结点都有孩子结点
	:param n:待比较数个数
	:param i:当前结点的下标
	:param array:待排序数据
	:return:
	"""
	while 2*i < n:
		# 孩子结点判断，2i为左孩子，2i+1为右孩子
		lchild_index = 2 * i
		max_child_index = lchild_index # n = 2i
		if n > lchild_index and array[lchild_index + 1] > array[lchild_index]: # n>2i说明还有右孩子
			max_child_index = lchild_index + 1

		# 和子树的根结点比较
		if array[max_child_index] > array[i]:
			array[max_child_index], array[i] = array[i], array[max_child_index]
			i = max_child_index  # 被交换后，还需要判断是否需要调整
		else:
			break
		# print_tree2(array)  # 到目前为止，只是解决了单个结点的调整(70, 40, 60),下面使用循环依次解决比起始结点编号小的结点；


heap_adjust(total, total//2, origin)
# print(origin)
# print_tree2(origin)


"""
构建大顶堆：
	起点的选择：
		从最下层最右边叶子结点的父结点开始，由于构造了一个前置的0，所以编号和索引相等，但是元素个数等于长度-1；
	下一个结点：
		按照二叉树性质5编号的结点，从起点开始找编号逐个递减的结点，直至编号为1；
"""


def max_heap(total, array:list):
	for i in range(total//2, 0, -1):
		heap_adjust(total, i, array)
	return array


print_tree2(max_heap(total, origin))

