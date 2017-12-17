#!/usr/bin/env python3
"""
计算杨辉三角形前6行
"""
"""
方法1：下一行依赖上一行的所有元素，是上一行所有元素两两相加的和，在2头再各加1；
	下一行循环的次数是上一行元素的个数-1
"""
triangle = [[1], [1, 1]]

for i in range(2, 6):
	cur = [1]
	pre = triangle[i-1]
	for j in range(len(pre)-1):
		cur.append(pre[j]+pre[j+1])
	cur.append(1)
	triangle.append(cur)
print(triangle)