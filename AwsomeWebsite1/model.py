from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	email = Column(String(255))
	name = Column(String(255))
	photos = relationship("Photo", back_populates='user')
	password = Column(String(255))
	
class Photo(Base):
	__tablename__ = 'photo'
	avgRanking = Column(Float)
	numOfVotes = Column(Integer)
	imgURL = Column(String(255), primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship("User", back_populates='photos')

class Comp(Base):
	__tablename__ = 'competition'
	id = Column(Integer, primary_key=True)
	subject = Column(String(255))
	photos = relationship("Photo")


engine = create_engine('sqlite:///PhotoComps.db')

Base.metadata.create_all(engine)