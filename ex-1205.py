#!/usr/bin/env python3
# 转矩
"""
1 2 3        1 4 7
4 5 6   --》 2 5 8
7 8 9        3 6 9
"""

"""
lst1 = range(1, 10)
for i in lst1:
	if i % 3 == 0:
		print(i, end='\n')
	else:
		print(i, end=' ')
"""

"""
str1 = "
1 2 3
4 5 6
7 8 9
"
print(str1)

for i in str1:
	print(i, len(str1))
"""
lst1 = [1, 2, 3]
lst2 = [4, 5, 6]
lst3 = [7, 8, 9]

for i in [lst1, lst2, lst3]:
	for j in i:
		print(j, end=' ')
	print()

N_list = []

for i in range(3):
	for x in [lst1, lst2, lst3]:
		N_list.append(x[i])
print(N_list)

for j in range(len(N_list)):
	if (j+1) % 3 == 0:
		print(N_list[j], end="\n")
	else:
		print(N_list[j], end=" ")