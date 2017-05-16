from model import *

#User
user = User(
	name='a',
	email='a',
	password='a')
session.add(user)



#Competition
subject = 'This Weeks Competition: Street Photography'
exdate = '2017-5-27'
description = 'Street photography, also sometimes called candid photography, is photography conducted for art or enquiry that features unmediated chance encounters and random incidents[1] within public places. Although there is a difference between street and candid photography it is usually subtle with most street photography being candid in nature but not all candid photography being classifiable as street photography. Street photography does not necessitate the presence of a street or even the urban environment. Though people usually feature directly, street photography might be absent of people and can be of an object or environment where the image projects a decidedly human character in facsimile or aesthetic.'
competition = Comp(
	expiration_date=datetime.strptime(exdate, '%Y-%m-%d'),
	subject=subject,
	description=description,
	running=True)
session.add(competition)
session.commit()