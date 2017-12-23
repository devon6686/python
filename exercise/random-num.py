#!/usr/bin/env python3
"""
随机取10个数：
	数字取值范围[1,20]
	重复的数字及次数
	不重复的数字
"""
import random


num = []
repeat = {}
single = []

for _ in range(10):
	num.append(random.randint(1, 20))

for value in num:
	if num.count(value) > 1:
		repeat[value] = num.count(value)
	else:
		single.append(value)

print("{}-->{}".format("RepeatNum", "Count"))
for repeatNum, count in repeat.items():
	print("{:>4}:{:^4}".format(repeatNum, count))

print("SingleNum:")
for singleNum in single:
	print("{:^2}".format(singleNum), end=' ')

