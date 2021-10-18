from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import json

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email not recognized', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route("sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        else:
            if len(email) < 4:
                flash("Email has to be longer than 3 characters", category='error')
            elif '@' not in email:
                flash("Please include @ in your email", category='error')
            elif len(first_name) < 2:
                flash("Name has to be longer than 1 character", category='error')
            elif password1 != password2:
                flash("Passwords not match", category='error')
            elif len(password1) < 7:
                flash("Password has to be longer than 7 character", category='error')
            else:
                new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                    password1, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash("Account has been successfully created", category='success')
                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/delete-user', methods=['POST'])
def delete_user():
    user = json.loads(request.data)
    userId = user['userId']
    user = User.query.get(userId)
    if user:
        if user.id == current_user.id:
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("auth.logout"))


@auth.route('/add-admin', methods=['POST', 'GET'])
def add_admin():
    # if not current_user.is_admin:
    #     return redirect(url_for("views.home"))

    if request.method == 'POST':
        email = request.form.get('email')
        newAdmin = User.query.filter_by(email=email).first()

        password = request.form.get('password')

        if newAdmin:
            if check_password_hash(current_user.password, password):
                flash('New admin added successfully!', category='success')
                newAdmin.is_admin = True
                db.session.commit()
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email not recognized', category='error')

    return render_template("add_admin.html", user=current_user)
