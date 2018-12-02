from webob import Request, Response, dec
from wsgiref.simple_server import make_server


class Application:
	def notfound(self):
		res = Response()
		res.status_code = 404
		res.body = "<h1>您访问的页面被外星人劫持了</h1>".encode()
		return res

#  定义路由表
	ROUTETABLE = {}

	@classmethod
	def register(cls, path, handler):
		cls.ROUTETABLE[path] = handler

	@dec.wsgify
	def __call__(self, request: Request) -> Response:
		return self.ROUTETABLE.get(request.path, self.notfound)(request)


def index(request: Request):
	res = Response()
	res.body = "<h1>homepage</h1>".encode()
	return res


def showpython(request: Request):
	res = Response()
	res.body = "<h1>Python</h1>".encode()
	return res


# 注册
Application.register('/', index)
Application.register('/python', showpython)

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

