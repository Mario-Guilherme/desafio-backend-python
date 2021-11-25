from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import Biblioteca
from database import db_session


class BibliotecaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model: Biblioteca = Biblioteca
        sql_session = db_session
        load_instance = True
