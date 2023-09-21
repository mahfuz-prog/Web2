from flask_referral import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(30), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	joined_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	referral_code = db.Column(db.String(20), nullable=True)
	referrals = db.relationship('Referral', backref='network', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.joined_time}', '{self.referrals}')"

class Referral(db.Model):
	__tablename__ = 'referral'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, unique=True, nullable=False)
	user_name = db.Column(db.String(20), unique=True, nullable=False)
	upline_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Referral('user_id: {self.user_id}', 'user_name: {self.user_name}', 'upline_id: {self.upline_id}')"
	