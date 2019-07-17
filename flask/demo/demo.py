from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:devon123@127.0.0.1:32769/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
	name = db.Column(db.String(32), nullable=False, unique=True, server_default='')

	def __repr__(self):
		return '<Role %r>' % self.name


class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), nullable=False, unique=True, index=True)
	email = db.Column(db.String(128), unique=True)
	role_id = db.Column(db.Integer, nullable=False)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r, Role id %r>' %(self.username, self.role_id)





