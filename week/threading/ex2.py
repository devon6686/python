#!/usr/bin/env python3
import threading

X = 'abc'
ctx = threading.local()
ctx.x = 123
print(type(ctx), type(ctx.x))


def worker():
	print(X)
	print(ctx)
	# ctx.x = 567   #  线程间资源隔离，threading.local相当于本地局部变量的作用
	print(ctx.x)


threading.Thread(target=worker).start()
