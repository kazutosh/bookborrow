from flask import render_template, request, redirect, url_for, flash
from flask import Blueprint
from flask_login import current_user, login_user, logout_user
from sqlalchemy import select

from ..db import db
from ..models import User

module = Blueprint("login", __name__)

@module.route("/login", methods=['GET'])
def login_get():
    return render_template("login.html")

@module.route("/signup", methods=["GET"])
def signup_get():
    return render_template("signup.html")

@module.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    user = db.session.scalar(select(User).where(User.email==email))
    if not user or not user.check_password(password):
        return redirect(url_for(".login_get"))
    
    login_user(user)
    return redirect(url_for("index.index_get"))

@module.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    password = request.form.get("password")

    # TODO: 存在するユーザの場合の処理
    existing_user = db.session.scalar(select(User).where(User.email==email))
    if existing_user:
        return redirect(url_for(".signup_get"))
    
    user = User(name=email + "さん", email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    login_user(user)
    return redirect(url_for("index.index_get"))

@module.route("/logout", methods=["GET"])
def logout_get():
    logout_user()
    return redirect(url_for(".login_get"))