from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from flask_migrate import Migrate

class Base(DeclarativeBase):
  pass

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

db = SQLAlchemy(
  model_class=Base, 
  metadata=MetaData(
    naming_convention=convention
  )
)

migrate = Migrate(db=db)