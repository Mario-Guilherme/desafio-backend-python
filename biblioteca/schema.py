from flask_restx import model
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields

from biblioteca.models import Livro, Autor

from database import db_session


class LivroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Livro = Livro
        sql_session = db_session
        load_instance = True

    id = auto_field()


class AutorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Autor = Autor
        sql_session = db_session
        load_instace = True

    id = auto_field()
