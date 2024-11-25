from flask import render_template, request, redirect, url_for
from flask import Blueprint
from sqlalchemy import select

from ..db import db
from ..models import Book

module = Blueprint("qr", __name__)

@module.route("/qr", methods=['GET'])
def books_get():
    return "このページは" + module.name + "です"

@module.route("/qr/<book_id>", methods=["GET"])
def qr_get(book_id: str):
    url_borrow = url_for("borrow.borrow_get", book_id=book_id)
    return render_template("qr.html", url_path=url_borrow)
