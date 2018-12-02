#!/usr/bin/env python3


# f = None      #可以事先定义变量f为None

try:
	f = open('test1')
# except MyException as e:
# 	print(e)
# except OSError as e:
# 	print('InterruptedError')
except Exception as e:
	print(e, type(e))
finally:    # finally语句是最后执行的语句，不管前面是否出现异常；
	print("clean work")
	try:
		f.close()   # 第9行如果文件不存在错误，会导致f变量没有定义，因此需要在finally语句在执行清理操作的时候注意变量f；
	except NameError:
		print('NameError: f')

print(dir())    # 查看当前环境或模块中所有的变量
print('outer')


