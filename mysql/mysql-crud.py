"""
CRUD
"""
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
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
	
	
	
except Exception as e:
	print(e)
	session.rollback()
finally:
	pass







