from flask import render_template, request, redirect, url_for
from flask import Blueprint
from sqlalchemy import select

from ..db import db
from ..models import Book

module = Blueprint("books", __name__)

@module.route("/books", methods=['GET'])
def books_get():
    books = db.session.scalars(select(Book))
    return render_template('books.html', books=books)

@module.route("/create", methods=["POST"])
def book_create():
    book_name = request.form["book_name"]
    book_author = request.form["book_author"]
    book_isbn = request.form["book_isbn"]

    new_book = Book(
        name=book_name,
        author=book_author,
        isbn=book_isbn  
    )
    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for(".books_get"))

@module.route("/delete", methods=["POST"])
def book_delete():
    book_id = request.form["book_id"]
    book = db.session.scalar(select(Book).where(Book.id == book_id))
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for(".books_get"))
