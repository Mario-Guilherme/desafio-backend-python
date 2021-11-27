from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

from typing import List


class Livro(Base):
    __tablename__ = "livro"

    id: int = Column(Integer, primary_key=True)
    titulo: str = Column(String)
    editora: str = Column(String)
    foto: str = Column(String)

    autores = relationship("Autor", backref="livro")

    def __repr__(self) -> str:
        return f"<Title {self.titulo}>"


class Autor(Base):
    __tablename__ = "autor"

    id: int = Column(Integer, primary_key=True)
    autor: str = Column(String)

    livro_id = Column(Integer, ForeignKey("livro.id"))

    def __repr__(self) -> str:
        return f"<Title {self.autor}>"
