#!/usr/bin/env python3
"""
1.快速生成52张扑克牌
2.随机选取一张牌
"""
import random
# 随机生成52张
kind = ["heart", "spade", "club", "diamond"]
lst1 = list(range(2, 11))
lst1.extend(list("JQKA"))

poker = [x+str(y) for x in kind for y in lst1]
print(poker)
print('---'*20)

# 随机选取一张牌
color = random.choice(kind)
num = random.choice(lst1)
print("Random choice: \n\tcolor:{} card:{}".format(color, num))
print('---'*20)
