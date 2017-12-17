#!/usr/bin/env python3
# 转矩

"""
1 2 3      1 4
4 5 6  --> 2 5
           3 6
"""


# 方法1
"""
lst1 = [1, 2, 3, 4]
lst2 = [5, 6, 7, 8]
row = 2
column = 4
N_list = []

for i in range(column):
    for j in [lst1,lst2]:
        N_list.append(j[i])

for x in range(len(N_list)):
    if (x+1) % row == 0:
        print(N_list[x], end='\n')
    else:
        print(N_list[x], end=' ')
"""


# 原始矩阵
lst1 = range(1, 9)
row = 2
column = 4

for i in lst1:
    if i % column == 0:
        print(i, end='\n')
    else:
        print(i, end=' ')
print('{}'.format('-'*30))

# 转换矩阵
# 方法1
n_row = 4
n_column = 2
n_lst = [1, 2, 3, 4, 5, 6, 7, 8]

for i in range(n_row):
    print("{} {}".format(n_lst[i::n_row][0], n_lst[i::n_row][1]))
print('{}'.format('>'*30))

# 方法2
for i in range(n_row):
    for j in range(n_column):
        print('{}'.format(n_lst[i::n_row][j]), end=' ')
    print()
print('{}'.format('>'*30))
