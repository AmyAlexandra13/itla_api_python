from typing import List, Optional

from pydantic import BaseModel

from models.paginacion import PaginacionUNICDA


class EditorialUnicda(BaseModel):
    id: int
    nombre: str


class LibroUNICDA(BaseModel):
    """Modelo para libros de UNICDA"""
    id: int
    editorialId: int
    titulo: str
    sinopsis: Optional[str] = None
    anoPublicacion: Optional[int] = None
    archivoURL: Optional[str] = None
    imagenURL: Optional[str] = None
    editorial: Optional[EditorialUnicda] = None


class LibrosUNICDAPaginadoResponse(BaseModel):
    pagination: "PaginacionUNICDA"
    data: List[LibroUNICDA]
