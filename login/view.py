from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from login.login_forms import RegisterForm, LoginForm
from models import User, db


login_blueprint = Blueprint('login_blueprint', __name__, template_folder='templates')


@login_blueprint.route('/register', methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == register_form.email.data))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login_blueprint.login'))
        new_user = User(
            email=register_form.email.data,
            password=generate_password_hash(register_form.password.data, method='pbkdf2:sha256', salt_length=8),
            name=register_form.name.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=register_form)


@login_blueprint.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        password = login_form.password.data
        result = db.session.execute(db.select(User).where(User.email == login_form.email.data))
        user = result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login_blueprint.login'))
            # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login_blueprint.login'))
        else:
            login_user(user)
            return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=login_form)


@login_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))
