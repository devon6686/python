#!/usr/bin/env python3
import time

import threading


class MyThread(threading.Thread):

	def start(self) -> None:
		print('start')
		super().start()

	def run(self) -> None:
		print('run')
		super().run()


def worker1(n=5):
	print('current_thread\n\t', threading.current_thread())
	print('Main_thread\n\t', threading.main_thread())
	print(threading.active_count())
	print('enumerate\n\t', threading.enumerate())
	for _ in range(n):
		time.sleep(1)
		print('t1: hello world')
	print('Thread over')


def worker(n=5):
	print(threading.current_thread())
	for _ in range(n):
		time.sleep(1)
		print('hello world2')
	print('Thread Over')


# print(threading.current_thread(), '-----')
# t = threading.Thread(target=worker1, name='worker')
# t.start()
# print('enumerate\n\t', threading.enumerate(), '********')


t = MyThread(target=worker, name='w1')
# t.run()
t.start()
print('~~~~~' * 20)

t1 = MyThread(target=worker, name='w2')
# t.run()       # start方法是多线程，run方法只是普通的函数调用
t1.start()
