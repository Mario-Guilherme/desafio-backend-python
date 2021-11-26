from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from biblioteca.interface import BibliotecaInterface

from typing import List


class Livro(Base):
    __tablename__ = "livro"

    id: int = Column(Integer, primary_key=True)
    titulo: str = Column(String)
    editora: str = Column(String)
    foto: str = Column(String)

    autores = relationship("Autor", backref="livro")

    def update(self, changes: BibliotecaInterface):
        for key, val in changes.items():
            setattr(self, key, val)
        return self

    def __repr__(self) -> str:
        return f"<Title {self.titulo}>"
