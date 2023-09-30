# Referral System - Flask
#### In this system, username is used for the referral code. If any new user doesn't have any referral code then by default Company will get the referral.

*signup route default = Company*

*create a default user with Username = Company*

```
from flask_referral import app, db, bcrypt
with app.app_context():
...  db.create_all()
```

```
from flask_referral.db_models import User
with app.app_context():
...  p = bcrypt.generate_password_hash('asd')
...  u = User(username='Company', email='company@gmail.com', password=p)
...  db.session.add(u)
...  db.session.commit()
```
