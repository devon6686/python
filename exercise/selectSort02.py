#!/usr/bin/env python3
"""
简单选择排序：
	2元选择排序思路：
		每次循环找到2个极值；
		同时固定左边最大值和右边最小值；
	优点：
		减少迭代的次数；
"""

lst1 = [
	[1, 3, 5, 9, 4, 2, 7, 6, 8],
	[9, 8, 7, 6, 5, 4, 3, 2, 1],
	[1, 2, 3, 4, 5, 6, 7, 8, 9],
	[1, 1, 1, 1, 1, 1, 1, 1, 1]
]

nums = lst1[0]
length = len(nums)
print(nums)
count_swap = 0
count_iter = 0

# 二元选择排序
for i in range(length // 2):
	maxindex = i
	minindex = -i - 1
	minorigin = minindex
	for j in range(i + 1, length - i):  # 每次左右都要少比较一个
		count_iter += 1
		if nums[maxindex] < nums[j]:
			maxindex = j
		if nums[minindex] > nums[-j - 1]:
			minindex = -j - 1
	print(maxindex, minindex)
	# 元素全相同的情况下
	if nums[maxindex] == nums[minindex]:
		break
	if i != maxindex:
		tmp = nums[i]
		nums[i] = nums[maxindex]
		nums[maxindex] = tmp
		count_swap += 1
		# 如果最小值被交换过，要更新索引
		if i == minindex or i == length + minindex:
			minindex = maxindex
	if minorigin != minindex:
		tmp = nums[minindex]
		nums[minindex] = nums[minorigin]
		nums[minorigin] = tmp
		count_swap += 1
print(nums, count_swap, count_iter)



