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
    def create(data_atributte: interface_livro_autor) -> interface_livro_autor:
        print(data_atributte)

        livro = Livro(
            titulo=data_atributte["titulo"],
            editora=data_atributte["editora"],
            foto=data_atributte["foto"],
        )
        db_session.add(livro)
        db_session.commit()

        autores = []
        for autor_x in data_atributte["autores"]:
            autor = Autor(autor_x, livro.id)
            autores.append(autor_x)
            db_session.add(autor)

        livro_schema = LivroSchema()
        livro_schema.load()
        # novo_titulo = schema.load(data_atributte, session=db_session)
        db_session.commit()

        return livro_schema.dump(livro)
