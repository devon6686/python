"""
	路径正则化
	方法过滤
	路由分组，按照前缀分别路由,一级目录：/product, /python
"""
from webob import Request, Response, dec, exc
from wsgiref.simple_server import make_server
import re


class Router:
	def __init__(self, prefix: str='/'):
		self.__prefix = prefix.rstrip('/\\')
		#  定义路由表
		# ROUTETABLE = []
		# /product/tv/1234 /product/tc/abc
		# /python/student/16
		# /product/(\w+)/(?P<id>\d+)
		self.__routetable = []

	@property
	def prefix(self):
		return self.__prefix

	def route(self, pattern, *methods):
		def wrapper(handler):
			# cls.ROUTETABLE[path] = handler
			self.__routetable.append((methods, re.compile(pattern), handler))
			return handler
		return wrapper

	def get(self, pattern):
		return self.route(pattern, "GET")

	def post(self, pattern):
		return self.route(pattern, "POST")

	def match(self, request) -> Response:
		#  判断prefix
		if not request.path.startswith(self.prefix):
			return None
		for methods, pattern, handler in self.__routetable:
			if not methods or request.method in methods:
				if request.method.upper() == "GET":
					matcher = pattern.match(request.path.replace(self.prefix, '', 1))
					if matcher:
						# 动态增加属性
						request.args = matcher.group()  # 所有分组组成的元组，包括命名的
						request.kwargs = matcher.groupdict()  # 命名分组组成的字典
						return handler(request)


class Application:
	ROUTERS = []

	@classmethod
	def register(cls, router: Router):
		cls.ROUTERS.append(router)

	@dec.wsgify
	def __call__(self, request: Request) -> Response:
		for router in self.ROUTERS:
			response = router.match(request)
			if response:
				return response
		raise exc.HTTPNotFound("您访问的页面被外星人劫持了")


idx = Router()
py = Router('/python')

# 注册
Application.register(idx)
Application.register(py)


@idx.get('^/$')
def index(request: Request):
	res = Response()
	res.body = "<h1>Home Page</h1>".encode()
	return res


@py.post('/python')
def showpython(request: Request):
	res = Response()
	res.body = "<h1>Python</h1>".encode()
	return res


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

