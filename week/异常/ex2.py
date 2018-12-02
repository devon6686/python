#!/use/bin/env python3
import time


def foo1():
	try:    # 一般来说try最多不超过3层
		1/0
	finally:
		print('fool1 fin')
		# return # finally不建议使用return，否则异常会被吞并；


def foo2():
	time.sleep(3)
	foo1()

	while True:
		print('--'*10)
		time.sleep(1)


try:
	foo2()
except Exception as e:
	print('outer', e)
finally:
	print('outer fin')      # 内层异常如果没有处理就会继续向外抛出，直到主线程退出；


