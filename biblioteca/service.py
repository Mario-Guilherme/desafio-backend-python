from sqlalchemy.orm import session
from biblioteca.models import Livro, Autor
from database import db_session
from biblioteca.interface import LivroInterface, AutorInterface
from biblioteca.schema import LivroSchema, AutorSchema

from typing import List, Union


interface_livro_autor = Union[LivroInterface, AutorInterface]


class LivroService:
    @staticmethod
    def get_all() -> List[Livro]:

        return Livro.query.all()

    @staticmethod
    def delete_by_id(id: int) -> List[int]:
        biblioteca = Livro.query.filter(Livro.id == id).first()
        if not biblioteca:
            return []
        db_session.delete(biblioteca)
        db_session.commit()

        return [id]

    @staticmethod
    def __save_db(value):
        db_session.add(value)
        db_session.commit()

    def create(self, data_atributte: interface_livro_autor) -> interface_livro_autor:

        livro = Livro(
            titulo=data_atributte["titulo"],
            editora=data_atributte["editora"],
            foto=data_atributte["foto"],
        )
        self.__save_db(livro)

        livro_schema = LivroSchema()
        livro_schema.load()

        return livro_schema.dump(livro)

    def create_autor(self, livro_id, autores) -> List[Autor]:

        autores = []
        for autor_x in autores:
            autor = Autor(autor_x, livro_id)
            autores.append(autor_x)
            self.__save_db(autor)

        return autores
