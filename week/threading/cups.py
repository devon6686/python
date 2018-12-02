"""老板雇佣一个工人，让他生产杯子，老板一直等着工人，直到工人生产10个杯子"""
from threading import Thread, Event
import logging
import time


FORMAT = '%(asctime)s %(threadName)s %(thread)d %(message)s'
logging.basicConfig(level=logging.INFO, datefmt=FORMAT)


def boss(event: Event):
	# logging.info('I am boss, waiting for U')
	event.wait()
	logging.info('Good Job.')


def worker(event: Event, count=10):
	logging.info("I am working for U")
	cups = []
	while True:
		logging.info('make 1')
		time.sleep(0.5)
		cups.append(1)
		if len(cups) >= count:
			event.set()
			break
	logging.info("I finished my job, cups={}".format(len(cups)))


event = Event()
w = Thread(target=worker, args=(event,))
b = Thread(target=boss, args=(event,))

w.start()
b.start()