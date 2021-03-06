from biblioteca.models import Livro, Autor
from database import db_session
from biblioteca.interface import LivroInterface, AutorInterface

from typing import Any, Iterable, List, Union

import json
import csv

import os

import pandas as pd


interface_livro_autor = Union[LivroInterface, AutorInterface]
ALLOWED_EXTENSIONS = {"csv"}


class LivroService:

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
            dicionario_livro_autor.update({"titulo": livro.titulo})
            dicionario_livro_autor.update({"editora": livro.editora})
            dicionario_livro_autor.update({"foto": livro.foto})

            autores = self.get_autor(livro.id)
            autores_lista = [autor.autor for autor in autores]
            dicionario_livro_autor.update({"autores": autores_lista})
            livros_autores.append(dicionario_livro_autor)
            dicionario_livro_autor = {}

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

    @staticmethod
    def __update_db(value: Any) -> None:
        db_session.merge(value)
        db_session.commit()

    def update_livro(self, livro: Livro, titulo: str, editora: str, foto: str) -> None:
        livro_new = Livro(titulo=titulo, editora=editora, foto=foto)
        livro_new.id = livro.id
        self.__update_db(livro_new)

    def update_autor(
        self, autores_olds: Iterable[Autor], autores_news: List[str], livro_id: int
    ) -> None:

        self.delete_autor(autores_olds)

        for autor_new in autores_news:
            autor = Autor(autor=autor_new, livro_id=livro_id)
            self.__save_db(autor)

    @staticmethod
    def spawn_dict_temp() -> None:
        if not os.path.exists(os.path.join(os.getcwd(), "uploads")):
            os.makedirs(os.path.join(os.getcwd(), "uploads"))

    @staticmethod
    def allowed_file(filename) -> bool:
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    def save_data_csv_db(self, path) -> None:
        with open(path, encoding="utf-8") as file:
            rows_csv = csv.DictReader(file)
            for row in rows_csv:
                livro = self.create_livro(
                    titulo=str(row["titulo"]),
                    editora=str(row["editora"]),
                    foto=str(row["foto"]),
                )
                self.create_autor(livro_id=livro.id, autores=eval(row["autores"]))

    @staticmethod
    def delete_csv(path) -> None:
        if os.path.exists(path):
            os.remove(path)

    def make_file_to_email(self) -> str:
        all_data = self.get_all()
        path_file = "uploads/dados_livros.csv"
        self.spawn_dict_temp()
        pd.DataFrame(json.loads(all_data)).to_csv(path_file, index=False)
        return path_file
