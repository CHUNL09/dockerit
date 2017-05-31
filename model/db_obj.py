from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
import datetime

Base = declarative_base()

class AccountGroup(Base):
    __tablename__ = 'accountgroup'
    id = Column(Integer,primary_key=True)
    name = Column(String(32))
    privilege = Column(String(256),nullable=True)
    description = Column(String(256),nullable=True)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    name = Column(String(64),nullable=False,unique=True)
    password = Column(String(256),nullable=False)
    group = Column(Integer,ForeignKey(AccountGroup.id))

class NodeDB(Base):
    __tablename__ = 'node'
    id  = Column(Integer,primary_key=True)
    hostname = Column(String(64))
    ip = Column(String(64))
    port = Column(Integer)
    cpus = Column(Integer)
    mem = Column(String(64))
    images = Column(Integer)
    state = Column(String(12))
    node_group = Column(String(12))
    containers = Column(Integer)
    os_version = Column(String(64))
    kernel_version = Column(String(64))
    docker_version = Column(String(64))

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    item_id = Column(String(64))
    item_type = Column(String(32))
    key_action = Column(String(32))
    date = Column(DateTime,default=datetime.datetime.now())
    details = Column(String(256))
    user = Column(Integer,ForeignKey('user.id'))
