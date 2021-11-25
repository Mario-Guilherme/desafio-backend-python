from sqlalchemy import Column, Integer, String, ARRAY

from database import Base

from typing import List

from interface import BibliotecaInterface


class Biblioteca(Base):
    __tablename__ = "biblioteca"

    id: int = Column(Integer, primary_key=True)
    titulo: str = Column(String)
    editora: str = Column(String)
    foto: str = Column(String)
    autores: List[str] = Column(ARRAY(String))

    def update(self, changes: BibliotecaInterface):
        for key, val in changes.items():
            setattr(self, key, val)
        return self

    def __repr__(self) -> str:
        return f"<Title {self.titulo}>"
