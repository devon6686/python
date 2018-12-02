import logging
import threading

# FORMAT = "%(asctime)s %(thread)d  %(message)s %(test)s" # 添加扩展字符串key
FORMAT = "%(asctime)s %(thread)d  %(message)s "
logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt="%Y-%m-%d-%H:%M:%S")
d = {'test': 'hello world'}

help(logging.basicConfig)

# def fadd(x, y):
# 	logging.warning("{} {}".format(threading.enumerate(), x + y))
# 	logging.info("%s %s", x, y, extra=d)
#   logging.info("{} {}".format(threading.enumerate(), x + y), extra=d)  # 日志级别和格式字符串扩展, dict


# t = threading.Timer(1, fadd, args=[4, 5])
# t.start()

# log = logging.getLogger('')
# print(log.name)
# print(log, type(log))

def testadd(x, y):
	log = logging.getLogger('a')
	print(log.name)
	print(log, type(log), log.parent)

	logging.warning("{} {}".format(threading.enumerate(), x+y))


# t = threading.Timer(1, testadd, args=[1, 2])
# t.start()

root = logging.getLogger()
print(root, id(root))

loga = logging.getLogger('a')
print(loga, id(loga), id(loga.parent))

logb = logging.getLogger('a.b')
print(logb, id(logb), id(logb.parent))