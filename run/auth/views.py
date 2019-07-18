"""Route definitions for the auth blueprint."""

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from run import db
from . import auth
from ..models import User, Role
from .forms import (LoginForm, RegistrationForm, ChangePasswordForm,
                    PasswordResetRequestForm, PasswordResetForm)
from ..decorators import admin_required
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Define the login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.home')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Define the logout route."""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Define the user registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    display_name=form.display_name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Define the change password route."""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.home'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/admin')
@login_required
@admin_required
def admin():
    """Define the user admin route."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template("auth/admin.html", users=users, roles=roles)
