#!/usr/bin/env python3
"""
冒泡法排序
"""

lst1 = [1, 3, 8, 9, 7, 4, 2, 5, 6]
nums = len(lst1)
count = 0
count_swap = 0

for i in range(nums):
	flag = False
	for j in range(nums-i-1):
		count += 1
		if lst1[j] > lst1[j+1]:
			tmp = lst1[j]
			lst1[j] = lst1[j+1]
			lst1[j+1] = tmp
			flag = True
			count_swap += 1
	if not flag:
		break
print(lst1, count_swap, count)
