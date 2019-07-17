"""
	路径正则化
	方法过滤
	路由分组，按照前缀分别路由,一级目录：/product, /python
"""
from webob import Request, Response, dec, exc
from wsgiref.simple_server import make_server
import re


class Application:
	# def notfound(self):
	# 	res = Response()
	# 	res.status_code = 404
	# 	res.body = "<h1>您访问的页面被外星人劫持了</h1>".encode()
	# 	return res

	#  定义路由表
	# ROUTETABLE = {}
	ROUTETABLE = []
	# /product/tv/1234 /product/tc/abc
	# /python/student/16
	# /product/(\w+)/(?P<id>\d+)

	@classmethod
	def route(cls, pattern, *methods):
		def wrapper(handler):
			# cls.ROUTETABLE[path] = handler
			cls.ROUTETABLE.append((methods, re.compile(pattern), handler))
			return handler
		return wrapper

	@classmethod
	def get(cls, pattern):
		return cls.route('GET', pattern)

	@classmethod
	def post(cls, pattern):
		return cls.route('POST', pattern)

	@dec.wsgify
	def __call__(self, request: Request) -> Response:
		for methods, pattern, handler in self.ROUTETABLE:
			if not methods or request.method in methods:
				if request.method.upper() == "GET":
					matcher = pattern.match(request.path)
					if matcher:
						# 动态增加属性
						request.args = matcher.group()  # 所有分组组成的元组，包括命名的
						request.kwargs = matcher.groupdict()  # 命名分组组成的字典
						return handler(request)
		raise exc.HTTPNotFound("<h1>您访问的页面被外星人劫持了</h1>")
		# return self.ROUTETABLE.get(request.path, self.notfound)(request)


@Application.route('GET', '^/$')
def index(request: Request):
	res = Response()
	res.body = "<h1>homepage</h1>".encode()
	return res


@Application.route('POST', '^/python$')
def showpython(request: Request):
	res = Response()
	res.body = "<h1>Python</h1>".encode()
	return res


# 注册
# Application.route('/', index)
# Application.route('/python', showpython)

if __name__ == '__main__':
	ip = '127.0.0.1'
	port = 9000
	server = make_server(ip, port, Application())
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	finally:
		server.server_close()

