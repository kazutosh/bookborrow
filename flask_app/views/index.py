from flask import render_template, redirect, url_for
from flask import Blueprint
from flask_login import current_user

index_module = Blueprint("index", __name__)

@index_module.route("/",methods=['GET'])
def index_get():
    if current_user.is_authenticated:
        return redirect(url_for("borrow.borrows_get"))
    
    return redirect(url_for("login.login_get"))

@index_module.route("/quagga", methods=["GET"])
def index_quagga_get():
    return render_template("quagga.html")