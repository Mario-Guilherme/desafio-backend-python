from models import Biblioteca


from database import db_session

from typing import List


class BibliotecaService:
    @staticmethod
    def get_all() -> List[Biblioteca]:
        return Biblioteca.query.all()
