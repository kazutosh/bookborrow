from datetime import date
from flask import render_template, request, redirect, url_for, abort
from flask import Blueprint
from flask_login import current_user
from sqlalchemy import select

from ..db import db
from ..models import Book

module = Blueprint("books", __name__)

@module.route("/books", methods=['GET'])
def books_get():
    books = db.session.scalars(select(Book))
    return render_template('books.html', books=books, currect_user=current_user)

@module.route("/books/<book_id>/delete", methods=['POST'])
def books_delete(book_id):
    book = db.session.scalar(select(Book).where(Book.id == book_id))
    if book:
        db.session.delete(book)
        db.session.commit()
    return redirect(url_for(".books_get"))

@module.route("/create", methods=["POST"])
def book_create():
    book_name = request.form["book_name"]
    book_author = request.form["book_author"]
    book_isbn = request.form["book_isbn"]

    new_book = Book(
        title=book_name,
        authors=book_author,
        isbn=book_isbn  
    )
    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for(".books_get"))

@module.route("/books/<book_id>", methods=["GET"])
def book_detail(book_id: int):
    book = db.session.scalar(select(Book).where(Book.id == book_id))
    if book == None:
        abort(404)

    return render_template("book_detail.html", book=book)

@module.route("/editBook", methods=["POST"])
def book_edit():
    book_id = request.form["id"]
    book = db.session.scalar(select(Book).where(Book.id == book_id))
    if book == None:
        abort(404)

    for key, value in request.form.items():
        if key == "id":
            book.id = value
        elif key == "title":
            book.title = value
        elif key == "authors":
            book.authors = value
        elif key == "isbn":
            book.isbn = value
        elif key == "publisher":
            book.publisher = value
        elif key == "published_date":
            book.published_date = date.fromisoformat(value) if value else None

    db.session.commit()

    return redirect(url_for(".book_detail", book_id=book_id))