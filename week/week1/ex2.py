#!/usr/bin/env python3
"""
2-1:快速统计字符串每个元素出现的次数： 如"abcevaefegsgdghfdefavbdr"， “a”:x,"b":y
2-2:快速统计字符串每个元素出现的次数： 如"abcevaefegsgdghfdefavbdr"， “a”:x,"b":y，
	根据出现的次数降序排列，并且列出出现次数最多的三个元素
"""

import collections

str1 = "abcevaefegsgdghfdefavbdr"
num = 3
c1 = collections.Counter(str1)
c2 = c1.items()
print(c2, '--'*40)

c3 = sorted(c2, key=lambda x: x[1], reverse=True)

c4 = c1.most_common(3)
print(c3, '\n', c4)