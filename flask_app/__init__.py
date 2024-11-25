from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import MetaData
from flask_login import LoginManager

from flask_app import models
from .db import db

def create_app():
    # appの設定
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///bookborrow.sqlite"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "secret"

    # DBの設定
    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.filter_by(id=user_id).one_or_none()

    # Blueprintの登録
    from flask_app.views.index import index_module
    app.register_blueprint(index_module)

    from .views import books
    app.register_blueprint(books.module)

    from .views import qr
    app.register_blueprint(qr.module)

    from .views import borrow
    app.register_blueprint(borrow.module)

    from .views import barcode
    app.register_blueprint(barcode.module)

    from .views import login
    app.register_blueprint(login.module)

    return app

