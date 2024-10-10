from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    # appの設定
    app = Flask(__name__, instance_relative_config=True)

    app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///blog.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "secret"

    # DBの設定
    db.init_app(app)
    from flask_app import models
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return models.Account.query.filter_by(id=user_id).one_or_none()

    # Blueprintの登録
    from flask_app.views.index import index_module
    app.register_blueprint(index_module)

    return app

