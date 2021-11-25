from typing import Dict
from typing import List
from typing import Union


class BibliotecaInterface(Dict[Union[int, str, List[str]]]):
    id: int
    titulo: str
    editora: str
    foto: str
    autores: List[str]
