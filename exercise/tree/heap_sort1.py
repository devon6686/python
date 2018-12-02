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


# origin = [0, 30, 50, 10, 40, 80, 20, 90, 70, 60]
origin = [0, 40, 50, 70, 60, 90, 10, 30, 80, 20]

length = len(origin) - 1

print(origin)
print_tree2(origin)


def heap_adjust(n, i, array: list):
	"""
	调整当前结点（核心算法）
	调整的结点的起点在n//2，保证所有调整的结点都有孩子结点，该结点是父结点；
	:param n:待比较数个数
	:param i:当前结点的下标
	:param array:待排序数据
	:return:
	"""
	while 2*i <= n:
		# 孩子结点判断，2i为左孩子，2i+1为右孩子
		lchild_index = 2 * i
		max_child_index = lchild_index  # n = 2i
		if n > lchild_index and array[lchild_index + 1] > array[lchild_index]:  # n>2i说明还有右孩子
			max_child_index = lchild_index + 1

		# 和子树的根结点比较
		if array[max_child_index] > array[i]:
			array[max_child_index], array[i] = array[i], array[max_child_index]
			i = max_child_index  # 被交换后，还需要判断是否需要调整
		else:
			break
		# print('~'*20)
		# print_tree2(array)


"""
	到目前为止，只是解决了单个结点的调整,下面使用循环依次解决比起始结点编号小的结点；
"""


# heap_adjust(length, length//2, origin)
# print(origin)
# print_tree2(origin)


"""
构建大顶堆：
	起点的选择：
		从最下层最右边叶子结点的父结点开始，由于构造了一个前置的0，所以编号和索引相等，但是元素个数等于长度-1；
	下一个结点：
		按照二叉树性质5编号的结点，从起点开始找编号逐个递减的结点，直至编号为1；
	大顶堆不稳定；
"""


def max_heap(total, array: list):
	for i in range(total//2, 0, -1):
		heap_adjust(total, i, array)
		print_tree2(array)
	return array


print('{}1{}'.format('-'*10, '-'*10))
print_tree2(max_heap(length, origin))


"""
排序：
	思路：
		1.在大顶堆的基础上，每次都要让堆顶的元素和最后一个元素结点交换，然后排除最后一个元素，形成一个新的被破坏的堆；
			因为列表origin被影子copy，元素顺序发生变化；
		2.让它重新调整，调整后，堆顶一定是最大元素；
		3.再次重复1，2步，直至剩余最后一个元素；
"""


def sort1(total, array: list):
	while total > 1:
		array[1], array[total] = array[total], array[1]
		total -= 1

		heap_adjust(total, 1, array)
		print(array)
	return array


print('{}2{}'.format('-'*10, '-'*10))
print_tree2(sort1(length, origin))


"""
改进：
	如果只剩最后2个元素了，如果后一个结点比堆顶大，就不用调整了；
"""


def sort2(total, array: list):
	while total > 1:
		array[1], array[total] = array[total], array[1]
		total -= 1
		if total == 2 and array[total] >= array[total - 1]:
			break
		heap_adjust(total, 1, array)
	return array


# print('{}3{}'.format('-'*10, '-'*10))
# print_tree2(sort2(length, origin))
