from flask import Blueprint, redirect, url_for, render_template, request, flash
from .model import User

from flask_login import login_user, current_user, login_required, logout_user

from werkzeug.security import generate_password_hash, check_password_hash
from settings import db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        rem = True if request.form.get('remember') else False
        if not user or not check_password_hash(user.password, password):
            flash('Логин или пароль введены неверно!')
            return  render_template('login/login.html')
        login_user(user, remember=rem)

        return redirect(url_for('auth.profile'))
    else:
        return render_template('login/login.html')


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Такая почта уже есть!')

        new_user = User(name, generate_password_hash(password, method='sha256'), email)
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        return redirect(url_for('auth.login'))
    else:
        return render_template('login/signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('posts.main'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('login/profile.html', username=current_user.name )

