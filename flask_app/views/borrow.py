from datetime import date, datetime, timedelta
from dataclasses import dataclass

from flask import render_template, request, redirect, url_for, abort, Response
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

    accept_wait = AcceptWait(
        will_cancel_at=datetime.now() + timedelta(hours=1)
    )

    borrow = Borrow(
        user_id=current_user.id,
        book_id=book.id,
        return_expected_at=date.today() + timedelta(days=7),
        borrowed_at=date.today(),
        accept_wait=accept_wait
    )

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
    if (
        not current_borrow or 
        current_borrow.user_id != current_user.id or
        current_borrow.accept_wait and not current_borrow.accept_wait.is_accepted
    ):
        abort(400)
    
    current_borrow.returned_at = date.today()
    db.session.commit()

    return redirect(url_for(".borrows_get"))

@module.route("/accept")
def accept_get():
    waits = db.session.scalars(
        select(AcceptWait)
        .where(AcceptWait.is_accepted == False)
        .options(joinedload(AcceptWait.borrow))
    )

    if len(request.args.keys()) == 0:
        return render_template("accept.html", waits=waits) 
    
    is_accept = bool(request.args.get("is_accept"))
    accept_id = request.args.get("accept_id")

    wait = db.session.scalar(
        select(AcceptWait)
        .where(AcceptWait.id == accept_id)
        .options(joinedload(AcceptWait.borrow))
    )

    if wait and not wait.is_accepted:
        if is_accept:
            wait.is_accepted = True
        else:
            db.session.delete(wait)
            db.session.delete(wait.borrow)

        db.session.commit()

    res = Response(status=302)
    res.location = request.path
    res.headers["X-Debug"] = str(wait.borrow)
    return res
        



@module.route("/history", methods=['GET'])
def history_get():
    borrows = db.session.scalars(
        select(Borrow)
        .where(Borrow.user_id==current_user.id)
        .options(joinedload(Borrow.book))
    )
    return render_template("history.html", borrows = borrows)
