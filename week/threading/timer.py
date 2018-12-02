"""
实现Timer，延时执行的线程
延时计算add(x，y)
"""
from threading import Thread, Event
import datetime
import logging
logging.basicConfig(level=logging.INFO)


def nadd(x: int, y: int):
	logging.info(x + y)


class Timer:
	def __init__(self, interval, fn, *args, **kwargs):
		self.interval = interval
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.event = Event()

	def start(self):
		Thread(target=self.__run).start()

	def cancel(self):
		"""set event为 True"""
		self.event.set()
		logging.info('cancel')

	def __run(self):
		start = datetime.datetime.now()
		logging.info('waiting')

		self.event.wait(self.interval)
		"""当event标记不为True时，执行函数"""
		if not self.event.is_set():
			self.fn(*self.args, **self.kwargs)
		delta = (datetime.datetime.now() - start).total_seconds()
		logging.info('finished {}'.format(delta))


t = Timer(10, nadd, 4, 50)
t.start()
e = Event()
e.wait(4)  # 由于未设置event标记状态，所以等待4s后返回event标记为False
# t.cancel()
