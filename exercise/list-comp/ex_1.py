#!/usr/bin/env python3
"""
1.1 返回1-10的平方;
1.2 有一个列表lst=[1, 4, 9 ,16, 2, 5, 10, 15],生成一个新列表，要求元素是lst相邻2项的和；
1.3 打印九九乘法表;
1.4 生成100个格式如"1001.asdgdjssebf",以'.'分隔，左边是以1开始的4位数字，右边是10位随机的小写英文字母；
"""
import random


# square(1,10)
nums = [i**2 for i in range(1,11)]
print(nums)

# new list
lst = [1, 4, 9, 16, 2, 5, 10, 15]
new_lst = [lst[i] + lst[i+1] for i in range(len(lst) - 1)]
print(new_lst)

# 99乘法表
ROW_FMT = '{}*{}={:<3}{}'
[print(ROW_FMT.format(j, i, i*j, '\n' if i == j else ''), end="") for i in range(1, 10) for j in range(1, i + 1)]

# ID generator
# ASCII a-c -> 97-121
id_lst = [print('{:04}.{}'.format(i, "".join([chr(random.randint(97, 122)) for _ in range(10)]))) for i in range(1, 101)]
