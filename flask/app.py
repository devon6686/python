"""
flask exercise
"""
from flask import Flask, url_for, request
from flask import render_template
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('flask')
handler = logging.FileHandler('flask.log')
fmt = logging.Formatter(FORMAT)
handler.setFormatter(fmt)
logger.addHandler(handler)

# from logging.config import dictConfig
#
# dictConfig({
# 	'version': 1,
# 	'formatters': {'default': {
# 		'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
# 	}},
# 	'handlers': {'wsgi': {
# 		'class': 'logging.StreamHandler',
# 		'stream': 'ext://flask.logging.wsgi_errors_stream',
# 		'formatter': 'default'
# 	}},
# 	'root': {
# 		'level': 'INFO',
# 		'handlers': ['wsgi']
# 	}
# })

app = Flask(__name__)


# 路由
# @app.route('/')
# def index():
# 	return 'index'


# @app.route('/hello')
# def hello():
# 	return 'hello world!'


@app.route('/post/<int:post_id>')
def show_post(post_id):
	return 'Post {}'.format(post_id)


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	return 'Subpath: {}'.format(subpath)


"""
转换器类型：
	string：缺省值，接受任何不包含斜杠的文本
	int：
	float：
	path：类似string，可以接受斜杠
	uuid：接受UUID字符串
"""


@app.route('/projects/')
def projects():
	return 'The project page'


@app.route('/about')
def about():
	return 'The about page'


"""
/ 重定向行为:
	projects的URL，会自动补齐尾部'/'；
	about的url，如果访问时尾部带了'/'，会报错；
"""


@app.route('/')
def index():
	return 'index'


@app.route('/login')
def login():
	return 'login'


@app.route('/user/<username>')
def profile(username):
	# app.logger.info('user: {}'.format(username))
	logger.info('user: {}'.format(username))
	return 'User %s' % username


"""
url_for()函数用于构建指定函数的URL。它把函数名称作为第一个参数，可以接受任意个关键字参数，每个关键字参数对应URL中的变量。
未知变量讲添加到URL中作为查询参数。
"""
with app.test_request_context():
	print(url_for('index'))
	print(url_for('login'))
	print(url_for('login', next='/'))
	print(url_for('profile', username='John Doe'))


@app.route('/method', methods=['GET', 'POST'])
def method():
	if request.method == 'POST':
		return 'do post'
	else:
		return 'do show'


# 如果支持GET方法，flask会自动添加HEAD方法支持；
# url_for('static', filename='style.css')


# flask使用Jinja2模板引擎，render_template方法可以渲染模板
# flask会在templates文件夹内寻找模板
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)


# error page
@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
