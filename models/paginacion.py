from typing import List, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class Paginacion(BaseModel):
    total: int
    numeroPagina: int
    limite: int
    totalPaginas: int

class ResponsePaginado(BaseModel, Generic[T]):
    items: List[T]
    paginacion: Paginacion


class PaginacionUNICDA(BaseModel):
    pages: int
    records: int
    currentPage: int
    prevPage: int
    nextPage: int