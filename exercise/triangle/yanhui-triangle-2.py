#!/usr/bin/env python3
"""
计算杨辉三角形前6行
	方法2：方法1的变体，把前2行也写入循环中进行判断;
"""
triangle = []
n = 6

for i in range(n):
	row = [1]
	triangle.append(row)
	if i == 0:
		continue
	for j in range(i-1):
		row.append(triangle[i-1][j]+triangle[i-1][j+1])
	row.append(1)
print(triangle)