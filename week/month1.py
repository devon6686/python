#!/usr/bin/env python3

# ex1
import random
origin_nums = {5, 10, 3, 8, 6, 10, 9, 15, 24, 30, 27, 48, 24}
new_nums = []
count = 0

while count < 10:
	num = random.choice(list(origin_nums))
	if num % 3 == 0 and num % 4 != 0:
		new_nums.append(num)
		count += 1
print(new_nums)