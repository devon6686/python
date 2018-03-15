#!/usr/bin/env python3
"""
遗弃变量：'_'
EX1: 环境变量JAVA_HOME=/usr/bin，取出变量名和路径
EX2: 从lst = [1,(2,3,4),5]中，取出4
"""

key, _, val = 'JAVA_HOME=/usr/bin'.partition('=')
print(key, val)

lst = [1, (2, 3, 4), 5]
_, (*_, num), _ = lst
print(num)
