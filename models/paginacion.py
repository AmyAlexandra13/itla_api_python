from typing import List, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class Paginacion(BaseModel):
    total: int
    numeroPagina: int
    limite: int
    totalPaginas: int

class ResponsePaginado(BaseModel, Generic[T]):
    estudiantes: List[T]
    paginacion: Paginacion