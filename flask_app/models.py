from sqlalchemy.orm import Mapped, mapped_column

from .db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    isbn: Mapped[str] = mapped_column(nullable=True)


# DBのテーブルを定義する
# class Account(UserMixin, db.Model):
#     # テーブル名を指定
#     __tablename__ = 'Account'
#     # 数値型のidカラム
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     # 文字列型のnameカラム
#     name = db.Column(db.String(128), unique= True)

#     # mail = db.Column(db.String(128), unique=True)
#     password = db.Column(db.String(256))

#     def set_password(self, password):
#         self.password = generate_password_hash(password)

#     # 入力されたパスワードが登録されているパスワードハッシュと一致するかを確認
#     def check_password(self, password):
#             return check_password_hash(self.password, password)

# class User(db.Model):
#     id: Mapped[int] = mapped_column(primary_key=True)
#     username: Mapped[str] = mapped_column(unique=True)
#     email: Mapped[str]