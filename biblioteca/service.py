from flask import abort
from sqlalchemy.orm import selectin_polymorphic, session
from biblioteca.models import Livro, Autor
from database import db_session
from biblioteca.interface import LivroInterface, AutorInterface
from biblioteca.schema import LivroSchema, AutorSchema

from typing import Any, Iterable, List, Union

import json


interface_livro_autor = Union[LivroInterface, AutorInterface]


class LivroService:
    def __init__(self) -> None:
        pass

    ######################### GET #############################
    @staticmethod
    def get_autor(livro_id):
        return Autor.query.filter_by(livro_id=livro_id)

    @staticmethod
    def get_livro():
        return Livro.query.all()

    def get_all(self) -> List[Union[Livro, Autor]]:
        livros = self.get_livro()
        livros_autores = []
        dicionario_livro_autor = {}
        for livro in livros:
            dicionario_livro_autor["titulo"] = livro.titulo
            dicionario_livro_autor["editora"] = livro.editora
            dicionario_livro_autor["foto"] = livro.foto

            autores = self.get_autor(livro.id)
            autores_lista = [autor.autor for autor in autores]
            dicionario_livro_autor["autores"] = autores_lista
            livros_autores.append(dicionario_livro_autor)

        return json.dumps(livros_autores)

    ############################# DELETE ###############################################
    def delete_by_id(self, livro: Livro, autores: List[str]) -> None:
        self.delete_autor(autores)
        self.delete_livro(livro)

    @staticmethod
    def delete_livro(livro: Livro) -> None:
        db_session.delete(livro)
        db_session.commit()

    @staticmethod
    def delete_autor(autores: List[str]) -> None:
        for autor in autores:
            db_session.delete(autor)
            db_session.commit()

    @staticmethod
    def find_id_livro(id: int) -> Livro:
        return Livro.query.filter(Livro.id == id).first()

    @staticmethod
    def find_id_autor(livro_id: int):
        return Autor.query.filter(Autor.livro_id == livro_id)

    ######################################### POST ##########################################
    @staticmethod
    def __save_db(value: Any) -> None:
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

        return autores_list

    def create(self, data_atributte: interface_livro_autor) -> interface_livro_autor:

        livro = self.create_livro(
            data_atributte["titulo"], data_atributte["editora"], data_atributte["foto"]
        )

        self.create_autor(livro.id, data_atributte["autores"])
        return json.dumps(data_atributte)

    ################################# PUT ####################################

    def put_livro_autor():
        pass

    @staticmethod
    def find_existing_livro(titulo: str, editora: str, foto: str) -> Union[Livro, Any]:
        existing_livro = (
            Livro.query.filter(Livro.titulo == titulo)
            .filter(Livro.editora == editora)
            .filter(Livro.foto == foto)
            .first()
        )
        return existing_livro
