# all the imports
from model import*
import os
import sqlite3
from flask import Flask, request, session as login_session, g, redirect, url_for, abort, render_template, flash
from flask_dance.contrib.google import make_google_blueprint, google
import json 
import flask_login
from flask_login import LoginManager, login_required, logout_user
login_manager = LoginManager()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

login_manager.init_app(app)

engine = create_engine('sqlite:///PhotoComps.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()


app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id="256940704567-4ta4m3aic8dn9gtnj12pfianjckrgrag.apps.googleusercontent.com",
    client_secret="s__arhyb5FMRxTJjdDaGuDQL",
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/', methods=['POST', 'GET'])
def HomePage():
	if request.method=='POST' or 'id' in login_session:
		return redirect(url_for('CopmHome'))
	else:
		return render_template('HomePage.html')

@app.route('/login', methods=['POST', 'GET'])
def login(  ):
	if request.method=='POST':
		#insert login logic
		email = request.form['email']
		password = request.form['password']
		user = session.query(User).filter_by(email=email)
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

@app.route('/Competition')
def CompHome():
	return render_template('CompetitionHomePage.html')

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
		if session.query(User).filter_by(email = email).first() is not None:
			flash("A user with this email address already exists")
			return redirect(url_for('SignUp'))
		else:
			user = User(
				name=name,
				email=email,
				password=password)
			session.add(user)
			session.commit()
			return redirect(url_for('CompHome'))

@app.route('/logout')
@login_required
def logout():
	'''Google Stuff
    logout_user()
    return redirect(url_for("HomePage"))
	'''


if __name__ == "__main__":
	app.run(debug=True)