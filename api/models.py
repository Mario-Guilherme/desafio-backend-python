from re import I
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ARRAY

from database import Base, db_session

from typing import List


class Biblioteca(Base):
    __tablename__ = "biblioteca"

    id: int = Column(Integer, primary_key=True)
    titulo: str = Column(String)
    editora: str = Column(String)
    foto: str = Column(String)
    autores: str = Column(ARRAY(String))

    def __init__(
        self,
        id: int = None,
        titulo: str = None,
        editora: str = None,
        foto: str = None,
        autores: List[str] = None,
    ) -> None:

        self.id = id
        self.titulo = titulo
        self.editora = editora
        self.autores = autores

    def __repr__(self) -> str:
        return f"<Title {self.titulo}>"
