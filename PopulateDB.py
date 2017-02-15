from model import *

#User
user = User(
	name='a',
	email='a',
	password='a')
session.add(user)



#Competition
subject = 'Test'
exdate = '2017-2-18'
description = 'Test Test 123'
competition = Comp(
	expiration_date=datetime.strptime(exdate, '%Y-%m-%d'),
	subject=subject,
	description=description
	running=True)
session.add(competition)
session.commit()