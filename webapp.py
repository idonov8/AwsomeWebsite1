# all the imports
from model import*
import os
import sqlite3
from flask import Flask, request, session as login_session, g, redirect, url_for, abort, render_template, flash, send_from_directory
#from flask_dance.contrib.google import make_google_blueprint, google
#import json
#import flask_login
#from flask_login import LoginManager, login_required, logout_user
#login_manager = LoginManager()
from datetime import datetime
from flask_uploads import *

#from dateutil.parser import parse
#import pandas as pd

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

#login_manager.init_app(app)

engine = create_engine('sqlite:///PhotoComps.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()


app.secret_key = "supersekrit"
'''
blueprint = make_google_blueprint(
    client_id="256940704567-4ta4m3aic8dn9gtnj12pfianjckrgrag.apps.googleusercontent.com",
    client_secret="s__arhyb5FMRxTJjdDaGuDQL",
    scope=["profile", "email"])
app.register_blueprint(blueprint, url_prefix="/login")
'''
UPLOAD_FOLDER = 'static/uploads'

#To do list:

# - Make the css links work, start doing design ####

# - Find a way to use DateTime in competition table |V|
# 	+ Finishing manager page |V|

# - Discover Page
#	+ Write the algorithems for voting.
# 	+ Somehow remember the photos the user voted for. 
# 	+ Make the picture to change when user vote 

# 	+ Creat a user profile page

# - Uploading Pictures 
# 	+ html for it |V|
# 	+ How do i put a "list" of photos in one column of the user's table |V|

# 	+ Space in database for extra info about photographers (for the profile page)------

# - Deploy the webapp |V|


@app.route('/', methods=['POST', 'GET'])
def HomePage():
	#if request.method=='POST' or 'id' in login_session:
		return redirect(url_for('CompHome'))
	#else:
	#	return render_template('HomePage.html')

@app.route('/login', methods=['POST', 'GET'])
def login(  ):
	if request.method=='POST':
		email = request.form['email']
		password = request.form['password']
		user = session.query(User).filter_by(email=email).first()
		
		if email==password and password=='admin':
			return redirect(url_for('manager'))

		if user is None:
			flash('Wrong Email or Password')
			return redirect(url_for('login'))

		if email is None or password is None:
			flash('Missing Argument')
			return redirect(url_for('login'))

		if password==user.password:
			#flask_login.login_user(user, remember=False, force=True, fresh=True)
			login_session['name'] = user.name
			login_session['email'] = user.email
			login_session['id'] = user.id
			login_session['logged_in'] = True
			return redirect(url_for('HomePage'))
	else:
		return render_template('login.html')


	'''#Google Stuff
	if not google.authorized:
		return redirect(url_for("google.login"))
	resp = google.get("/plus/v1/people/me")
	assert resp.ok, resp.text
	return "You are {email} on Google".format(email=resp.json()["emails"][0]["value"])
	#return redirect(url_for("HomePage"))
	user = User(
		)
		'''

@app.route('/Competition', methods=['POST','GET'])
def CompHome():
	#if 'id' in login_session and request.method=='GET':
		competitions = session.query(Comp).all()
		for competition in competitions:
			competition.ExpirationMechanism()
			compet = session.query(Comp).filter_by(running=True).one_or_none()
			if compet is not None:
				login_session['compID'] = compet.id
				return render_template('CompetitionHomePage.html', comp=compet, comps=competitions, session= login_session)
			
		return 'No competition is running at the moment.'

	#else:
	#y	return redirect(url_for('HomePage'))
	

@app.route('/signup', methods=['POST', 'GET'])
def SignUp():
	if request.method=='GET':
		return render_template("SignUp.html")
	else:
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		if name == "" or email == "" or password == "":
			flash("Your form is missing arguments")
			return redirect(url_for('SignUp'))
		if session.query(User).filter_by(email=email).first() is not None:
			flash("A user with this email address already exists")
			return redirect(url_for('SignUp'))
		else:
			user = User(
				name=name,
				email=email,
				password=password)
			session.add(user)
			session.commit()
			login_session['name'] = name
			login_session['email'] = email
			login_session['id'] = user.id
			login_session['logged_in'] = True
			return redirect(url_for('CompHome'))

@app.route('/discover')
def Discover():
	if request.method == 'POST':
		return 'YEAHHHHH'
	#if 'id' in login_session:
	compet = session.query(Comp).filter_by(id=login_session['compID']).one()
	return render_template('Discover.html', comp=compet, session=login_session)
	#else:
	#	return redirect(url_for('HomePage'))

@app.route('/upload', methods=['POST', 'GET'])
def Upload():
	if request.method == 'POST':
		pic = request.files['pic']
		#for pic in pics:
		photo = Photo(
				numOfVotes=0,
				user_id=login_session['id'],
				comp_id=login_session['compID'],
				)
		session.add(photo)
		session.commit()
		pic_filename = str(photo.id) + "_" + secure_filename(pic.name) + ".jpeg"
		pic.save(os.path.join(UPLOAD_FOLDER, pic_filename))
		photo.uploadPhoto(pic_filename)
		session.commit()
		return redirect(url_for('CompHome'), )

	if 'id' not in login_session:
		return redirect(url_for('HomePage'))

	else:
		user = session.query(User).filter_by(id=login_session['id']).one()
		return render_template('Upload.html', user=user, session=login_session)

@app.route('/logout')
def logout():
	'''Google Stuff
    logout_user()
    return redirect(url_for("HomePage"))
	'''
	del login_session['name']
	del login_session['email']
	del login_session['id']
	login_session['logged_in'] = False
	return redirect(url_for('HomePage'))

@app.route('/manager', methods=['POST','GET'])
def manager():
	if request.method=='POST':
		#update competition
		subject = request.form['subject']
		exdate = request.form['expiration date']
		description = request.form['description']
		competition = Comp(
			expiration_date=datetime.strptime(exdate, '%Y-%m-%d'),
			subject=subject,
			description=description)
		competition.ExpirationMechanism()
		session.add(competition)
		session.commit()
		return redirect(url_for('HomePage'))
	else:
		return render_template("manager.html")

if __name__ == "__main__":
	app.debug=True
	app.run()
