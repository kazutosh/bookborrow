from flask import render_template, request, redirect, url_for
from flask import Blueprint
from sqlalchemy import select

from ..db import db
from ..models import Book

module = Blueprint("borrow", __name__)

@module.route("/borrow", methods=['GET'])
def books_get():
    return "このページは" + module.name + "です"
