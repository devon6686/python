#!/usr/bin/env python3
"""
求100内的素数
"""

import math

primenumber = []
flag = False
for x in range(2, 10000):
	for i in primenumber:
		if x % i == 0:
			flag = True
			break
		if i >= math.ceil(math.sqrt(x)):
			flag = False
	if not flag:
		print(x)
		primenumber.append(x)