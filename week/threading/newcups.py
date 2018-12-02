"""10个人生产100个杯子"""
import threading
import logging

logging.basicConfig(level=logging.INFO)

cups = []
locker = threading.Lock()


def worker(lock: threading.Lock, task=100):
	while True:
		lock.acquire()
		count = len(cups)
		# lock.release()
		logging.info(count)
		if count >= task:
			lock.release()
			break       # no release lock
		# lock.acquire()
		cups.append(1)
		lock.release()
		logging.info("{} make 1".format(threading.current_thread().name))
	logging.info("result: {}".format(len(cups)))


for x in range(10):
	threading.Thread(target=worker, args=(locker, 100)).start()
