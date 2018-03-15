#!/usr/bin/env python3
"""
猴子偷桃问题：
	猴子第一天摘下若干个桃子，当即吃了一半，还不过瘾，又多吃了一个。第二天早上又将剩下的桃子吃了一半，又多吃了一个。
	以后每天早上都吃了前一天剩余桃子的一半零1个。到第10天早上想吃时，发现只要1个桃子了。求第一天共摘了多少个桃子。

d1 -> n/2 - 1
d2 -> d1/2 -1
d3 -> d2/2 - 1
...
d9 -> d8/2 -1
d10 --> d9/2 -1 = 1
"""

"""
#随着天数的减少，来计算
def fn(day=10, total=1):
	total = 2 * (total + 1)
	day -= 1
	if day == 1:
		return total
	return fn(day, total)


print(fn())
"""


# 随着天数的增加来计算
def fn(day=1):
	if day == 10:
		return 1
	return 2*(fn(day + 1) + 1)


print(fn())