from typing import Dict
from typing import List


class LivroInterface(Dict):
    id: int
    titulo: str
    editora: str
    foto: str
    autores: List[str]
