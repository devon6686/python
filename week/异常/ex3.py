#!/usr/bin/env python3

try:
	1/0
except ArithmeticError:
	print('ArithmeticError')
except:
	print('except')
else:   # 异常没有发生时执行的语句
	print('else')
finally:
	print('fin')


# try的工作原理：
# 1、如果try中语句执行时发生异常，搜索except子句，并执行第一个匹配该异常的except子句；
# 2、如果try中语句执行时发生异常，却没有匹配的except子句，异常将被递交到外层的try，如果外层不处理这个异常，异常将继续向外层传递；
# 	如果都不处理该异常，则会传递到最外层，如果还没有处理，就终止异常所在的线程；
# 3、如果在try执行时没有发生异常，将会执行else子句中的语句；
# 4、无论try中是否发生异常，finally子句最终都会执行；
