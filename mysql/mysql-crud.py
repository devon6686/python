"""
CRUD操作
sqlalchemy.insepct(entity)函数可以查看状态。
常见的状态值有transient，pending， persistent，deleted，detached。
transient：实体类尚未加入到session中，同时并没有保存到数据库中；
pending：transient的实体被add()加入到session中，状态切换到pending，但它还没有flush到数据库中；
persistent：session中的实体对象对应着数据库中的真实记录。pending状态在提交成功后可以变成persistent状态，
	或者查询成功返回的实体也是persistent状态
deleted：实体被删除且已经flush但未commit完成；事务提交成功了，实体变成detached，
	事务失败，返回persistent；
detached：删除成功的实体进入这个状态；
"""
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Enum, func
from sqlalchemy.orm import sessionmaker


# 实体基类
Base = declarative_base()


# 实体类
class Student(Base):
	__tablename__ = 'student'

	id = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
	name = Column(String(64), nullable=True)
	age = Column(Integer)

	def __repr__(self):
		return "<{} id:{} name:{} age:{}>".format(self.__class__.__name__, self.id, self.name, self.age)

	__str__ = __repr__


#  引擎，管理连接池
host = '127.0.0.1'
port = 32769
user = 'root'
password = 'devon123'
database = 'test'

conn_str = "mysql+pymysql://{}:{}@{}:{}/{}".format(user, password, host, port, database)
engine = sqlalchemy.create_engine(conn_str, echo=True)

Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)

Session = sessionmaker()
session = Session(bind=engine)

try:
	# insert
	# student = Student()
	# student.name = 'tom'
	# student.age = 20
	#
	# session.add(student)
	# student1 = Student()
	# session.add_all([student1, student2])

	# lst = []
	# for i in range(5):
	# 	student = Student()
	# 	student.name = 'tom' + str(i)
	# 	student.age = 20 + i
	# 	lst.append(student)
	# 
	# session.add_all(lst)
	# session.commit()  # pending

	# select 
	# query_obj = session.query(Student).filter(Student.age > 20)
	# query_obj = session.query(Student).filter(Student.age > 20).filter(Student.age < 40)
	# for x in query_obj:
	# 	print(x)

	# update
	# student = session.query(Student).get(2)
	# student.age = 40
	# session.add(student)

	# delete
	student = session.query(Student).get(2)
	session.delete(student)

	session.commit()
except Exception as e:
	print(e)
	session.rollback()
finally:
	pass







