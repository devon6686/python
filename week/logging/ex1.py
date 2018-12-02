import logging


FORMAT = "%(asctime)s %(thread)d  %(message)s "
logging.basicConfig(format=FORMAT, datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
# logging.basicConfig 实际上是创建root log格式; default log level: WARNING

root = logging.getLogger()
print(root, id(root))

log1 = logging.getLogger('s')
# log1 = logging.getLogger(__name__)    # 保证不同名；不同模块，如果同名，实例对象就是同一个
log1.setLevel(logging.INFO)
print(log1.getEffectiveLevel())

handler1 = logging.FileHandler('./log_error.log')
handler1.setLevel(logging.ERROR)
fmtr = logging.Formatter('%(levelname)s %(asctime)s %(thread)d  %(threadName)s %(message)s')
handler1.setFormatter(fmtr)
log1.addHandler(handler1)

log2 = logging.getLogger('s.s1')
log2.setLevel(30)
print(log2.getEffectiveLevel())

handler2 = logging.FileHandler('./log_warning.log')
handler2.setLevel(logging.WARNING)
log2.addHandler(handler2)

log3 = logging.getLogger('s.s1.s11')
log3.setLevel(10)
print(log3.getEffectiveLevel())

handler3 = logging.FileHandler('./log_info.log')
handler3.setLevel(logging.INFO)
log3.addHandler(handler3)

log3.info('log3 info')
log2.warning('log2 warning')
log1.error('log1 error')



