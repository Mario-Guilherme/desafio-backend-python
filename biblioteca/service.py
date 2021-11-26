from biblioteca.models import Livro, Autor
from database import db_session
from biblioteca.interface import LivroInterface, AutorInterface
from biblioteca.schema import LivroSchema, AutorSchema

from typing import List, Union

import json


interface_livro_autor = Union[LivroInterface, AutorInterface]


class LivroService:
    def __init__(self) -> None:
        pass

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
    def __save_db(value) -> None:
        db_session.add(value)
        db_session.commit()

    def create_livro(self, titulo: str, editora: str, foto: str) -> Livro:
        livro = Livro(titulo=titulo, editora=editora, foto=foto)
        self.__save_db(livro)
        return livro

    def create_autor(self, livro_id: int, autores: List[str]) -> List[Autor]:

        autores_list = []
        for autor_x in autores:
            autor = Autor(autor=autor_x, livro_id=livro_id)
            self.__save_db(autor)
            autores_list.append(autor_x)
        print(autores_list)
        return autores_list

    def create(self, data_atributte: interface_livro_autor) -> interface_livro_autor:

        livro = self.create_livro(
            data_atributte["titulo"], data_atributte["editora"], data_atributte["foto"]
        )

        self.create_autor(livro.id, data_atributte["autores"])
        return json.dumps(data_atributte)
