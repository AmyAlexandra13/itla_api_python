from typing import Optional

from pydantic import BaseModel


class UsuarioOut(BaseModel):
    usuarioId: int
    nombre: str


class EditorialOut(BaseModel):
    editorialId: int
    nombre: str


class Libro(BaseModel):
    libroId: int
    titulo: str
    sipnosis: Optional[str] = None
    yearPublicacion: Optional[int] = None
    archivoUrl: Optional[str] = None
    imagenUrl: Optional[str] = None
    estado: str
    cantidadDisponible: int
    fechaCreacion: str  # formato ya viene como string (DD-MM-YYYY HH24:MI:SS)
    fechaActualizacion: Optional[str] = None
    usuarioCreacion: UsuarioOut
    usuarioActualizacion: UsuarioOut | None = None
    editorial: EditorialOut
