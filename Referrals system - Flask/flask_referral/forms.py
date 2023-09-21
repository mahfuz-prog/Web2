from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from flask_referral.db_models import User

class SignUp(FlaskForm):
	username = StringField('Name', validators=[DataRequired(), Length(min=2, max=40)])
	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=30)])
	password = PasswordField('Password', validators=[DataRequired()])
	referral_code = StringField('Referral Code', validators=[])
	submit = SubmitField('Create Account')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username taken. Try another one!')

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError('Email taken. Try another one!')
			
	def validate_referral_code(self, referral_code):
		ref = User.query.filter_by(username=referral_code.data).first()
		if ref is None:
			raise ValidationError('Invalid referral code.')

class LogIn(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=30)])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')
