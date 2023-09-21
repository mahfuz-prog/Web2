from flask import render_template, url_for, flash, redirect, request
from flask_referral import app, db, bcrypt
from flask_referral.forms import SignUp, LogIn
from flask_referral.db_models import User, Referral
from flask_login import login_user, current_user, login_required, logout_user

@app.route('/')
@app.route('/home/')
def home():
	return render_template('home.html', title='Home')

@app.route('/sign-up/<referral_code>/', methods=['GET', 'POST'])
@app.route('/sign-up/', defaults={'referral_code': 'Company'}, methods=['GET', 'POST']) # default code is for 1st user in this case company
def signup(referral_code):
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	# /sign-up/<referral_code>/ generate 404 error if referral code is not valid
	User.query.filter_by(username=referral_code).first_or_404()
	form = SignUp()
	if request.method == 'GET':
		form.referral_code.data = referral_code
	if form.validate_on_submit():
		pw_hash = bcrypt.generate_password_hash(form.password.data)
		user = User(username=form.username.data, email=form.email.data, password=pw_hash, referral_code=form.referral_code.data)
		db.session.add(user)
		db.session.commit()

		network = User.query.filter_by(username=form.referral_code.data).first()
		ref = Referral(user_id=user.id, user_name=user.username, upline_id=network.id, network=network)
		db.session.add(ref)
		db.session.commit()
		flash(f'Account created for {form.username.data}.', 'success')
		return redirect(url_for('login'))
	return render_template('signup.html', title='Sign Up', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LogIn()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('account'))
			flash(f'You are logged in {user.username}.', 'success')
		else:
			flash(f'Bad Credentials! Try again.', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(request.referrer)

@app.route('/account/')
@login_required
def account():
	link = f"{url_for('signup', referral_code=current_user.username, _external=True)}"
	count = len(current_user.referrals)
	return render_template('account.html', title='Account', link=link, count=count)

