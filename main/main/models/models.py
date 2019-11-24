from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Date,
)

from .meta import Base

from datetime import datetime

# class TestModel(Base):
#     __tablename__ = 'test_table'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text)
#     value = Column(Integer)
#     date = Column(DateTime, default=datetime.now())

# Index('test_index', TestModel.name, unique=True, mysql_length=255)


# class TestModel2(Base):
#     __tablename__ = 'test_table2'
#     id = Column(Integer, primary_key=True)
#     name = Column(Text)
#     value = Column(Integer)
#     date = Column(DateTime, default=datetime.now())

# Index('test2_index', TestModel2.name, unique=True, mysql_length=255)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(Text)
    uuid = Column(Text)

class Access(Base):
    __tablename__ = 'access'
    id = Column(Integer, primary_key=True)
    exp_date = Column(Date)