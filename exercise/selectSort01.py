#!/usr/bin/env python3
"""
简单选择排序：
	思路：每次循环找到极值，放到一端；
"""

lst1 = [
	[1, 3, 5, 9, 4, 2, 7, 6, 8],
	[9, 8, 7, 6, 5, 4, 3, 2, 1],
	[1, 2, 3, 4, 5, 6, 7, 8, 9]
]

nums = lst1[0]
count_swap = 0
count_iter = 0

for i in range(len(nums)):
	maxindex = i
	for j in range(i + 1, len(nums)):
		count_iter += 1
		if nums[maxindex] < nums[j]:
			maxindex = j
	if i != maxindex:
		tmp = nums[i]
		nums[i] = nums[maxindex]
		nums[maxindex] = tmp
		count_swap += 1
print(nums, count_swap, count_iter)


