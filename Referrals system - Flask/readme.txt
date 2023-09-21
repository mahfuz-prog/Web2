In this system, username used for the referral code. If any new user doesn't have any referral code then by default Company will get the referral.
signup route default = Company

Before running the application run those commands in python environment to instantiate the database and create a default user with Username = Company.
from flask_referral import app, db, bcrypt
with app.app_context():
...  db.create_all()

from flask_referral.db_models import User
with app.app_context():
...  p = bcrypt.generate_password_hash('anything')
...  u = User(username='Company', email='company@gmail.com', password=p)
...  db.session.add(u)
...  db.session.commit()
