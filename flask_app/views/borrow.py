from datetime import date, datetime, timedelta
from dataclasses import dataclass

from flask import render_template, request, redirect, url_for, abort
from flask import Blueprint
from flask_login import login_required, current_user
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..db import db
from ..models import Book, Borrow, User, AcceptWait

module = Blueprint("borrow", __name__)

@module.route("/borrow/<book_id>", methods=['GET'])
@login_required
def borrow_get(book_id: str):
    book = db.session.scalar(select(Book).where(Book.id==book_id))
    if not book:
        abort(404)

    return_exptected_at = date.today() + timedelta(days=7)
    current_borrow = db.session.scalar(select(Borrow).where(Borrow.book_id==book_id).where(Borrow.returned_at==None))
    return render_template("borrow.html", 
                           book=book,
                           current_borrow=current_borrow, 
                           return_exptected_at=return_exptected_at)

@module.route("/borrows", methods=['GET'])
@login_required
def borrows_get():
    borrows = db.session.scalars(
        select(Borrow)
        .where(Borrow.user_id==current_user.id)
        .where(Borrow.returned_at==None)
        .options(joinedload(Borrow.book))
    )
    return render_template("borrows.html", borrows=borrows)

@module.route("/borrow/<book_id>", methods=['POST'])
@login_required
def borrow_post(book_id: str):
    book = db.session.scalar(select(Book).where(Book.id==book_id))
    if not book:
        abort(404)

    current_borrow = db.session.scalar(select(Borrow).where(Borrow.book_id==book_id).where(Borrow.returned_at==None))
    if current_borrow:
        # 借りられているなら400
        abort(400)
    
    borrow = Borrow(
        user_id=current_user.id,
        book_id=book.id,
        return_expected_at=date.today() + timedelta(days=7),
        borrowed_at=date.today()
    )

    accept_wait = AcceptWait(
        borrow=borrow,
        will_cancel_at=datetime.now() + timedelta(hours=1)
    )
    borrow.accept_wait = accept_wait

    db.session.add(borrow)
    db.session.add(accept_wait)
    db.session.commit()

    return redirect(url_for(".borrows_get"))

@module.route("/return/<book_id>", methods=['POST'])
@login_required
def return_post(book_id: str):
    book = db.session.scalar(select(Book).where(Book.id==book_id))
    if not book:
        abort(404)
    
    current_borrow = db.session.scalar(select(Borrow).where(Borrow.book_id==book_id).where(Borrow.returned_at==None))
    if not current_borrow or current_borrow.user_id != current_user.id:
        abort(400)
    
    current_borrow.returned_at = date.today()
    db.session.commit()

    return redirect(url_for(".borrows_get"))

@module.route("/accept")
def accept_get():
    return render_template("accept.html")


@module.route("/history", methods=['GET'])
def history_get():
    borrows = db.session.scalars(
        select(Borrow)
        .where(Borrow.user_id==current_user.id)
        .options(joinedload(Borrow.book))
    )
    return render_template("history.html" ,borrows = borrows)
