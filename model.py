from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from datetime import datetime

Base = declarative_base()


class VotedAssociation(Base):
	__tablename__ = 'voted_association'
	photo_id = Column(Integer, ForeignKey('photo.id'), primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	user = relationship("User", back_populates="voted_photos")
	photo = relationship("Photo", back_populates="voted_for") 


class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	email = Column(String(255))
	name = Column(String(255))
	#profile_photo = Column(Photo)
	uploaded_photos = relationship("Photo", back_populates='user')
	voted_photos = relationship("VotedAssociation", back_populates="user")
	favorite_photos = relationship("FavoritesAssociation", back_populates="user")
	password = Column(String(255))

	def getVoted(self):
		a = []
		for i in self.voted_photos:
			a.append(i.photo)
		return a

	def getFavorites(self):
		a = []
		for i in self.favorite_photos:
			a.append(i.photo)
		return a


	
class Photo(Base):
	__tablename__ = 'photo'
	id = Column(Integer, primary_key=True)
	avgRanking = Column(Float, default=0)
	numOfVotes = Column(Integer, default=0)
	imgURL = Column(String(255))
	user_id = Column(Integer, ForeignKey('user.id'))

	comp_id = Column(Integer, ForeignKey('competition.id'))

	user = relationship("User", back_populates='uploaded_photos')
	competition = relationship("Comp", back_populates='photos')
	voted_for = relationship("VotedAssociation", back_populates="photo")

	favorited = relationship("FavoritesAssociation", back_populates="photo")

	def uploadPhoto(self, url):
		self.imgURL = url

	def getURL(self):
		return self.imgURL

	def vote(self, rating, user):
		if self in user.getVoted():
			pass
		elif rating == 2:
			z = FavoritesAssociation()
			z.photo=self
			z.user=user
			self.favorited.append(z)
		
		a = VotedAssociation()
		a.photo=self
		a.user = user
		self.voted_for.append(a)
		self.numOfVotes += 1
		self.avgRanking = (self.avgRanking + rating) / self.numOfVotes


class Comp(Base):
	__tablename__ = 'competition'
	id = Column(Integer, primary_key=True)
	expiration_date = Column(DateTime)
	running = Column(Boolean) 
	subject = Column(String(255))
	description = Column(String(255))
	photos = relationship("Photo")

	def ExpirationMechanism(self):
		if self.expiration_date>=datetime.today():
			self.running = True
		else:
			self.running = False


class FavoritesAssociation(Base):
	__tablename__ = 'favorites_association'
	photo_id = Column(Integer, ForeignKey('photo.id'), primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
	user = relationship("User", back_populates="favorite_photos")
	photo = relationship("Photo", back_populates="favorited")




engine = create_engine('sqlite:///PhotoComps.db')

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

