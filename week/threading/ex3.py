import logging
import threading

FORMAT = "%(asctime)s %(thread)d  %(message)s %(test)s"
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d-%H:%M:%S")
d = {'test': 'hello world'}


def fadd(x, y):
	logging.warning("{} {}".format(threading.enumerate(), x + y))
	logging.info("%s %s", x, y, extra=d)
	logging.info("{} {}".format(threading.enumerate(), x + y), extra=d)  # 日志级别和格式字符串扩展, dict


t = threading.Timer(1, fadd, args=[4, 5])
t.start()
