from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields

from biblioteca.models import Livro

from database import db_session


class LivroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Livro = Livro
        sql_session = db_session
        load_instance = True

    id = auto_field()
