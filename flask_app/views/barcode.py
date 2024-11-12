from flask import render_template, request, redirect, url_for
from flask import Blueprint
from sqlalchemy import select

from ..db import db
from ..models import Book

module = Blueprint("barcode", __name__)

@module.route("/barcode", methods=['GET'])
def books_get():
    return "このページは" + module.name + "です"
