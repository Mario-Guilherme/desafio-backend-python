from models import Biblioteca


from database import db_session

from typing import List

from interface import BibliotecaInterface


class BibliotecaService:
    @staticmethod
    def get_all() -> List[Biblioteca]:
        return Biblioteca.query.all()

    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        biblioteca = Biblioteca.query.filter(Biblioteca.id == id).first()
        if not biblioteca:
            return []
        db_session.delete(biblioteca)
        db_session.commit()

        return [id]

    @staticmethod
    def create(data_atributte: BibliotecaInterface) -> Biblioteca:
        biblioteca = Biblioteca(
            titulo=data_atributte["titulo"],
            editora=data_atributte["editora"],
            foto=data_atributte["foto"],
            autores=data_atributte["autores"],
        )

        db_session.add(biblioteca)
        db_session.commit()

        return biblioteca
